from brownie import accounts, BuyMeACoffee, exceptions
from eth_utils import from_wei
from web3 import Web3
import pytest


def test_change_owner():
    owner, tipper_1, new_owner = accounts[0], accounts[1], accounts[2]
    contract = BuyMeACoffee.deploy({"from": owner})
    print(f"The owner of this contract is: {owner.address}")

    # attempting to fraudulently change the owner
    with pytest.raises(exceptions.VirtualMachineError):
        contract.changeOwner(tipper_1, {"from": tipper_1})

    print("Access denied")

    # successfully changing the owner
    tx = contract.changeOwner(new_owner, {"from": owner})
    tx.wait(1)
    assert contract.owner() == new_owner
