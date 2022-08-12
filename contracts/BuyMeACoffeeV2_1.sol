// SPDX-License-Identifier: MIT

pragma solidity 0.8.12;

import "../interfaces/IERC20.sol";
import "../interfaces/IPool.sol";
import "../interfaces/IWETHGateway.sol";
import "../interfaces/AggregatorV3Interface.sol";

// deployed address: 0xE9D3AB08080d797DC6856fC476e2b9BcD778Af84
// Goerli Testnet Contract
contract BuyMeACoffeeV2_1 {
    // owner
    address payable public owner;

    // AAVE Pool Address - Goerli (Pool-Proxy-Aave)
    IPool public constant AAVE_V3_POOL =
        IPool(0x368EedF3f56ad10b9bC57eed4Dac65B26Bb667f6);
    // AAVE WETH Gateway Address - Goerli
    IWETHGateway public constant WETH_GATEWAY =
        IWETHGateway(0xd5B55D3Ed89FDa19124ceB5baB620328287b915d);

    IERC20 public constant WETH_ATOKEN =
        IERC20(0x27B4692C93959048833f40702b22FE3578E77759);

    // Chainlink Goerli Price Feed
    //AggregatorV3Interface public constant ETHUSD_PRICE_FEED = AggregatorV3Interface(0x);

    // Aave Goerli Oracle - returns the price of the underlying asset in the base currency
    //address constant AAVE_ORACLE = 0x5bed0810073cc9f0DacF73C648202249E87eF6cB;

    // mapping of people who donated
    mapping(address => bool) public isKind;
    // array of people who donated
    address[] public kindPeople;

    // donations
    uint256 public ETHDonations;

    // event for each time a donation is made
    event NewCoffeeBought(
        uint256 _datetime,
        address indexed _tipper,
        string _name,
        uint256 _amount,
        string _message
    );

    // event for when donations are withdrawn from contract
    event WithdrawnCoffees(uint256 _datetime, uint256 _amount);

    // modifier to prevent others from executing certain functions
    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner.");
        _;
    }

    // initialising the owner
    constructor() {
        owner = payable(msg.sender);
    }

    // buy coffee with ETH
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

    // check how many people tipped
    function howMany() external view returns (uint256) {
        return kindPeople.length;
    }

    // check balance of ETH + aWETH
    function checkBalanceETH() external view onlyOwner returns (uint256) {
        return address(this).balance + WETH_ATOKEN.balanceOf(address(this));

        // could also return the usd balance using convert function with chainlink data feeds
    }

    // withdraw ETH
    function withdrawETHAave() external onlyOwner {
        // making sure there is something to withdraw
        require(ETHDonations > 0, "Nothing to withdraw");
        // updating the state variable
        ETHDonations = 0;

        // calculating total that will be withdrawn
        // uint256 amountWithdrawing = address(this).balance + WETH_ATOKEN.balanceOf(address(this));

        // calculating the amount of aWETH earned
        uint256 aWETHBalance = WETH_ATOKEN.balanceOf(address(this));
        // approving the gateway to spend the aWETH
        WETH_ATOKEN.approve(address(AAVE_V3_POOL), aWETHBalance);

        // withdrawing the interest and ETH
        WETH_GATEWAY.withdrawETH(
            address(AAVE_V3_POOL),
            type(uint256).max,
            //aWETHBalance,
            address(this)
        );

        //sending balance to owner
        owner.transfer(address(this).balance);

        // emitting event
        emit WithdrawnCoffees(block.timestamp, aWETHBalance);
    }

    // change address of owner
    function changeOwner(address _newOwner) external onlyOwner {
        require(_newOwner != address(0), "Cannot be a 0 address");
        owner = payable(_newOwner);
    }

    /*** Chainlink Data Feeds interaction - Goerli testnet 
    // functions to interact with chainlink data feed
    // converting the amount of ETH to USD
    function getConversionRate(uint256 ethAmount)
        public
        view
        returns (uint256)
    {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethPrice * ethAmount) / 1e18;
        return ethAmountInUSD;
    }

    // function to get the price of the ETH
    function getPrice() public view returns (uint256) {
        (, int256 price, , , ) = ETHUSD_PRICE_FEED.latestRoundData();
        // converting to wei
        return uint256(price * 1e10);
    }
    ***/
}
