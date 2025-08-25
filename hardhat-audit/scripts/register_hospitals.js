const hre = require("hardhat");

// vvvvvvvvvv   YOU MUST EDIT THESE   vvvvvvvvvvvv
const CONTRACT_ADDRESS = "0xb8e563b95b9d8202C9f886C326854588d71D863a";

const HOSPITAL_ADDRESSES = [
    "0x93C77E9573a8b6a1a206E0Ded2cbF76832ac0B65",
    "0x09C015194c1231dE307a3963Cdfe73B7cAAd9787",
    "0x4A9591B4c5E931C7fAc4A5ef58E55148963b685e",
];
// ^^^^^^^^^^^^   YOU MUST EDIT THESE   ^^^^^^^^^^^^

async function main() {
  const auditTrail = await hre.ethers.getContractAt("AuditTrail", CONTRACT_ADDRESS);

  console.log("Registering hospital clients...");

  for (const address of HOSPITAL_ADDRESSES) {
    console.log(` > Registering: ${address}`);
    const tx = await auditTrail.registerHospital(address);
    await tx.wait(); // Wait for the transaction to be mined
    console.log(`   ...Success! Transaction hash: ${tx.hash}`);
  }

  console.log("\n✅ All hospital clients have been registered successfully.");
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});