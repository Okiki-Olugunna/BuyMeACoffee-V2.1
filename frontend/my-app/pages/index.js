import abi from "../utils/V2_1_abi.json";
import Popup from "./components/Popup";
import Loading from "./components/Loading";
import { ethers } from "ethers";
import React, { useEffect, useState } from "react";
// import { useDisconnect } from "@thirdweb-dev/react";
import Head from "next/head";
import Image from "next/image";
import styles from "../styles/Home.module.css";

export default function Home() {
  // loading the V2_1 contract data
  const contractAddress = "0xE9D3AB08080d797DC6856fC476e2b9BcD778Af84";
  const contractABI = abi.abi;

  // Component states
  const [currentAccount, setCurrentAccount] = useState(false);
  const [ethAmount, setETHAmount] = useState("");

  const [name, setName] = useState("");
  const [message, setMessage] = useState("");

  const [loading, setLoadingState] = useState(false);
  const [thankYouPopUp, setThankYouPopUp] = useState(false);

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
        setThankYouPopUp(true);
      }
    } catch (error) {
      console.log(error);
    }
  };

  // withdraw donotions - for the owner of contract
  const withdrawCoffees = async () => {
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
        setThankYouPopUp(true);
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
        <Popup trigger={thankYouPopUp} setTrigger={setThankYouPopUp}>
          <h3>Thank you for the donation!</h3>
        </Popup>

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

          {/* Withdraw the coffee donations */}
          {/* <a onClick={withdrawCoffees} className={styles.card}>
            <h2>Withdraw Coffees</h2>
            <p>Reserved for the owner of the contract</p>
          </a> */}
        </div>
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
