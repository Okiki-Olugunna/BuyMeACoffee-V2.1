# can use this withdraw script as an alternative to using the user interface 
from brownie import accounts, config
from web3 import Web3
from eth_utils import from_wei

w3 = Web3(
    Web3.HTTPProvider(
        ""
      # removed my HTTP provider link since I'm pushing to github 
    )
)

contract_address = "0xE43841588D314D6Fe155dB1Fd6F7C9D5b71fAf08"
contract_abi = [
    {
        "inputs": [],
        "stateMutability": "nonpayable",
        "type": "constructor",
        "name": "constructor",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_datetime",
                "type": "uint256",
            },
            {
                "indexed": True,
                "internalType": "address",
                "name": "_tipper",
                "type": "address",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "_name",
                "type": "string",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "string",
                "name": "_message",
                "type": "string",
            },
        ],
        "name": "NewCoffeeBought",
        "type": "event",
    },
    {
        "anonymous": False,
        "inputs": [
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_datetime",
                "type": "uint256",
            },
            {
                "indexed": False,
                "internalType": "uint256",
                "name": "_amount",
                "type": "uint256",
            },
        ],
        "name": "WithdrawnCoffees",
        "type": "event",
    },
    {
        "inputs": [],
        "name": "AAVE_V3_POOL",
        "outputs": [{"internalType": "contract IPool", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "ETHDonations",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "WETH_ATOKEN",
        "outputs": [{"internalType": "contract IERC20", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "WETH_GATEWAY",
        "outputs": [
            {"internalType": "contract IWETHGateway", "name": "", "type": "address"}
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [
            {"internalType": "string", "name": "_name", "type": "string"},
            {"internalType": "string", "name": "_message", "type": "string"},
        ],
        "name": "buyCoffeeWithETH",
        "outputs": [],
        "stateMutability": "payable",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "_newOwner", "type": "address"}],
        "name": "changeOwner",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "checkBalanceETH",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "howMany",
        "outputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "address", "name": "", "type": "address"}],
        "name": "isKind",
        "outputs": [{"internalType": "bool", "name": "", "type": "bool"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [{"internalType": "uint256", "name": "", "type": "uint256"}],
        "name": "kindPeople",
        "outputs": [{"internalType": "address", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "owner",
        "outputs": [{"internalType": "address payable", "name": "", "type": "address"}],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "withdrawETHAave",
        "outputs": [],
        "stateMutability": "nonpayable",
        "type": "function",
    },
]


def main():
    # initialising my account
    account = accounts.add(config["wallets"]["from_key"])

    # intialising the contract
    contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)
    print(f"The coffee contract address is {contract_instance.address}")

    # getting the contract balance
    contract_balance = from_wei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(f"The contract balance is {contract_balance} ether.")

    # checking my balance
    my_balance = from_wei(w3.eth.get_balance(account.address), "ether")
    print(f"Your current balance is {my_balance} ether.")

    # withdrawing
    print("Withdrawing donations + yield...")
    tx = contract_instance.functions.withdrawETHAave().transact(
        {"from": account.address}
    )
    tx.wait(2)
    print("Successfully withdrawn.")

    # checking new balances
    my_balance = from_wei(w3.eth.get_balance(account.address), "ether")
    print(f"Your new balance is {my_balance} ether.")

    new_contract_balance = from_wei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(f"The coffee contract new balance is {new_contract_balance} ether")
