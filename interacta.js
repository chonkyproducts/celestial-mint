const { ethers } = require("hardhat");
async function main() {
    const CelestialNFTa = await ethers.getContractFactory("CelestialNFTa")

    // Get signer
    const signer = await ethers.getSigner("0x7Ce1b943483668A4725EeF6980c74316B0E4f3D7")

    const contract = CelestialNFTa.attach("0x0dF208358ee67B1f4211750d01617CbC7B956Fe8").connect(signer)

    // Specify a gas limit
    const gasLimit = 1000000; // Adjust this value as needed

    const res = await contract.requestPlanetarySigns({ gasLimit: gasLimit })

    console.log(res)
}

main()
  .then(() => process.exit(0))
  .catch((error) => {
    console.error(error);
    process.exitCode = 1;
  });
