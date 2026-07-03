# ConxiusOrbit Publishing Guide

**Version**: 1.2.10
**Status**: Ready to publish  
**Repository**: https://github.com/Conxian/conxius_orbit

**Note**: This guide was drafted for the initial v1.2.10 publish; update tag/version references for newer releases.

---

## 📦 Publishing Checklist

### ✅ Completed
- [x] Repository created and published to GitHub
- [x] Code committed (conxius_orbit.py, package.json, setup.py)
- [x] Documentation complete (README.md, CONTRIBUTING.md)
- [x] Tests added (17-test validation suite)
- [x] License added (MIT)
- [x] CI/CD workflows configured (.github/workflows/)
- [x] Version tagged (v1.2.10)

### ⏳ Pending
- [ ] Configure npm token (NPM_TOKEN secret)
- [ ] Configure PyPI token (PYPI_API_TOKEN secret)
- [ ] Verify GitHub Actions workflows
- [ ] Publish to npm registry
- [ ] Publish to PyPI registry
- [ ] Create GitHub release

---

## 🔑 Token Configuration

### Step 1: Get npm Token

1. **Create npm account** (if needed):
   - Go to https://www.npmjs.com/signup
   - Create account with email

2. **Generate Access Token**:
   - Log in to npm
   - Go to: https://www.npmjs.com/settings/[username]/tokens
   - Click "Generate New Token"
   - Select: **Automation** token type
   - Copy the token (starts with `npm_...`)

3. **Add to GitHub Secrets**:
   - Go to: https://github.com/Conxian/conxius_orbit/settings/secrets/actions
   - Click "New repository secret"
   - Name: `NPM_TOKEN`
   - Value: Paste your npm token
   - Click "Add secret"

### Step 2: Get PyPI Token

1. **Create PyPI account** (if needed):
   - Go to https://pypi.org/account/register/
   - Verify email

2. **Generate API Token**:
   - Log in to PyPI
   - Go to: https://pypi.org/manage/account/token/
   - Click "Add API token"
   - Token name: `conxius_orbit-github-actions`
   - Scope: **Entire account** (or create project first for project-specific)
   - Copy the token (starts with `pypi-...`)

3. **Add to GitHub Secrets**:
   - Go to: https://github.com/Conxian/conxius_orbit/settings/secrets/actions
   - Click "New repository secret"
   - Name: `PYPI_API_TOKEN`
   - Value: Paste your PyPI token
   - Click "Add secret"

---

## 🚀 Publishing Methods

### Method 1: Automatic (Recommended)

**GitHub Actions will automatically publish when you push a tag:**

```bash
# Tag already pushed: v1.2.10
# GitHub Actions will:
# 1. Run all tests on all platforms
# 2. Publish to npm (if NPM_TOKEN configured)
# 3. Publish to PyPI (if PYPI_API_TOKEN configured)
# 4. Create GitHub release
```

**Check workflow status**:
- Go to: https://github.com/Conxian/conxius_orbit/actions
- Look for "Publish ConxiusOrbit" workflow
- Verify it runs successfully after configuring tokens

### Method 2: Manual Publishing

#### npm Manual Publish

```bash
cd conxius_orbit

# Login to npm
npm login

# Publish
npm publish

# Verify
npm view conxius_orbit
```

#### PyPI Manual Publish

```bash
cd conxius_orbit

# Install build tools
pip install build twine

# Build package
python -m build

# Check package
twine check dist/*

# Upload to PyPI
twine upload dist/*

# Verify
pip search conxius_orbit
```

---

## 📋 Post-Publishing Checklist

After successful publishing:

### npm Package
- [ ] Verify at: https://www.npmjs.com/package/conxius_orbit
- [ ] Test installation: `npm install -g conxius_orbit`
- [ ] Test CLI: `conxius_orbit --version`
- [ ] Update README badges

### PyPI Package
- [ ] Verify at: https://pypi.org/project/conxius_orbit/
- [ ] Test installation: `pip install conxius_orbit`
- [ ] Test CLI: `conxius_orbit --version`
- [ ] Update README badges

### GitHub Release
- [ ] Verify at: https://github.com/Conxian/conxius_orbit/releases
- [ ] Check release notes
- [ ] Verify downloadable assets
- [ ] Star the repository! ⭐

---

## 🔍 Verification Commands

### Test npm Installation

```bash
# Install globally
npm install -g conxius_orbit

# Check version
conxius_orbit --version

# Check installation
which conxius_orbit  # Unix/Mac
where conxius_orbit  # Windows

# Launch GUI
conxius_orbit
```

### Test PyPI Installation

```bash
# Create virtual environment (recommended)
python -m venv test-env
source test-env/bin/activate  # Unix/Mac
test-env\Scripts\activate     # Windows

# Install
pip install conxius_orbit

# Check version
python -c "import conxius_orbit; print('Installed')"

# Launch GUI
python -m conxius_orbit
# Or
conxius_orbit
```

---

## 📈 Current Status

### Repository
- **GitHub**: ✅ Published
  - URL: https://github.com/Conxian/conxius_orbit
  - Branch: main
  - Tag: v1.2.10
  - Commits: 2

### Package Registries
- **npm**: ⏳ Awaiting token configuration
  - Package name: `conxius_orbit`
  - Version: 1.2.10
  - Entry: `conxius_orbit` command

- **PyPI**: ⏳ Awaiting token configuration
  - Package name: `conxius_orbit`
  - Version: 1.2.10
  - Entry: `conxius_orbit` command

### CI/CD
- **Workflows**: ✅ Configured
  - publish.yml: Multi-OS testing + npm/PyPI publish
  - ci.yml: Continuous integration (on push/PR)
  - Triggers: On tag push (v*)

---

## 🐛 Troubleshooting

### npm Publish Fails

**Error**: `ENEEDAUTH` or `EAUTHUNKNOWN`
```bash
# Re-login to npm
npm logout
npm login
npm publish
```

**Error**: `Package name already taken`
```bash
# Use scoped package
# Update package.json: "name": "@anya-org/conxius_orbit"
npm publish --access public
```

### PyPI Publish Fails

**Error**: `403 Invalid or non-existent authentication`
```bash
# Check token is correct
# Recreate token on PyPI
# Update GitHub secret
```

**Error**: `Package already exists`
```bash
# Bump version in setup.py and package.json
# Commit changes
# Create new tag: v1.0.1
git tag -a v1.0.1 -m "Version 1.0.1"
git push origin v1.0.1
```

### GitHub Actions Fails

**Check logs**:
1. Go to https://github.com/Conxian/conxius_orbit/actions
2. Click on failed workflow run
3. Review error messages
4. Fix issues and re-run

**Common issues**:
- Missing secrets (NPM_TOKEN or PYPI_API_TOKEN)
- Test failures (check test output)
- Build errors (check Python/Node versions)

---

## 📚 Additional Resources

- **npm Documentation**: https://docs.npmjs.com/
- **PyPI Documentation**: https://packaging.python.org/
- **GitHub Actions**: https://docs.github.com/en/actions
- **ConxiusOrbit README**: https://github.com/Conxian/conxius_orbit#readme

---

## 🎉 Success Criteria

Your package is successfully published when:

1. ✅ npm package visible at npmjs.com
2. ✅ PyPI package visible at pypi.org
3. ✅ GitHub release created
4. ✅ `npm install -g conxius_orbit` works
5. ✅ `pip install conxius_orbit` works
6. ✅ `conxius_orbit` command launches GUI
7. ✅ All CI/CD tests pass

---

## 📞 Support

If you encounter issues:
- 📖 Check documentation: https://conxian.github.io/conxius_orbit/
- 🐛 Open issue: https://github.com/Conxian/conxius_orbit/issues
- 💬 Discussions: https://github.com/Conxian/conxius_orbit/discussions

---

**Ready to publish!** 🚀

Once tokens are configured, GitHub Actions will automatically publish on the next tag push or you can publish manually using the commands above.
