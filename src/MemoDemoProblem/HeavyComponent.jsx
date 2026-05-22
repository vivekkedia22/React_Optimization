import React, { useEffect } from "react";

const HeavyComponent = ({ aFunc, name: { firstName } }) => {
  useEffect(() => {
    console.log("Heavy Component re-rendered");
    setTimeout(() => {
      console.log("into the world");
    }, 500);
  });

  return (
    <div
      style={{
        height: "200px",
        width: "200px",
        backgroundColor: "Red",
        display: "flex",
        flexDirection: "column",
        gap: "10px",
      }}
    >
      {firstName}
      <button
        onClick={() => {
          aFunc();
        }}
      >
        Click me
      </button>
    </div>
  );
};

export default HeavyComponent;
