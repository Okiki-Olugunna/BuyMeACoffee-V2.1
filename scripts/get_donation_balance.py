from brownie import accounts, config
from web3 import Web3


w3 = Web3(Web3.HTTPProvider(config["provider"]["http"]))

with open("./contract_data/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


with open("./contract_data/erc20_abi.json") as file_c:
    a_weth_abi = file_c.read()

# initialising the weth aToken
a_weth_token = w3.eth.contract(
    address="0x27B4692C93959048833f40702b22FE3578E77759", abi=a_weth_abi
)


def main():
    # initialising my account
    account = config["wallets"]["from_key"]["account"]
    account_address = config["addresses"]["account_address"]

    print(f"The coffee contract address is {contract_instance.address}\n")

    # getting the contract balance with state variable
    contract_balance = from_wei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(f"The contract balance is {contract_balance} ether.\n")

    # getting the contract aWETH token balance
    a_weth_token_balance = a_weth_token.functions.balanceOf(contract_address).call()
    converted_balance = w3.fromWei(a_weth_token_balance, "ether")

    print(f"The aWETH balance of the contract is: {converted_balance} aWETH\n")
    
