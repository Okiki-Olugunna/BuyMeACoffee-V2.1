# can use this withdraw script as an alternative to using the user interface 
from brownie import accounts, config
from web3 import Web3
from eth_utils import from_wei
from decimal import Decimal


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


def main():
    # initialising my account
    account = config["wallets"]["from_key"]["account"]
    account_address = config["addresses"]["account_address"]

    print(f"The coffee contract address is {contract_instance.address}\n")

    # getting the contract balance
    contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(f"The contract balance is {contract_balance} ether.\n")

    # checking my balance
    my_balance = w3.fromWei(w3.eth.get_balance(account_address), "ether")
    print(f"Your current balance is {my_balance} ether.\n")

    # withdrawing
    print("Withdrawing donations + yield...\n")

    print("Getting the nonce...\n")
    nonce = w3.eth.get_transaction_count(account_address)
    print("Nonce obtained...\n")

    print("Building the transaction...\n")
    tx = contract_instance.functions.withdrawETHAave().buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "gas": 500000,
            "chainId": 5,
            "from": account_address,
            "nonce": nonce,
        }
    )
    print("Transaction built.\n")

    # signing and sending the transaction
    print("Signing the transaction...\n")
    signed_tx = w3.eth.account.sign_transaction(tx, account)

    print("Sending the transaction...\n")
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction receipt...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    print("Successfully withdrawn.")

    # checking new balances
    my_balance = w3.fromWei(w3.eth.get_balance(account_address), "ether")
    print(f"Your new balance is {my_balance} ether.\n")

    new_contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(f"The coffee contract new balance is {new_contract_balance} ether\n")
