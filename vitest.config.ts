// Copyright (c) 2025 Anya Chain Labs
// This software is released under the MIT License.
// See the LICENSE file in the project root for full license information.

import { defineConfig } from "vitest/config";

/**
 * Vitest configuration for StacksOrbit.
 * Standardized configuration for Clarinet SDK integration.
 * This configuration uses the @stacks/clarinet-sdk/vitest environment
 * to provide native simnet support for Clarity smart contracts.
 */
export default defineConfig(async () => {
  const { vitestSetupFilePath, getClarinetVitestsArgv } = await import(
    "@stacks/clarinet-sdk/vitest"
  );

  return {
    test: {
      environment: "clarinet",
      globals: true,
      pool: "forks",
      isolate: false,
      maxWorkers: 1,
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
