// scripts/deployAuditTrail.js
const hre = require("hardhat");

async function main() {
  const AuditTrail = await hre.ethers.getContractFactory("AuditTrail");

  console.log("Deploying AuditTrail...");
  const auditTrail = await AuditTrail.deploy();

  // wait until deployment is finished
  await auditTrail.waitForDeployment();

  // for ethers v6 (Hardhat toolbox uses this now)
  console.log("AuditTrail contract deployed to Ganache at address:", await auditTrail.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
