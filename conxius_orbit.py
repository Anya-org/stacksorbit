#!/usr/bin/env python3
# Copyright (c) 2025 Conxian-Labs
# This software is released under the MIT License.
# See the LICENSE file in the project root for full license information.

"""
ConxiusOrbit - Main Entry Point
Bridges the package to the CLI implementation
"""

import sys
from conxius_orbit_cli import main as cli_main


def main():
    """Main entry point for the conxius_orbit package"""
    return cli_main()


if __name__ == "__main__":
    sys.exit(main())
