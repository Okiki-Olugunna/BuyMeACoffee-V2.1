from brownie import config
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

a_weth_token = w3.eth.contract(
    address="0x27B4692C93959048833f40702b22FE3578E77759", abi=a_weth_abi
)


def test_can_buy_coffees():
    # initialising the accounts

    account = config["wallets"]["from_key"]["account"]
    account_address = config["addresses"]["account_address"]

    # people that will donate
    donor_1 = config["wallets"]["from_key"]["donor_1"]
    donor_1_address = config["addresses"]["donor_1_address"]

    print("Initialising donor 2...\n")
    donor_2 = config["wallets"]["from_key"]["donor_2"]
    donor_2_address = config["addresses"]["donor_2_address"]

    # getting the contract balance with state variable
    initial_contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )

    # getting the contract aWETH token balance
    initial_a_weth_token_balance = a_weth_token.functions.balanceOf(
        contract_address
    ).call()
    initial_converted_balance = w3.fromWei(initial_a_weth_token_balance, "ether")

    # buying a coffee
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

    # Waiting for the transaction to go through...
    tx_receipt = w3.eth.wait_for_transaction_receipt(send_tx)

    # getting the new contract balance with state variable
    final_contract_balance = w3.fromWei(
        contract_instance.functions.ETHDonations().call(), "ether"
    )

    # getting the contract aWETH token balance
    final_a_weth_token_balance = a_weth_token.functions.balanceOf(
        contract_address
    ).call()
    final_converted_balance = w3.fromWei(final_a_weth_token_balance, "ether")

    # assertions
    assert initial_contract_balance < final_contract_balance
    assert initial_a_weth_token_balance < final_a_weth_token_balance
    assert initial_converted_balance < final_converted_balance
