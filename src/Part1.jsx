import React, { useEffect } from "react";

const Part1 = ({ aFunc }) => {
  useEffect(() => {
    // console.log("here the function is running");
    aFunc();
  }, [aFunc]);

  useEffect(() => {
    console.log("Re-rendered");
  }, []);

  return (
    <div
      style={{
        height: "200px",
        width: "200px",
        margin: "auto",
        marginTop: "40px",
        backgroundColor: "Red",
      }}
    >
      <div
        onClick={() => {
          aFunc();
        }}
      >
        Click me
      </div>
    </div>
  );
};

export default React.memo(Part1);
