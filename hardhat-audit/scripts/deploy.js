const hre = require("hardhat");

async function main() {
  // Get the contract factory for the AuditTrail contract
  const AuditTrail = await hre.ethers.getContractFactory("AuditTrail");

  // Deploy the contract
  const auditTrail = await AuditTrail.deploy();

  // Wait for the deployment to complete
  await auditTrail.waitForDeployment();

  // Log the address of the newly deployed contract
  console.log(`AuditTrail contract deployed to address: ${auditTrail.target}`);
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});