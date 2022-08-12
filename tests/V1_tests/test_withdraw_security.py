from brownie import accounts, BuyMeACoffee, exceptions
from eth_utils import from_wei
from web3 import Web3
import pytest

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def test_withdraw():
    owner, tipper_1 = accounts[0], accounts[1]
    contract = BuyMeACoffee.deploy({"from": owner})
    print(f"The owner of this contract is: {owner.address}")

    # tipping 1 ether
    print(f"tipper_1 is buying a coffee...")
    tx = contract.buyCoffee(
        "tipper_1",
        "thanks for your hard work",
        {"from": tipper_1, "value": 1_0000000000_00000000},
    )
    tx.wait(1)
    print("Coffee has been bought & tipped.")

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")

    # withdrawing tips - not the owner
    owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")
    print("Tipper 1 is attempting withdrawing his tip from the owner..")
    with pytest.raises(exceptions.VirtualMachineError):
        contract.withdraw({"from": tipper_1})

    print("Access denied ")

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")

    print("-----------------------------------")
    print("-----------------------------------")
    print("-----------------------------------")

    # withdrawing tips - correct owner
    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    initial_owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")
    print("Owner is withdrawing tips...")
    tx_3 = contract.withdraw({"from": owner})
    tx_3.wait(1)
    print("Tips have been withdrawn ")
    new_contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    owner_new_balance = from_wei(w3.eth.get_balance(owner.address), "ether")

    assert new_contract_balance == 0
    assert owner_new_balance == (contract_balance + initial_owner_balance)

    contract_balance = from_wei(contract.checkBalance({"from": owner}), "ether")
    owner_balance = from_wei(w3.eth.get_balance(owner.address), "ether")
    print(f"The balance of this contract is: {contract_balance} ether")
    print(f"The balance of the owner's address is: {owner_balance} ether")
