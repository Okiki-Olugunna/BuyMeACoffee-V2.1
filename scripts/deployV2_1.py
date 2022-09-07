from brownie import BuyMeACoffeeV2_1, accounts, config
import json


def deploy():
    account = accounts.add(config["wallets"]["from_key"])

    print("Deploying BuyMeACoffeeV2_1 contract ...\n")
    contract = BuyMeACoffeeV2_1.deploy({"from": account})
    print(f"Contract deployed to: {contract.address}\n")

    print("Updating the abi file in the frontend...")

    abi = contract.abi
    json_object = json.dumps(abi)
    with open("./frontend/my-app/utils/V2_1_abi.json", "w") as file:
        file.write(json_object)

    print("Successfully updated the ABI.\n")

    print("Updating the contract address file in the frontend...\n")
    
    address = contract.address
    with open("./frontend/my-app/utils/address.txt", "w") as file:
        file.write(address)

    print("Successfully updated the contract address.\n")

    print("The deployed contract is ready to be interacted with. :) \n")


def main():
    deploy()
    

# deployed at 0xE9D3AB08080d797DC6856fC476e2b9BcD778Af84
