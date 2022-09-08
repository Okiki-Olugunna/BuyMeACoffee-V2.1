from brownie import accounts, config
from web3 import Web3
# from eth_utils import from_wei


w3 = Web3(Web3.HTTPProvider(config["provider"]["http"]))

with open("./contract_data/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)


def main():
    # initialising my account
    account = config["wallets"]["from_key"]["account"]
    account_address = config["addresses"]["account_address"]

    print(f"The coffee contract address is {contract_instance.address}\n")

    print("Getting the owner of the contract..\n")

    owner = contract_instance.functions.owner().call({"from": account_address})

    print(f"The owner of the contract is {owner}\n")

    print(f"My address is {account_address}\n")

    if owner == account_address:
        print("You ARE the owner of the contract. \n")
    else:
        print("You are NOT the owner of the contract.\n")
    
