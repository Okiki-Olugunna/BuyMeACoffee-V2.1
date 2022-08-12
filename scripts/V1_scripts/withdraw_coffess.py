from brownie import BuyMeACoffee, accounts, config
from eth_utils import from_wei
from web3 import Web3
import json

w3 = Web3(Web3.HTTPProvider(config(["networks"]["default"])))

# abi = json.loads(open("../build/contracts/BuyMeACoffee.json"))


def main():
    # owner that deployed the original contract
    account = accounts.add(config["wallets"]["from_key"])

    # initialising deployed contract
    contract_address = "0x1E5baaB66B18b2AF7433b13Edf036233d8F35b2f"
    contract_abi = BuyMeACoffee.abi
    contract = w3.eth.contract(contract_address, contract_abi)

    # checking the balance of the contract
    contract_balance = from_wei(contract.checkBalance({"from": account}), "ether")
    print(f"Contract balance is: {contract_balance}")

    # withdrawing tips
    print("Withdrawing tips...")
    tx = contract.withdraw({"from": account})
    tx.wait(1)
    print(f"Tips withdrawn to: {account}")

    # checking the balance of the contract after withdrawing
    contract_balance = from_wei(contract.checkBalance({"from": account}), "ether")
    print(f"Contract balance is: {contract_balance}")
