param(
    [string]$ContractsDir = "..\Conxian\contracts",
    [string]$OutputPath = "..\Conxian\Clarinet.toml"
)

$projectDir = Resolve-Path "$PSScriptRoot\..\Conxian"
$contractsAbs = Resolve-Path "$PSScriptRoot\$ContractsDir"
$outputAbs = Resolve-Path "$PSScriptRoot\$OutputPath"

Write-Host "Scanning: $contractsAbs"

# Map of contract file paths to names
$contractNames = @{}
# Map of contract names to their deps
$contractDeps = @{}

# First pass: get all .clar files and assign names
Get-ChildItem -Path $contractsAbs -Recurse -Filter "*.clar" | ForEach-Object {
    $relPath = $_.FullName.Substring($projectDir.Length + 1).Replace('\', '/')
    
    # Strip extension and convert path to contract name
    $name = ($_.BaseName -replace '[-.]', '-').ToLower()
    
    $contractNames[$_.FullName] = @{
        Name = $name
        Path = $relPath
    }
}

Write-Host "Found $($contractNames.Count) .clar files"

# Second pass: scan for dependencies in each file
foreach ($file in (Get-ChildItem -Path $contractsAbs -Recurse -Filter "*.clar")) {
    $content = Get-Content $file.FullName -Raw
    $name = $contractNames[$file.FullName].Name
    $deps = @{}
    
    # Find contract-call? patterns: (contract-call? .some-contract ...)
    $content | Select-String -Pattern '\(contract-call\?\s*\.([a-zA-Z0-9_-]+)' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object {
            $depName = $_.Groups[1].Value.ToLower()
            if ($depName -ne $name) {
                $deps[$depName] = $true
            }
        }
    }
    
    # Find impl-trait patterns: (impl-trait .some-trait ...)
    $content | Select-String -Pattern '\(impl-trait\s+\.([a-zA-Z0-9_-]+)' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object {
            $depName = $_.Groups[1].Value.ToLower()
            if ($depName -ne $name) {
                $deps[$depName] = $true
            }
        }
    }
    
    # Find use-trait patterns: (use-trait .some-trait ...)
    $content | Select-String -Pattern '\(use-trait\s+\.([a-zA-Z0-9_-]+)' -AllMatches | ForEach-Object {
        $_.Matches | ForEach-Object {
            $depName = $_.Groups[1].Value.ToLower()
            if ($depName -ne $name) {
                $deps[$depName] = $true
            }
        }
    }
    
    $contractDeps[$name] = @{
        Path = $contractNames[$file.FullName].Path
        Deps = $deps.Keys | Sort-Object
    }
}

Write-Host "Extracted dependencies for $($contractDeps.Count) contracts"

# Generate Clarinet.toml
$lines = @()

$lines += "[project]"
$lines += "name = `"Conxian`""
$lines += "authors = []"
$lines += "description = `"`""
$lines += "telemetry = false"
$lines += "requirements = []"
$lines += "clarinet_version = `"latest`""
$lines += "epoch = `"latest`""
$lines += ""

$lines += "[accounts]"
$lines += "deployer = `"ST1PQHQKV0RJXZFY1DGX8MNSNYVE3VGZJSRTPGZGM`""
$lines += ""

$lines += "[simnet]"
$lines += "mnemonic = `"cute bird surprise boring old news cake design aisle helmet choose tree`""
$lines += ""

$lines += "[repl.analysis]"
$lines += "passes = [`"check_checker`"]"
$lines += ""

$lines += "[repl.analysis.check_checker]"
$lines += "strict = false"
$lines += "trusted_sender = false"
$lines += "trusted_caller = false"
$lines += "callee_filter = false"
$lines += ""

# Sort contracts by name for consistent output
$sorted = $contractDeps.Keys | Sort-Object
foreach ($name in $sorted) {
    $info = $contractDeps[$name]
    $lines += "[contracts.$name]"
    $lines += "path = `"$($info.Path)`""
    $lines += "clarity_version = 4"
    $lines += "epoch = `"latest`""
    
    if ($info.Deps.Count -gt 0) {
        $depsList = ($info.Deps | ForEach-Object { "`"$_`"" }) -join ", "
        $lines += "depends_on = [$depsList]"
    }
    
    $lines += ""
}

# Write output
$lines -join "`r`n" | Set-Content -Path $outputAbs -NoNewline
Write-Host "Generated Clarinet.toml with $($contractDeps.Count) contracts -> $outputAbs"
