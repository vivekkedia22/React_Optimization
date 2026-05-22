import { useState } from "react";

import HeavyComponent from "./HeavyComponent";

const Problem2 = () => {
  const [input, setInput] = useState("");

  const aFunc = () => {
    alert(`Hello::${input}`);
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
      <input
        value={input}
        onInput={e => {
          setInput(e.target.value);
        }}
      />
      <HeavyComponent aFunc={aFunc} />
    </div>
  );
};

export default Problem2;
