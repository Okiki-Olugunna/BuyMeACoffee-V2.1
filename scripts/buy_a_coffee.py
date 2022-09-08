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

with open("./contract_data/erc20_abi.json") as file_c:
    a_weth_abi = file_c.read()

a_weth_token = w3.eth.contract(
    address="0x27B4692C93959048833f40702b22FE3578E77759", abi=a_weth_abi
)


def main():
    print("\n------------------------------------------------------------------\n")
    print("------------------------------------------------------------------\n")
    print("\nSTARTING THE BUY_A_COFFEE.PY SCRIPT...\n")
    print("------------------------------------------------------------------\n")
    print("------------------------------------------------------------------\n")

    # initialising the accounts
    print("Initialising the accounts...\n")

    print("Initialising the main account...\n")
    account = config["wallets"]["from_key"]["account"]
    account_address = config["addresses"]["account_address"]

    # people that will donate
    print("Initialising donor 1...\n")
    donor_1 = config["wallets"]["from_key"]["donor_1"]
    donor_1_address = config["addresses"]["donor_1_address"]

    print("Accounts initialised.\n")

    owner_of_contract = contract_instance.functions.owner().call()
    print(f"We will be sending coffee donotions to this person: {owner_of_contract} ")
    print(f"Using their coffee contract address: {contract_address}\n")

    # getting the contract balance with state variable
    contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(
        f"The contract balance is {contract_balance} ether using the public state variable of the contract.\n"
    )

    # getting the contract aWETH token balance
    a_weth_token_balance = a_weth_token.functions.balanceOf(contract_address).call()
    converted_balance = w3.fromWei(a_weth_token_balance, "ether")

    print(
        f"The aWETH balance of the contract (amount in Aave) is: {converted_balance} aWETH\n"
    )

    # sending the first donation
    print(
        "Donor 1 will now buy a coffee for the owner of the contract with a small amount of ETH...\n"
    )

    donation_amount = w3.toWei("0.001", "ether")

    # getting the nonce
    nonce = w3.eth.get_transaction_count(donor_1_address)
    # building the transaction
    tx = contract_instance.functions.buyCoffeeWithETH(
        "Donor 1", "Thanks for your hard work."
    ).buildTransaction(
        {
            "gasPrice": w3.eth.gas_price,
            "chainId": 5,
            "from": donor_1_address,
            "value": donation_amount,
            "nonce": nonce,
        }
    )

    # signing and sending the transaction
    signed_tx = w3.eth.account.sign_transaction(tx, donor_1)
    send_tx = w3.eth.send_raw_transaction(signed_tx.rawTransaction)

    print("Waiting for the transaction to go through...\n")
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    print("--------------------------------------------")
    print(f"Transaction Receipt:\n{tx_receipt}")
    print("--------------------------------------------\n")

    converted_donation = w3.fromWei(donation_amount, "ether")
    print(f"Donor 1 just bought a coffee with the value of {converted_donation} ETH \n")

    # getting the new contract balance with state variable
    contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )
    print(
        f"The new contract balance is {contract_balance} ETH using the public state variable of the contract.\n"
    )

    # getting the contract aWETH token balance
    a_weth_token_balance = a_weth_token.functions.balanceOf(contract_address).call()
    converted_balance = w3.fromWei(a_weth_token_balance, "ether")

    print(
        f"The new aWETH balance of the contract (amount in Aave) is: {converted_balance} aWETH\n"
    )
