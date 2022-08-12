from brownie import accounts, BuyMeACoffee, exceptions

# from eth_utils import from_wei
from web3 import Web3
import pytest

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))


def test_cannot_send_0_ether():
    owner, tipper_1 = accounts[0], accounts[1]
    contract = BuyMeACoffee.deploy({"from": owner})
    print(f"The owner of this contract is: {owner.address}")

    # tipping 0 ether
    print(f"tipper_1 is attempting to buy a coffee with 0 ether...")

    with pytest.raises(exceptions.VirtualMachineError):
        contract.buyCoffee(
            "tipper_1",
            "thanks for your hard work",
            {"from": tipper_1, "value": 0},
        )

    print("Cannot buy coffee with 0 ether. Value of tip must be greater than 0")
    print("-----------------------------------")
