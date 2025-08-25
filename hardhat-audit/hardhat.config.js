require("@nomicfoundation/hardhat-toolbox");

// IMPORTANT: Paste the private key from your Ganache account
const GANACHE_PRIVATE_KEY =
  "0x3a1766fb90ebf1453a17c6e30f95f658e4c6ac0c5f7b4ba52d090c8a2c6fbc6d";

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.20",
  networks: {
    ganache: {
      url: "http://127.0.0.1:7545",
      accounts: [GANACHE_PRIVATE_KEY],
    },
  },
};
