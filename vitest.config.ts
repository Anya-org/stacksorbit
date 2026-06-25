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

  return {
    test: {
      environment: "clarinet",
      globals: true,
      // Use forks+singleFork across platforms; Windows thread workers have been
      // flaky in CI for Clarinet-powered suites.
      pool: "forks",
      forks: {
        singleFork: true,
      },
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
