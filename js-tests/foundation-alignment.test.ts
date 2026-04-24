import { describe, expect, it } from 'vitest';
import { Cl } from '@stacks/transactions';

const accounts = simnet.getAccounts();
const deployer = accounts.get('deployer')!;

describe('Foundation Alignment Test', () => {
  it('verifies revenue-automation fee-bps is initialized', async () => {
    const { result } = await simnet.callReadOnlyFn(
      'revenue-automation',
      'get-fee-bps',
      [],
      deployer
    );
    expect(result).toEqual(Cl.ok(Cl.uint(100)));
  });

  it('verifies dlc-orchestrator can open a DLC', async () => {
    const dlcId = new Uint8Array(32).fill(1);
    const { result } = await simnet.callPublicFn(
      'dlc-orchestrator',
      'open-dlc',
      [
        Cl.buffer(dlcId),
        Cl.principal(deployer),
        Cl.uint(1000000),
        Cl.uint(1000)
      ],
      deployer
    );
    expect(result).toEqual(Cl.ok(Cl.bool(true)));
  });
});
