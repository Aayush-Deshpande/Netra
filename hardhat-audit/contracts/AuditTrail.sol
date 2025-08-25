// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

/**
 * @title AuditTrail
 * @dev This contract acts as a digital notary to log model update hashes
 * from registered participants in a federated learning system.
 */
contract AuditTrail {
    // The address of the contract administrator (deployer)
    address public owner;

    // A list of approved addresses (hospitals)
    mapping(address => bool) public registeredHospitals;

    // An event that is logged to the blockchain on each update
    event UpdateRecorded(
        uint256 indexed round,
        address indexed hospital,
        bytes32 updateHash
    );

    // Modifier to restrict a function to only the owner
    modifier onlyOwner() {
        require(msg.sender == owner, "Only the owner can call this function");
        _;
    }

    // Modifier to restrict a function to registered hospitals
    modifier onlyRegistered() {
        require(registeredHospitals[msg.sender], "Not a registered hospital");
        _;
    }

    // This function runs once when the contract is deployed
    constructor() {
        owner = msg.sender;
    }

    /**
     * @dev Allows the owner to add a new hospital to the approved list.
     * @param _hospitalAddress The blockchain address of the hospital to register.
     */
    function registerHospital(address _hospitalAddress) public onlyOwner {
        registeredHospitals[_hospitalAddress] = true;
    }

    /**
     * @dev Allows a registered hospital to record the hash of its model update.
     * @param _round The federated learning round number.
     * @param _updateHash The 32-byte hash of the model update.
     */
    function recordUpdate(uint256 _round, bytes32 _updateHash) public onlyRegistered {
        emit UpdateRecorded(_round, msg.sender, _updateHash);
    }
}