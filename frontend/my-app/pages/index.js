import abi from "../utils/V2_1_abi.json";
import ThankYouPopup from "./components/ThankYouPopup";
import WithdrawPopup from "./components/WithdrawPopup";
import Loading from "./components/Loading";
import { ethers } from "ethers";
import React, { useEffect, useState } from "react";
// import { useDisconnect } from "@thirdweb-dev/react";
import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";
import WithdrawCoffees from "./components/WithdrawCoffees";

export default function Home() {
  // loading the V2_1 contract data
  const contractABI = abi.abi;
  const contractAddress = "0xE43841588D314D6Fe155dB1Fd6F7C9D5b71fAf08";

  // Component states
  const [currentAccount, setCurrentAccount] = useState(false);
  const [ethAmount, setETHAmount] = useState("");

  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const [loading, setLoadingState] = useState(false);
  const [thankYouPopUp, setThankYouPopUp] = useState(false);
  const [withdrawPopUp, setWithdrawPopUp] = useState(false);

  // used to show the withdraw button
  const [ownerAccount, setOwnerAccount] = useState(false);

  // event for input fields
  const onETHAmountChange = (event) => {
    setETHAmount(event.target.value);
  };

  const onNameChange = (event) => {
    setName(event.target.value);
  };

  const onMessageChange = (event) => {
    setMessage(event.target.value);
  };

  // function to connect to metamask
  const connectWallet = async () => {
    console.log("Requesting account...");

    // setOwnerAccount(false);

    // getting the chainid of the current network the user is connected to
    const chainId = await window.ethereum.request({ method: "eth_chainId" });

    if (typeof window.ethereum) {
      console.log("Ethereum wallet detected...");

      if (chainId !== "0x5") {
        // switch their network to Goerli
        await window.ethereum.request({
          method: "wallet_switchEthereumChain",
          params: [{ chainId: "0x5" }],
        });
      }

      try {
        const accounts = await window.ethereum.request({
          method: "eth_requestAccounts",
        });
        console.log(accounts[0]);
        setCurrentAccount(accounts[0]);
      } catch (error) {
        console.log("Error connecting..");
      }
    } else {
      console.log("Please install metamask");
    }

    // check to the see if the wallet address is the owner
    if (ethereum) {
      const provider = new ethers.providers.Web3Provider(ethereum, "any");
      const signer = provider.getSigner();
      const signerAddress = await signer.getAddress();
      console.log(`The signers address is: ${signerAddress}`);

      // loading the contract
      const buyMeACoffeeContract = new ethers.Contract(
        contractAddress,
        contractABI,
        signer
      );

      // loading the owner from the buymeacoffee contract
      // console.log("checking the wallet address..");
      const owner = await buyMeACoffeeContract.owner();
      // console.log(`The owner of the contract is: ${owner}`);

      // if the wallet address is equal to the owner
      if (signerAddress == owner) {
        // show withdraw button
        setOwnerAccount(true);
      }
    }
  };

  const isWalletConnected = async () => {
    if (typeof window.ethereum) {
      try {
        const accounts = await ethereum.request({ method: "eth_accounts" });
        console.log("accounts: ", accounts);

        if (accounts.length > 0) {
          const account = accounts[0];
          console.log("Wallet is connected! " + account);
        } else {
          console.log("Make sure MetaMask is connected");
        }
      } catch (error) {
        console.log("error: ", error);
      }
    }
  };

  // small coffee - 0.01ETH
  const buySmallCoffee = async () => {
    try {
      const { ethereum } = window;

      if (ethereum) {
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        const signer = provider.getSigner();
        const buyMeACoffeeContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );

        console.log("buying coffee..");
        const coffeeTxn = await buyMeACoffeeContract.buyCoffeeWithETH(
          "anon",
          "Enjoy your coffee!",
          { value: ethers.utils.parseEther("0.01") }
        );

        // show loading popup while transaction is being mined
        setLoadingState(true);
        await coffeeTxn.wait();

        console.log("Transaction mined ", coffeeTxn.hash);
        console.log("Coffee purchased!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingState(false);
        // show thank you popup
        setThankYouPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // medium coffee - 0.03ETH
  const buyMediumCoffee = async () => {
    try {
      const { ethereum } = window;

      if (ethereum) {
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        const signer = provider.getSigner();
        const buyMeACoffeeContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );

        console.log("buying coffee..");
        const coffeeTxn = await buyMeACoffeeContract.buyCoffeeWithETH(
          "anon",
          "Enjoy your coffee!",
          { value: ethers.utils.parseEther("0.03") }
        );

        // show loading popup while transaction is being mined
        setLoadingState(true);
        await coffeeTxn.wait();

        console.log("Transaction mined ", coffeeTxn.hash);
        console.log("Coffee purchased!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingState(false);
        // show thank you popup
        setThankYouPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // large coffee - 0.05ETH
  const buyLargeCoffee = async () => {
    try {
      const { ethereum } = window;

      if (ethereum) {
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        const signer = provider.getSigner();
        const buyMeACoffeeContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );

        console.log("buying coffee..");
        const coffeeTxn = await buyMeACoffeeContract.buyCoffeeWithETH(
          "anon",
          "Enjoy your coffee!",
          { value: ethers.utils.parseEther("0.05") }
        );

        // show loading popup while transaction is being mined
        setLoadingState(true);
        await coffeeTxn.wait();

        console.log("Transaction mined ", coffeeTxn.hash);
        console.log("Coffee purchased!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingState(false);
        // show thank you popup
        setThankYouPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // custom amount + name & message
  const buyCustomCoffee = async () => {
    // coffeeAmount = document.getElementById(coffeeAmount);
    //coffeeAmount.preventDefault();

    try {
      const { ethereum } = window;

      if (ethereum) {
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        const signer = provider.getSigner();
        const buyMeACoffeeContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );

        console.log("buying coffee..");
        const coffeeTxn = await buyMeACoffeeContract.buyCoffeeWithETH(
          name,
          message,
          { value: ethers.utils.parseEther(ethAmount) }
        );

        // show loading popup while transaction is being mined
        setLoadingState(true);
        await coffeeTxn.wait();

        console.log("Transaction mined ", coffeeTxn.hash);
        console.log("Coffee purchased!");

        // Clear the form fields.
        setName("");
        setMessage("");

        // remove loading popup
        setLoadingState(false);
        // show thank you popup
        setWithdrawPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // withdraw donotions - for the owner of contract
  const withdrawCoffees = async () => {
    try {
      const { ethereum } = window;

      if (ethereum) {
        const provider = new ethers.providers.Web3Provider(ethereum, "any");
        const signer = provider.getSigner();
        const buyMeACoffeeContract = new ethers.Contract(
          contractAddress,
          contractABI,
          signer
        );

        console.log("withdrawing coffees..");
        const withdrawTxn = await buyMeACoffeeContract.withdrawETHAave();

        // show loading popup while transaction is being mined
        setLoadingState(true);
        await withdrawTxn.wait();

        console.log("Transaction mined ", withdrawTxn.hash);
        console.log("Coffee purchased!");

        // remove loading popup
        setLoadingState(false);
        // show popup
        setWithdrawPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  return (
    <div className={styles.container}>
      <Head>
        <title>Buy Okiki A Coffee</title>
        <meta name="description" content="Give Okiki a tip" />
        <link rel="icon" href="/coffee-cup-removebg.png" />
      </Head>

      <button
        id="connectButton"
        className="connect"
        type="button"
        onClick={connectWallet}
      >
        {!currentAccount ? "Connect Wallet" : "Connected"}
      </button>

      <main className={styles.main}>
        <h1 className={styles.title}>
          Buy Okiki a <a>Coffee!</a>
        </h1>

        <Image
          src={"/coffee-cup-removebg.png"}
          width={405}
          height={336}
          alt="Coffee cup"
        />

        {/* 'loading' pop-up */}
        <center>
          <Loading trigger={loading}>
            <div></div>
          </Loading>
        </center>

        {/* 'thank you' pop-up */}
        <ThankYouPopup trigger={thankYouPopUp} setTrigger={setThankYouPopUp}>
          <h3>Thank you for the donation!</h3>
        </ThankYouPopup>

        {/* 'Withdrawals have been made' pop-up */}
        <WithdrawPopup trigger={withdrawPopUp} setTrigger={setWithdrawPopUp}>
          <h3>All donations have been withdrawn!</h3>
        </WithdrawPopup>

        <div className={styles.grid}>
          <a onClick={buySmallCoffee} className={styles.card}>
            <h2>Small Coffee</h2>
            <p>0.01 ETH</p>
          </a>

          <a onClick={buyMediumCoffee} className={styles.card}>
            <h2>Medium Coffee</h2>
            <p>0.03 ETH</p>
          </a>

          <a onClick={buyLargeCoffee} className={styles.card}>
            <h2>Large Coffee</h2>
            <p>0.05 ETH</p>
          </a>

          <a className={styles.customcard}>
            <h2>Custom Coffee</h2>
            <p>What's your name?</p>
            <p>
              <input
                id="name"
                name="donorName"
                type={"text"}
                placeholder="John Snow"
                onChange={onNameChange}
              ></input>
            </p>

            <p>What would you like to say to Okiki?</p>
            <p>
              <input
                id="message"
                name="donorMessage"
                type={"text"}
                placeholder="You are absolutely amazing!"
                onChange={onMessageChange}
              ></input>
            </p>

            <p>Type an amount:</p>
            <p>
              <input
                id="coffeeAmount"
                name="coffeeAmount"
                type={"text"}
                placeholder="0.5"
                onChange={onETHAmountChange}
              ></input>
            </p>
            <p>
              <button type="submit" onClick={buyCustomCoffee}>
                Buy Coffee
              </button>
            </p>
          </a>
        </div>

        {/* Withdraw the coffee donations */}
        {/* <a onClick={withdrawCoffees} className={styles.withdrawcard}>
          <h2>Withdraw Coffees</h2>
          <p>Reserved for the owner of the contract</p>
        </a> */}

        {/* 'Withdraw Coffees' button*/}
        <WithdrawCoffees
          trigger={ownerAccount}
          setTrigger={setOwnerAccount}
          className={styles.withdrawcard}
        >
          <a onClick={withdrawCoffees}>
            <h2>Withdraw Coffees</h2>
            <p>Click to withdraw all of your donations</p>
          </a>
        </WithdrawCoffees>
      </main>

      <footer>
        Feeling curious? Have a look through my{" "}
        <a
          className="github"
          target="_blank"
          href="https://github.com/Okiki-Olugunna"
        >
          GitHub
        </a>
      </footer>
    </div>
  );
}
