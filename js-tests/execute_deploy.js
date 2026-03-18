const { makeContractDeploy, broadcastTransaction, AnchorMode } = require('@stacks/transactions');
const { STACKS_MAINNET, STACKS_TESTNET, STACKS_DEVNET } = require('@stacks/network');
const fs = require('fs');

async function deploy(contractName, codeBody, privateKey, networkName) {
  try {
    let network;
    if (networkName.toLowerCase() === 'mainnet') network = STACKS_MAINNET;
    else if (networkName.toLowerCase() === 'devnet') network = STACKS_DEVNET;
    else network = STACKS_TESTNET;
    
    const txOptions = {
      contractName,
      codeBody,
      senderKey: privateKey,
      network,
      anchorMode: AnchorMode.Any,
      postConditionMode: 1, // Allow
    };
    
    const transaction = await makeContractDeploy(txOptions);
    const broadcastResponse = await broadcastTransaction({ transaction, network });
    
    if (broadcastResponse.error) {
      return { success: false, error: broadcastResponse.error, reason: broadcastResponse.reason };
    }
    
    return { success: true, txId: broadcastResponse.txid };
  } catch (error) {
    return { success: false, error: error.message };
  }
}

// Check if running from command line
if (require.main === module) {
  const args = process.argv.slice(2);
  if (args.length < 3) {
    console.error('Usage: node execute_deploy.js <contractName> <path> <network>');
    console.error('Note: DEPLOYER_PRIVKEY must be set in environment variables.');
    process.exit(1);
  }
  
  const [contractName, contractPath, networkName] = args;
  
  // 🛡️ Sentinel: Read private key from environment variables to prevent process list leaks.
  const privateKey = process.env.DEPLOYER_PRIVKEY;
  if (!privateKey) {
    console.error(JSON.stringify({
      success: false,
      error: 'Missing DEPLOYER_PRIVKEY environment variable',
      reason: 'security_policy_violation'
    }));
    process.exit(1);
  }

  try {
    const codeBody = fs.readFileSync(contractPath, 'utf8');

    deploy(contractName, codeBody, privateKey, networkName).then(result => {
      console.log(JSON.stringify(result));
      if (!result.success) process.exit(1);
    });
  } catch (err) {
    console.error(JSON.stringify({
      success: false,
      error: `Failed to read contract: ${err.message}`,
      reason: 'file_not_found'
    }));
    process.exit(1);
  }
}

module.exports = { deploy };
