from brownie import config, exceptions
from web3 import Web3
import pytest


w3 = Web3(Web3.HTTPProvider(config["provider"]["http"]))

with open("./contract_data/address.txt") as file_a:
    contract_address = file_a.read()

with open("./contract_data/abi.json") as file_b:
    contract_abi = file_b.read()

# initialising the contract instance
contract_instance = w3.eth.contract(address=contract_address, abi=contract_abi)

# getting erc20 token info
with open("./contract_data/erc20_abi.json") as file_c:
    a_weth_abi = file_c.read()

# initialising the aWeth token
a_weth_token = w3.eth.contract(
    address="0x27B4692C93959048833f40702b22FE3578E77759", abi=a_weth_abi
)


def test_can_withdraw_coffees():
    # initialising an account that is not the owner
    hacker = config["wallets"]["from_key"]["donor_2"]
    hacker_address = config["addresses"]["donor_2_address"]

    # getting the contract balance
    initial_contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )

    # checking my balance
    hackers_initial_balance = w3.fromWei(w3.eth.get_balance(hacker_address), "ether")

    # withdrawing
    # Getting the nonce...
    nonce = w3.eth.get_transaction_count(hacker_address)
    # Building the transaction...
    tx = contract_instance.functions.withdrawETHAave().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "gas": 500000,
            "chainId": 5,
            "from": hacker_address,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, hacker)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    # Waiting for the transaction receipt...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # checking new balances
    hackers_new_balance = w3.fromWei(w3.eth.get_balance(hacker_address), "ether")

    new_contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )

    # assertions
    assert hackers_new_balance <= hackers_initial_balance
    assert new_contract_balance >= initial_contract_balance
