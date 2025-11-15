# StacksOrbit VS Code Extension Proposal

This document outlines a proposal for a Visual Studio Code extension for StacksOrbit. This extension will provide a seamless and integrated experience for developers working with the Stacks blockchain, directly within their favorite editor.

## Features

### 1. Command Palette Integration

All of the core StacksOrbit commands will be accessible directly from the VS Code command palette. This will allow developers to run commands without leaving their editor, streamlining their workflow.

**Proposed Commands:**

*   `StacksOrbit: Run Setup Wizard`
*   `StacksOrbit: Deploy`
*   `StacksOrbit: Monitor`
*   `StacksOrbit: Verify`
*   `StacksOrbit: Dashboard`
*   `StacksOrbit: Diagnose`

### 2. Integrated Dashboard

The new Textual-based dashboard will be displayed in a dedicated webview panel within VS Code. This will provide a rich, interactive experience that is far superior to a simple terminal output.

### 3. Syntax Highlighting

The extension will provide syntax highlighting for Clarity smart contracts (`.clar` files) and `Clarinet.toml` files. This will improve readability and make it easier to write and review code.

### 4. Debugger Integration (Future Goal)

In the future, the extension could be integrated with a Stacks debugger, providing a full-featured debugging experience for smart contracts.

## Implementation Details

*   **Language:** TypeScript
*   **Framework:** VS Code Extension API
*   **Key Dependencies:**
    *   `vscode`: The core VS Code API
    *   `child_process`: For running StacksOrbit commands
    *   `webpack`: For bundling the extension

## Next Steps

1.  Create a new directory for the extension (`vscode-stacksorbit`).
2.  Initialize a new VS Code extension project using `yo code`.
3.  Implement the command palette integration.
4.  Implement the integrated dashboard using a webview.
5.  Implement syntax highlighting for Clarity and `Clarinet.toml` files.
6.  Publish the extension to the Visual Studio Code Marketplace.
