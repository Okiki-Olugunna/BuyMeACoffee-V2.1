import React from "react";

export default function Loading(props) {
  return props.trigger ? (
    <div className="loading">
      <div className="loading-inner">{props.children}</div>
    </div>
  ) : (
    ""
  );
}
