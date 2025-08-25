require("@nomicfoundation/hardhat-toolbox");

// IMPORTANT: Paste the private key from your Ganache account
const GANACHE_PRIVATE_KEY =
  "0x055d7db39fcc3c2e6706af9ed29a0a9abbcaa49311552f3cea7e26525989174f";

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
