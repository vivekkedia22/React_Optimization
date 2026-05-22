import React, { useEffect } from "react";

const HeavyComponent = ({ aFunc }) => {
  useEffect(() => {
    console.log("Re-rendered");
  }, []);

  return (
    <div style={{ height: "200px", width: "200px", backgroundColor: "Red" }}>
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

export default React.memo(HeavyComponent);
