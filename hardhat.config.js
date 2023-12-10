require("dotenv").config();
require("@nomicfoundation/hardhat-toolbox");

const INFURA_API_KEY = process.env.INFURA_API_KEY;
const MUMBAI_PRIVATE_KEY = process.env.MUMBAI_PRIVATE_KEY;

module.exports = {
  solidity: "0.8.20",
  networks: {
    fuji: {
      url: `https://api.avax-test.network/ext/C/rpc`,
      accounts: [MUMBAI_PRIVATE_KEY],
    },
  },
  sourcify: {
    enabled: true,
  },
};

