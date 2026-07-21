// Batch KaTeX renderer: reads {"macros": {...}, "segments": [{"tex","display"}]}
// on stdin, writes a JSON array of rendered HTML strings on stdout.
// throwOnError stays true: a formula KaTeX cannot render must fail the build,
// never degrade silently (the HTML must follow the book exactly).
import katex from "katex";
import { readFileSync } from "fs";

const { macros, segments } = JSON.parse(readFileSync(0, "utf8"));

const out = segments.map(({ tex, display }, i) => {
  try {
    return katex.renderToString(tex, {
      displayMode: display,
      throwOnError: true,
      strict: "ignore", // e.g. Unicode … in math; KaTeX renders them fine
      macros: { ...macros },
    });
  } catch (e) {
    process.stderr.write(`segment ${i}: ${tex}\n${e.message}\n`);
    process.exit(1);
  }
});

process.stdout.write(JSON.stringify(out));
