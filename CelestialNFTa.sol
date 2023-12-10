// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

import "@openzeppelin/contracts/token/ERC721/ERC721.sol";
import "@openzeppelin/contracts/token/ERC721/extensions/ERC721URIStorage.sol";
import "@chainlink/contracts/src/v0.8/functions/dev/v1_0_0/FunctionsClient.sol";
import "@chainlink/contracts/src/v0.8/functions/dev/v1_0_0/libraries/FunctionsRequest.sol";
import "@chainlink/contracts/src/v0.8/shared/access/ConfirmedOwner.sol";
import "@openzeppelin/contracts/utils/Strings.sol";
import "./Base64.sol"; 

contract CelestialNFTa is ERC721URIStorage, FunctionsClient, ConfirmedOwner {
    constructor() ERC721("CelestialNFTa", "CST") FunctionsClient(router) ConfirmedOwner(msg.sender) {}
    using FunctionsRequest for FunctionsRequest.Request;
    using Strings for uint256;
   
event ResponseWithImage(
        bytes32 indexed requestId,
        bytes planetarySignsData,
        bytes imageData,
        bytes response,
        bytes err
    );

     // Custom error type
    error UnexpectedRequestID(bytes32 requestId);

    uint256 private tokenIdCounter;

    address router = 0xA9d587a00A31A52Ed70D6026794a8FC5E2F5dCb0;
    uint64 subscriptionId = 1566;

    function requestPlanetarySigns() external returns (bytes32 requestIdPlanetarySigns) {
    // Request Planetary Signs data
    FunctionsRequest.Request memory reqPlanetarySigns;
     string memory source =
        "const apiResponse1 = await Functions.makeHttpRequest({url: 'https://celestialmint.xyz/api/planetary-signs'});" 
        "const apiResponse2 = await Functions.makeHttpRequest({url: 'https://celestialmint.xyz/get-composed-image'});"
        "if (apiResponse1.error || apiResponse2.error) { throw Error('Request failed'); }"
        "return Functions.encodeString([apiResponse1.data, apiResponse2.data]);";
    reqPlanetarySigns.initializeRequestForInlineJavaScript(source);

    // Encode the request to CBOR
    bytes memory requestData = FunctionsRequest.encodeCBOR(reqPlanetarySigns);
    
    //Callback gas limit
    uint32 gasLimit = 300000;

    // donID - Hardcoded for Mumbai
    bytes32 donID =
        0x66756e2d6176616c616e6368652d66756a692d31000000000000000000000000;
  
    // Send the Chainlink request
    requestIdPlanetarySigns = _sendRequest(requestData, subscriptionId, gasLimit, donID);
    return requestIdPlanetarySigns;
}


function fulfillRequest(
    bytes32 requestId,
    bytes memory response,
    bytes memory err
) internal override {
    (bytes memory planetarySignsData, bytes memory imageData) = abi.decode(response, (bytes, bytes));

    emit ResponseWithImage(requestId, planetarySignsData, imageData, response, err);

    // Mint an NFT with metadata
    _mintWithMetadata(planetarySignsData, imageData);
}

function _mintWithMetadata(bytes memory planetarySignsData, bytes memory imageData) private {
        // Convert bytes to Base64 using the Base64 library
        string memory base64PlanetarySignsData = Base64.encode(planetarySignsData);
        string memory base64ImageData = Base64.encode(imageData);

        // Concatenate metadata
        string memory metadata = string(
            abi.encodePacked(
                '{"planetarySignsData": "', base64PlanetarySignsData, '", "imageData": "', base64ImageData, '"}'
            )
        );

        // Mint the NFT
        _safeMint(msg.sender, tokenIdCounter);
        _setTokenURI(tokenIdCounter, metadata);
        tokenIdCounter++;
    }

function getTokenIdCounter() external view returns (uint256) {
        return tokenIdCounter;
    }

    address private withdrawAddress = 0x7Ce1b943483668A4725EeF6980c74316B0E4f3D7;

    // Mapping to store the last minting timestamp for each wallet
    mapping(address => uint256) private lastMintTimestamp;

    // Minimum time between mints (1 day)
    uint256 private constant minTimeBetweenMints = 1 days;

    // Only the specified address can withdraw funds
function withdraw() external {
        require(msg.sender == withdrawAddress, "Only the withdrawal address can call this function");
        uint256 balance = address(this).balance;
        payable(withdrawAddress).transfer(balance);
    }

    // Ensure only one mint per day per wallet
function mintOncePerDay() external {
        require(lastMintTimestamp[msg.sender] + minTimeBetweenMints < block.timestamp, "Can only mint once per day");

        // Update the last mint timestamp for the wallet
        lastMintTimestamp[msg.sender] = block.timestamp;
    }
}