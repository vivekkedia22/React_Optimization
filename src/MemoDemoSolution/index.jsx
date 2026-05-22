import { useCallback, useMemo, useState } from "react";

import HeavyComponent from "./HeavyComponent";

const MemoDemoSolution = () => {
  const [state, setState] = useState(true);

  const aFunc = useCallback(() => {
    alert("Hello world");
  }, []);

  const { name } = useMemo(() => ({ name: { firstName: "Vivek" } }), []);

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
      <HeavyComponent aFunc={aFunc} name={name} />
    </div>
  );
};

export default MemoDemoSolution;
