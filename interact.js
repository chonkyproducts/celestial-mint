const { ethers } = require("hardhat");
async function main() {
    const PlanetarySignsNFT = await ethers.getContractFactory("PlanetarySignsNFT")

    // Get signer
    const signer = await ethers.getSigner("0x7Ce1b943483668A4725EeF6980c74316B0E4f3D7")

    const contract = PlanetarySignsNFT.attach("0x6A73980ACF596141D36c2daCF73f700C902f4b9F").connect(signer)

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




