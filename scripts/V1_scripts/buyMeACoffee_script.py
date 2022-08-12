from brownie import accounts, BuyMeACoffee
from eth_utils import from_wei
from web3 import Web3

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def main():
    owner = accounts[0]
    tipper_1, tipper_2, new_owner = accounts[1], accounts[2], accounts[3]

    contract = BuyMeACoffee.deploy({"from": owner})
    print(f"The owner of this contract is: {owner.address}")

    owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")
    print("-----------------------------------")

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print("-----------------------------------")

    # first tip - 1 ether
    print(f"tipper_1 is buying a coffee...")
    tx = contract.buyCoffee(
        "tipper_1",
        "thanks for your hard work",
        {"from": tipper_1, "value": 1_0000000000_00000000},
    )
    tx.wait(1)
    print("coffee has been bought & tipped.")

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print("-----------------------------------")

    # second tip - 5 ether
    print(f"tipper_2 is buying a coffee...")
    tx_2 = contract.buyCoffee(
        "tipper_2",
        "thanks for all you do",
        {"from": tipper_2, "value": 5_0000000000_00000000},
    )
    tx_2.wait(1)
    print("coffee has been bought & tipped.")

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print("-----------------------------------")

    # who gave a tip?
    print("These are the addresses of those who were kind enough to buy you a coffee:")
    for i in range(contract.howMany()):
        print(contract.kindPeople(i))

    print("-----------------------------------")

    # withdrawing tips
    owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")
    print("Owner is withdrawing tips...")
    tx_3 = contract.withdraw({"from": owner})
    tx_3.wait(1)
    print("Tips have been withdrawn ")

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")

    # chnaging the owner
    print("Changing the owner of the buyMeACoffee contract...")
    # contract_owner = contract.owner({"from": owner})
    print(f"Current owner is: {contract.owner()}")
    print(f"The new owner will be: {new_owner.address}")

    tx_4 = contract.changeOwner(new_owner.address, {"from": owner})
    tx_4.wait(1)
    print(f"The new owner is: {contract.owner()}")

    print("------ End of script ------ ")
