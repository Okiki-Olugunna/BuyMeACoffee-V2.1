// SPDX-License-Identifier: MIT

pragma solidity 0.8.12;

import "../interfaces/IERC20.sol";
import "../interfaces/IPool.sol";
import "../interfaces/IWETHGateway.sol";
import "../interfaces/AggregatorV3Interface.sol";

/**
 * @title BuymeAcoffee-V2.1
 * @author Okiki Olugunna
 * @notice This contract acts as a platform for a creator to receive donations from
 * fans or, other words, allow their supporter to buy them a coffee.
 * @notice When someone buys a coffee, the funds (ETH) are supplied to Aave V3 to earn
 * interest. The owner can withdraw these donations at any time.
 * @dev This contract is intended for the Goerli Testnet
 * @dev The deployed contract address is 0xE9D3AB08080d797DC6856fC476e2b9BcD778Af84
 */
contract BuyMeACoffeeV2_1 {
    /**
     * @notice This is the owner of the contract
     * @dev The owner is the deployer of the contract
     */
    address payable public owner;

    /**
     * @notice This is the contract address of the Aave V3 Pool on Goerli
     * (Pool-Proxy-Aave)
     */
    IPool public constant AAVE_V3_POOL =
        IPool(0x368EedF3f56ad10b9bC57eed4Dac65B26Bb667f6);

    /**
     * @notice This is the contract address of the WETH Gateway on Goerli
     * @dev This is where the ETH sent to the buyCoffeeWithETH() function goes through to get to the Pool
     */
    IWETHGateway public constant WETH_GATEWAY =
        IWETHGateway(0xd5B55D3Ed89FDa19124ceB5baB620328287b915d);

    /**
     * @notice This is the contract address of the WETH 'a' token on Aave V3 (Goerli)
     * @dev The ETH sent to Aave V3 via the WETH Gateway accrues interest in the form of 'aWETH'
     */
    IERC20 public constant WETH_ATOKEN =
        IERC20(0x27B4692C93959048833f40702b22FE3578E77759);

    /// @notice This mapping stores the addresses of the people who donated
    mapping(address => bool) public isKind;

    /**
     * @notice This array stores addresses of the people donated
     * @dev This array is used in the howMany() function to count the number of donors
     */
    address[] public kindPeople;

    /// @notice This state variable stores the amount of donations sent to the contract
    uint256 public ETHDonations;

    /**
     * @notice This event gets triggered each time a donation is made
     * @param _datetime The unix timestamp of the donation
     * @param _tipper The address of the donor
     * @param _name The name of the donor
     * @param _amount The amount donated in wei
     * @param _message The message sent with the donation
     */
    event NewCoffeeBought(
        uint256 _datetime,
        address indexed _tipper,
        string _name,
        uint256 _amount,
        string _message
    );

    /**
     * @notice This event gets triggered when donations are withdrawn from contract
     * @param _datetime The unix timestamp of the withdrawal
     * @param _amount The amount withdrawn in wei
     */
    event WithdrawnCoffees(uint256 _datetime, uint256 _amount);

    /// @dev Only the owner of the contract can call functions marked by this modifier
    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner.");
        _;
    }

    /// @dev constructor to initialise the owner
    constructor() {
        owner = payable(msg.sender);
    }

    /**
     * @notice This function allows supporter to "buy a coffee" with ETH
     * @param _name The name of the donor
     * @param _message The message they would like the contract owner to see
     */
    function buyCoffeeWithETH(string calldata _name, string calldata _message)
        external
        payable
    {
        require(msg.value > 0, "Value must be greater than 0.");
        // updating total ETH donations
        ETHDonations += msg.value;

        // transferring eth to aave
        WETH_GATEWAY.depositETH{value: msg.value}(
            address(AAVE_V3_POOL),
            address(this),
            0
        );

        // if statement for first time donors
        if (!isKind[msg.sender]) {
            // updating mapping to true for msg.sender
            isKind[msg.sender] = true;
            // adding msg.sender to kindPeople array
            kindPeople.push(msg.sender);
        }

        // emitting event
        emit NewCoffeeBought(
            block.timestamp,
            msg.sender,
            _name,
            msg.value,
            _message
        );
    }

    /**
     * @notice This function checks how many unique addresses have bought a coffee
     * @return uint256 The value returned is the number of unique addresses who have donated
     */
    function howMany() external view returns (uint256) {
        return kindPeople.length;
    }

    /**
     * @notice This function checks the balance of ETH + aWETH
     * @dev This function is not used on the frontend
     */
    function checkBalanceETH() external view onlyOwner returns (uint256) {
        return address(this).balance + WETH_ATOKEN.balanceOf(address(this));
    }

    /**
     * @notice This function allows the owner to withdraw the ETH donations
     * that have gained interest from Aave
     */
    function withdrawETHAave() external onlyOwner {
        // making sure there is something to withdraw
        require(ETHDonations > 0, "Nothing to withdraw");
        // updating the state variable
        ETHDonations = 0;

        // calculating the amount of aWETH earned
        uint256 aWETHBalance = WETH_ATOKEN.balanceOf(address(this));

        // approving the gateway to spend the aWETH
        WETH_ATOKEN.approve(address(WETH_GATEWAY), aWETHBalance);

        // withdrawing the interest and ETH + sending it to the owner
        WETH_GATEWAY.withdrawETH(
            address(AAVE_V3_POOL),
            type(uint256).max,
            owner
        );

        // emitting event
        emit WithdrawnCoffees(block.timestamp, aWETHBalance);
    }

    /**
     * @notice This function allows the owner to change address of owner address of
     * the contract
     * @param _newOwner The address of the new owner
     */
    function changeOwner(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "Cannot be a 0 address");
        owner = payable(_newOwner);
    }
}
