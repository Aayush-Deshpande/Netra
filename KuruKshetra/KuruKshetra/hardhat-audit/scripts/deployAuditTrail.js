const hre = require("hardhat");

async function main() {
  const AuditTrail = await hre.ethers.getContractFactory("AuditTrail");
  const auditTrail = await AuditTrail.deploy();
  await auditTrail.waitForDeployment();
  
  console.log(
    `AuditTrail contract deployed to Ganache at address: ${auditTrail.address}`
  );
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});