from brownie import BuyMeACoffeeV2_1, accounts, config


def deploy():
    account = accounts.add(config["wallets"]["from_key"])

    print("Deploying BuyMeACoffeeV2_1 contract ...")
    contract = BuyMeACoffeeV2_1.deploy({"from": account})
    print(f"Contract deployed to: {contract}")
    # print(f"The contract abi: {contract.abi}")


def main():
    deploy()


# deployed at 0xE9D3AB08080d797DC6856fC476e2b9BcD778Af84
