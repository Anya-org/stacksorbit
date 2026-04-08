import { describe, expect, it } from "vitest";
import { Cl } from "@stacks/transactions";

const accounts = simnet.getAccounts();
const deployer = accounts.get("deployer")!;
// Clarinet's simnet accounts map currently aliases `wallet_1` to `deployer`, so we use a
// deterministic external principal to exercise non-admin authorization paths.
const nonAdminPrincipal = "ST2QH59X7AMWTNQVGBQ8D43HK06GTZ6VVNZMDRGT6";

describe("Conxian Systemic Alignment", () => {
  it("revenue-automation: should calculate 1% fee correctly", () => {
    const amount = 1000000n; // 1 STX
    const initialBalance = amount * 2n;
    simnet.mintSTX(deployer, initialBalance);

    const protocolWallet = Cl.contractPrincipal(deployer, "revenue-automation");
    const setWallet = simnet.callPublicFn(
      "revenue-automation",
      "set-protocol-wallet",
      [protocolWallet],
      deployer
    );
    expect(setWallet.result).toBeOk(Cl.bool(true));

    const result = simnet.callPublicFn(
      "revenue-automation",
      "process-revenue-stx",
      [Cl.uint(amount), protocolWallet],
      deployer
    );

    expect(result.result).toBeOk(
      Cl.tuple({
        fee: Cl.uint(10000n),
        net: Cl.uint(990000n)
      })
    );
  });

  it("revenue-automation: non-admin cannot change protocol wallet or admin", () => {
    const protocolWallet = Cl.contractPrincipal(deployer, "revenue-automation");

    const setWallet = simnet.callPublicFn(
      "revenue-automation",
      "set-protocol-wallet",
      [protocolWallet],
      nonAdminPrincipal
    );
    expect(setWallet.result).toBeErr(Cl.uint(401n));

    const setAdmin = simnet.callPublicFn(
      "revenue-automation",
      "set-contract-admin",
      [Cl.principal(deployer)],
      nonAdminPrincipal
    );
    expect(setAdmin.result).toBeErr(Cl.uint(401n));
  });

  it("revenue-automation: admin can rotate admin principal", () => {
    const promote = simnet.callPublicFn(
      "revenue-automation",
      "set-contract-admin",
      [Cl.principal(nonAdminPrincipal)],
      deployer
    );
    expect(promote.result).toBeOk(Cl.bool(true));

    const protocolWallet = Cl.contractPrincipal(deployer, "revenue-automation");

    const fromOldAdmin = simnet.callPublicFn(
      "revenue-automation",
      "set-protocol-wallet",
      [protocolWallet],
      deployer
    );
    expect(fromOldAdmin.result).toBeErr(Cl.uint(401n));

    const fromNewAdmin = simnet.callPublicFn(
      "revenue-automation",
      "set-protocol-wallet",
      [protocolWallet],
      nonAdminPrincipal
    );
    expect(fromNewAdmin.result).toBeOk(Cl.bool(true));
  });

  it("dlc-orchestrator: should open a DLC contract", () => {
    const dlcId = new Uint8Array(32).fill(1);
    const oracle = deployer;
    const collateral = 1000000n;
    const expiry = 100n;

    const result = simnet.callPublicFn(
      "dlc-orchestrator",
      "open-dlc",
      [Cl.buffer(dlcId), Cl.principal(oracle), Cl.uint(collateral), Cl.uint(expiry)],
      deployer
    );

    expect(result.result).toBeOk(Cl.bool(true));

    const status = simnet.callReadOnlyFn(
      "dlc-orchestrator",
      "get-dlc-status",
      [Cl.buffer(dlcId)],
      deployer
    );

    expect(status.result).toBeSome(
      Cl.tuple({
        oracle: Cl.principal(oracle),
        collateral: Cl.uint(collateral),
        status: Cl.stringAscii("OPEN"),
        expiry: Cl.uint(expiry)
      })
    );
  });

  it("dlc-bond: should issue a bond", () => {
    const bondId = 1n;
    const amount = 5000000n;
    const ratio = 150n;

    const result = simnet.callPublicFn(
      "dlc-bond",
      "issue-bond",
      [Cl.uint(bondId), Cl.uint(amount), Cl.uint(ratio)],
      deployer
    );

    expect(result.result).toBeOk(Cl.uint(bondId));
  });
});
