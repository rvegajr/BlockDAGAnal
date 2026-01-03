require("@nomicfoundation/hardhat-toolbox");
require("@nomicfoundation/hardhat-verify");

/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: {
    version: "0.8.24",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200,
      },
    },
  },
  networks: {
    hardhat: {
      chainId: 1337,
    },
    phoenixTestnet: {
      url: process.env.PHOENIX_TESTNET_RPC || "https://testnet-rpc.bdp.network",
      chainId: 8888,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
    phoenix: {
      url: process.env.PHOENIX_MAINNET_RPC || "https://rpc.bdp.network",
      chainId: 888,
      accounts: process.env.PRIVATE_KEY ? [process.env.PRIVATE_KEY] : [],
    },
  },
  etherscan: {
    apiKey: {
      phoenixTestnet: process.env.PHOENIX_TESTNET_API_KEY || "",
      phoenix: process.env.PHOENIX_MAINNET_API_KEY || "",
    },
    customChains: [
      {
        network: "phoenixTestnet",
        chainId: 8888,
        urls: {
          apiURL: "https://testnet-explorer.bdp.network/api",
          browserURL: "https://testnet-explorer.bdp.network",
        },
      },
      {
        network: "phoenix",
        chainId: 888,
        urls: {
          apiURL: "https://explorer.bdp.network/api",
          browserURL: "https://explorer.bdp.network",
        },
      },
    ],
  },
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts",
  },
};

