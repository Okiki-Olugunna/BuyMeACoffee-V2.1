// if signer is equal to the owner state variable of the contract
// then show the withdraw button on the website
import React from "react";

export default function WithdrawCoffees(props) {
  return props.trigger ? (
    <div className="withdrawcard">
      <div
      //className=""
      >
        {props.children}
      </div>
    </div>
  ) : (
    ""
  );
}
