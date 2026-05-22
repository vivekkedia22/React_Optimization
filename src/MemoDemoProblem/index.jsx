import { useState } from "react";

import HeavyComponent from "./HeavyComponent";

const MemoDemoProblem = () => {
  const [state, setState] = useState(true);

  const aFunc = () => {
    alert("Hello World");
  };

  return (
    <div
      className="App"
      style={{
        display: "flex",
        flexDirection: "column",
        width: "100vw",
        height: "100vh",
        gap: "100px",
        alignItems: "center",
      }}
    >
      <button
        onClick={() => {
          setState(prev => !prev);
        }}
      >
        Click me to change state:: {state ? "True" : "False"}
      </button>
      <HeavyComponent aFunc={aFunc} name={{ firstName: "Vivek" }} />
    </div>
  );
};

export default MemoDemoProblem;
