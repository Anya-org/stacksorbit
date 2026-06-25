// Copyright (c) 2025 Conxian-Labs
// This software is released under the MIT License.
// See the LICENSE file in the project root for full license information.

import { defineConfig } from "vitest/config";

/**
 * Modernized Vitest configuration for Conxius Orbit.
 * Optimized for @stacks/clarinet-sdk ^3.17.0 and Vitest 4.
 * Root-Up synchronized.
 */
export default defineConfig(async () => {
  const { vitestSetupFilePath, getClarinetVitestsArgv } = await import(
    "@stacks/clarinet-sdk/vitest"
  );
  const isWindows = process.platform === "win32";

  return {
    test: {
      environment: "clarinet",
      globals: true,
      pool: isWindows ? "threads" : "forks",
      ...(isWindows
        ? {
            threads: {
              singleThread: true,
            },
          }
        : {
            forks: {
              singleFork: true,
            },
          }),
      setupFiles: [vitestSetupFilePath],
      environmentOptions: {
        clarinet: {
          ...getClarinetVitestsArgv(),
          manifestPath: "./Clarinet.toml",
        },
      },
      include: ["js-tests/**/*.test.ts", "tests/**/*.test.ts"],
    },
  };
});
