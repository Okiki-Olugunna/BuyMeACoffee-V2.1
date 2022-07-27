// SPDX-License-Identifier: MIT

pragma solidity ^0.8.0;

contract BuyMeACoffee {
    address payable public owner;

    address[] public kindPeople;

    event NewCoffeeBought(
        uint256 _datetime,
        address indexed _tipper,
        string _name,
        uint256 _amount,
        string _message
    );

    event WithdrawnCoffees(uint256 _datetime, uint256 _amount);

    modifier onlyOwner() {
        require(msg.sender == owner, "You are not the owner.");
        _;
    }

    constructor() {
        owner = payable(msg.sender);
    }

    // function for others to send donation/tip
    function buyCoffee(string calldata _name, string calldata _message)
        external
        payable
    {
        kindPeople.push(msg.sender);

        emit NewCoffeeBought(
            block.timestamp,
            msg.sender,
            _name,
            msg.value,
            _message
        );
    }

    // function to check how many people tipped
    function howMany() external view returns (uint256) {
        return kindPeople.length;
    }

    // function to check balance of tips
    function checkBalance() external view onlyOwner returns (uint256) {
        return address(this).balance;
    }

    // function to withdraw all tips
    function withdraw() external onlyOwner {
        uint256 balance = address(this).balance;
        payable(msg.sender).transfer(balance);
        emit WithdrawnCoffees(block.timestamp, balance);
    }

    // function to change address of owner
    function changeOwner(address _newOwner) external onlyOwner {
        owner = payable(_newOwner);
    }
}
