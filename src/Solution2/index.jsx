import { useCallback, useEffect, useRef, useState } from "react";

import HeavyComponent from "./HeavyComponent";

//fix for my example 2
const Solution2 = () => {
  const [input, setInput] = useState("");

  const ref = useRef();

  useEffect(() => {
    ref.current = () => {
      alert(`Hello ${input}`);
    };
  });

  const aFunc = useCallback(() => {
    ref.current();
  }, []);

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

export default Solution2;
