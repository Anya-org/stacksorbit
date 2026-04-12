import { describe, expect, it } from "vitest";
import { Cl } from "@stacks/transactions";

const accounts = simnet.getAccounts();
const deployer = accounts.get("deployer")!;
// The simnet manifest defines only one standard account, so use contract principals
// as distinct principals to exercise `stx-transfer?` behavior.
const protocolWallet = Cl.contractPrincipal(deployer, "dlc-bond");
const recipient = Cl.contractPrincipal(deployer, "dlc-orchestrator");

describe("Conxian Systemic Alignment", () => {
  it("revenue-automation: should calculate 1% fee correctly", () => {
    const amount = 1000000n; // 1 STX
    simnet.mintSTX(deployer, amount);

    const setProtocolWallet = simnet.callPublicFn(
      "revenue-automation",
      "set-protocol-wallet",
      [protocolWallet],
      deployer
    );

    expect(setProtocolWallet.result).toBeOk(Cl.bool(true));

    const { value: storedProtocolWallet } = simnet.getDataVar(
      "revenue-automation",
      "protocol-wallet"
    ) as any;
    expect(storedProtocolWallet).toEqual(`${deployer}.dlc-bond`);

    const result = simnet.callPublicFn(
      "revenue-automation",
      "process-revenue-stx",
      [Cl.uint(amount), recipient],
      deployer
    );

    expect(result.result).toBeOk(
      Cl.tuple({
        fee: Cl.uint(10000n),
        net: Cl.uint(990000n)
      })
    );
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
