#!/usr/bin/env python3
"""Generate a self-contained reveal.js slide deck on React render optimization.

Run:  python3 build_deck.py
Out:  react-optimization.html  (open in any browser; press F for fullscreen)

The deck is built from the four source components in ../src:
  MemoDemoProblem -> MemoDemoSolution   (useCallback / useMemo / React.memo)
  Problem2        -> Solution2          (latest-ref pattern + stable useCallback)
"""

import html
from pathlib import Path

REVEAL = "https://cdn.jsdelivr.net/npm/reveal.js@5.1.0"


def code_block(code: str, highlight: str = "") -> str:
    escaped = html.escape(code.strip("\n"))
    attr = f' data-line-numbers="{highlight}"' if highlight else ""
    return (
        f'<pre><code class="language-jsx" data-trim{attr}>\n'
        f"{escaped}\n"
        f"</code></pre>"
    )


def bullets(items: list[str]) -> str:
    lis = "\n".join(f"<li>{i}</li>" for i in items)
    return f"<ul>\n{lis}\n</ul>"


def split_slide(eyebrow, badge_class, badge_text, title, code, highlight,
                points, result_class, result_text) -> str:
    return f"""
<section>
  <div class="slide-head">
    <span class="eyebrow">{eyebrow}</span>
    <span class="badge {badge_class}">{badge_text}</span>
  </div>
  <h2 class="slide-title">{title}</h2>
  <div class="two-col">
    <div class="col-code">
      {code_block(code, highlight)}
    </div>
    <div class="col-notes">
      {bullets(points)}
      <div class="result {result_class}">{result_text}</div>
    </div>
  </div>
</section>
""".strip()


# ---------------------------------------------------------------- code samples

PROBLEM1 = """
const MemoDemoProblem = () => {
  const [state, setState] = useState(true);

  // new function reference on EVERY render
  const aFunc = () => {
    alert("Hello World");
  };

  return (
    <>
      <button onClick={() => setState(p => !p)}>
        Toggle: {state ? "True" : "False"}
      </button>

      {/* new object literal on EVERY render */}
      <HeavyComponent aFunc={aFunc} name={{ firstName: "Vivek" }} />
    </>
  );
};

// child is NOT memoized
export default HeavyComponent;
"""

SOLUTION1 = """
const MemoDemoSolution = () => {
  const [state, setState] = useState(true);

  // stable function reference
  const aFunc = useCallback(() => {
    alert("Hello world");
  }, []);

  // stable object reference
  const { name } = useMemo(
    () => ({ name: { firstName: "Vivek" } }),
    []
  );

  return (
    <>
      <button onClick={() => setState(p => !p)}>
        Toggle: {state ? "True" : "False"}
      </button>
      <HeavyComponent aFunc={aFunc} name={name} />
    </>
  );
};

// skip re-render when props are referentially equal
export default React.memo(HeavyComponent);
"""

PROBLEM2 = """
const Problem2 = () => {
  const [input, setInput] = useState("");

  // recreated on EVERY keystroke, and it
  // closes over `input`
  const aFunc = () => {
    alert(`Hello::${input}`);
  };

  return (
    <>
      <input
        value={input}
        onInput={e => setInput(e.target.value)}
      />
      <HeavyComponent aFunc={aFunc} />
    </>
  );
};
"""

SOLUTION2 = """
const Solution2 = () => {
  const [input, setInput] = useState("");
  const ref = useRef();

  // runs every render: ref always points
  // at the LATEST closure over `input`
  useEffect(() => {
    ref.current = () => alert(`Hello ${input}`);
  });

  // stable reference, calls latest version
  const aFunc = useCallback(() => ref.current(), []);

  return (
    <>
      <input
        value={input}
        onInput={e => setInput(e.target.value)}
      />
      <HeavyComponent aFunc={aFunc} />
    </>
  );
};

export default React.memo(HeavyComponent);  // child
"""

# ---------------------------------------------------------------------- slides

slides = []

# 1. Title
slides.append("""
<section class="title-slide">
  <h1>Optimizing React</h1>
  <p class="subtitle">Stop unnecessary re-renders with <code>React.memo</code>,
     <code>useCallback</code> &amp; <code>useMemo</code></p>
  <p class="byline">A walk through two real before / after examples</p>
</section>
""".strip())

# 2. Core idea
slides.append("""
<section>
  <h2 class="slide-title">The core idea</h2>
  <div class="concept">
    <p>When a component re-renders, <strong>all of its children re-render too</strong>
       &mdash; even the expensive ones.</p>
    <p><code>React.memo</code> lets a child skip re-rendering <em>when its props
       have not changed</em>.</p>
    <p class="warn">But props are compared by <strong>reference</strong>.
       A fresh <code>{}</code> object or a new arrow function is
       <em>never</em> equal to the previous one &mdash; so <code>memo</code>
       alone is not enough.</p>
  </div>
</section>
""".strip())

# 3. Example 1 - Problem
slides.append(split_slide(
    eyebrow="Example 1 &middot; rendering on state change",
    badge_class="bad", badge_text="Problem",
    title="New props on every render",
    code=PROBLEM1, highlight="5-7|16|20",
    points=[
        "Clicking the button re-renders the parent.",
        "<code>aFunc</code> and <code>{ firstName }</code> are "
        "<strong>created fresh</strong> each render.",
        "Their references change, so the child re-renders too &mdash; "
        "even if wrapped in <code>React.memo</code>.",
    ],
    result_class="bad",
    result_text="Heavy child re-renders on every click",
))

# 4. Example 1 - Solution
slides.append(split_slide(
    eyebrow="Example 1 &middot; rendering on state change",
    badge_class="good", badge_text="Solution",
    title="Stabilise the props, then memoize",
    code=SOLUTION1, highlight="5-7|10-13|24",
    points=[
        "<code>useCallback</code> keeps the function reference stable.",
        "<code>useMemo</code> keeps the object reference stable.",
        "<code>React.memo</code> can now compare props and bail out.",
    ],
    result_class="good",
    result_text="Child renders once; clicks no longer touch it",
))

# 5. Example 2 - Problem
slides.append(split_slide(
    eyebrow="Example 2 &middot; a callback that needs live state",
    badge_class="bad", badge_text="Problem",
    title="The callback depends on changing state",
    code=PROBLEM2, highlight="6-8|14",
    points=[
        "Every keystroke updates <code>input</code> and re-renders the parent.",
        "<code>aFunc</code> must read the latest <code>input</code>, "
        "so it is rebuilt each render.",
        "<code>useCallback(fn, [input])</code> would still change every "
        "keystroke &mdash; <code>memo</code> stays useless.",
    ],
    result_class="bad",
    result_text="Heavy child re-renders on every keystroke",
))

# 6. Example 2 - Solution
slides.append(split_slide(
    eyebrow="Example 2 &middot; a callback that needs live state",
    badge_class="good", badge_text="Solution",
    title="The &ldquo;latest ref&rdquo; pattern",
    code=SOLUTION2, highlight="3|7-9|12",
    points=[
        "A <code>ref</code> always holds the newest closure over <code>input</code>.",
        "<code>aFunc</code> is wrapped once with empty deps &mdash; its "
        "reference never changes.",
        "It forwards to <code>ref.current()</code>, so the button still "
        "sees the live value.",
    ],
    result_class="good",
    result_text="Stable prop + live data: child never re-renders",
))

# 7. Takeaways
slides.append("""
<section>
  <h2 class="slide-title">Takeaways</h2>
  <ul class="takeaways">
    <li><code>React.memo</code> only helps when <strong>prop references are stable</strong>.</li>
    <li>Wrap callbacks in <code>useCallback</code> and objects/arrays in <code>useMemo</code> before passing them to a memoized child.</li>
    <li>When a stable callback still needs fresh state, store the closure in a <strong>ref</strong> and expose a one-time <code>useCallback</code> wrapper.</li>
    <li>Measure first &mdash; reach for these only on components that are genuinely expensive to render.</li>
  </ul>
</section>
""".strip())

slides_html = "\n\n".join(slides)

HTML = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Optimizing React</title>
  <link rel="stylesheet" href="{REVEAL}/dist/reveal.css" />
  <link rel="stylesheet" href="{REVEAL}/dist/theme/black.css" id="theme" />
  <link rel="stylesheet" href="{REVEAL}/plugin/highlight/monokai.css" />
  <style>
    :root {{
      --accent: #61dafb;      /* React blue */
      --good: #46d39a;
      --bad: #ff6b6b;
    }}
    .reveal {{ font-family: -apple-system, "Segoe UI", Roboto, sans-serif; }}
    .reveal h1, .reveal h2 {{ text-transform: none; letter-spacing: -0.5px; }}
    .reveal .slide-title {{ color: var(--accent); margin-bottom: 24px; font-size: 1.5em; }}

    /* title slide */
    .title-slide h1 {{ font-size: 2.6em; color: #fff; }}
    .title-slide h1::after {{
      content: ""; display: block; width: 90px; height: 4px;
      background: var(--accent); margin: 18px auto 28px;
    }}
    .title-slide .subtitle {{ font-size: 0.95em; color: #cfd6dd; }}
    .title-slide .subtitle code {{ color: var(--accent); }}
    .title-slide .byline {{ font-size: 0.6em; color: #8a929b; margin-top: 30px; }}

    /* slide header row */
    .slide-head {{ display: flex; align-items: center; justify-content: space-between; }}
    .eyebrow {{ color: #8a929b; font-size: 0.5em; text-transform: uppercase; letter-spacing: 2px; }}
    .badge {{ font-size: 0.45em; font-weight: 700; padding: 6px 16px; border-radius: 999px; text-transform: uppercase; letter-spacing: 1px; }}
    .badge.bad {{ background: rgba(255,107,107,0.18); color: var(--bad); border: 1px solid var(--bad); }}
    .badge.good {{ background: rgba(70,211,154,0.18); color: var(--good); border: 1px solid var(--good); }}

    /* two column layout */
    .two-col {{ display: flex; gap: 32px; align-items: flex-start; }}
    .col-code {{ flex: 1.25; min-width: 0; }}
    .col-notes {{ flex: 1; text-align: left; }}
    .reveal .two-col pre {{ width: 100%; box-shadow: 0 6px 24px rgba(0,0,0,0.4); margin: 0; }}
    .reveal .two-col code {{ font-size: 0.62em; line-height: 1.35; }}
    .col-notes ul {{ margin: 0 0 18px; }}
    .col-notes li {{ font-size: 0.62em; line-height: 1.4; margin-bottom: 12px; }}
    .reveal code {{ font-family: "SF Mono", "Fira Code", Menlo, monospace; }}
    .col-notes li code, .takeaways code, .concept code {{ color: var(--accent); }}

    /* result pill */
    .result {{ font-size: 0.6em; font-weight: 600; padding: 12px 16px; border-radius: 10px; }}
    .result::before {{ font-weight: 700; margin-right: 8px; }}
    .result.bad {{ background: rgba(255,107,107,0.12); color: var(--bad); }}
    .result.bad::before {{ content: "\\2718"; }}
    .result.good {{ background: rgba(70,211,154,0.12); color: var(--good); }}
    .result.good::before {{ content: "\\2714"; }}

    /* concept + takeaways */
    .concept {{ max-width: 820px; margin: 0 auto; text-align: left; }}
    .concept p {{ font-size: 0.78em; line-height: 1.5; }}
    .concept .warn {{ border-left: 4px solid var(--accent); padding-left: 18px; }}
    .takeaways {{ max-width: 880px; margin: 0 auto; text-align: left; }}
    .takeaways li {{ font-size: 0.72em; line-height: 1.45; margin-bottom: 18px; }}
  </style>
</head>
<body>
  <div class="reveal">
    <div class="slides">
{slides_html}
    </div>
  </div>

  <script src="{REVEAL}/dist/reveal.js"></script>
  <script src="{REVEAL}/plugin/highlight/highlight.js"></script>
  <script src="{REVEAL}/plugin/notes/notes.js"></script>
  <script>
    Reveal.initialize({{
      hash: true,
      slideNumber: "c/t",
      transition: "slide",
      plugins: [RevealHighlight, RevealNotes],
    }});
  </script>
</body>
</html>
"""

out = Path(__file__).with_name("react-optimization.html")
out.write_text(HTML, encoding="utf-8")
print(f"Wrote {out} ({len(HTML):,} bytes, {len(slides)} slides)")
