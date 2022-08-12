import React from "react";

export default function Loading(props) {
  return props.trigger ? (
    <div>
      Waiting for the transaction to go through...
      <p></p>
      {/* <center> */}
      <div className="loading">
        <div className="loading-inner">{props.children}</div>
      </div>
      {/* </center> */}
    </div>
  ) : (
    ""
  );
}
