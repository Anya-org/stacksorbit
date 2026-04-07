import { describe, expect, it } from "vitest";
import { Cl, cvToValue } from "@stacks/transactions";

const accounts = simnet.getAccounts();
const deployer = accounts.get("deployer")!;

describe("Conxian Systemic Alignment", () => {
  it("revenue-automation: should calculate 1% fee correctly", () => {
    const amount = 1000000n; // 1 STX
    const expectedFeeBps = 100n;
    const fee = (amount * expectedFeeBps) / 10000n;
    const net = amount - fee;
    const protocolWalletValue = cvToValue(
      simnet.getDataVar("revenue-automation", "protocol-wallet")
    );
    if (typeof protocolWalletValue !== "string") {
      throw new Error("Invalid protocol-wallet type");
    }
    const protocolWallet = protocolWalletValue;
    const recipient = "ST2NEB84ASENDXKYGJPQW86YXQCEFEX2ZQPG87ND";

    const getStxBalance = (address: string): bigint =>
      simnet.getAssetsMap().get("STX")?.get(address) ?? 0n;

    simnet.mintSTX(deployer, amount);
    const deployerBalanceBefore = getStxBalance(deployer);
    const protocolWalletBalanceBefore = getStxBalance(protocolWallet);
    const recipientBalanceBefore = getStxBalance(recipient);

    const result = simnet.callPublicFn(
      "revenue-automation",
      "process-revenue-stx",
      [Cl.uint(amount), Cl.principal(recipient)],
      deployer
    );

    expect(result.result).toBeOk(
      Cl.tuple({
        fee: Cl.uint(fee),
        net: Cl.uint(net)
      })
    );

    const deployerBalanceAfter = getStxBalance(deployer);
    const protocolWalletBalanceAfter = getStxBalance(protocolWallet);
    const recipientBalanceAfter = getStxBalance(recipient);

    expect(protocolWalletBalanceAfter - protocolWalletBalanceBefore).toBe(fee);
    expect(recipientBalanceAfter - recipientBalanceBefore).toBe(net);
    expect(deployerBalanceBefore - deployerBalanceAfter).toBe(amount);
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
