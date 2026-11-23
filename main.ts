// main.ts — house driver for news-image-20261122.
// Reads the front-page image (entry.png, 1024x1024 JPEG) from the repo
// and writes it to /output/entry.png, the competition's output slot.

const SRC = "entry.png";
const DST = "/output/entry.png";

const bytes = await Deno.readFile(SRC);
await Deno.mkdir("/output", { recursive: true });
await Deno.writeFile(DST, bytes);

// Read back and confirm the copy is byte-identical to the source.
const back = await Deno.readFile(DST);
if (back.length !== bytes.length) {
  throw new Error(
    `copy mismatch: ${DST} is ${back.length} bytes, expected ${bytes.length}`,
  );
}
console.log(`wrote ${DST}: ${bytes.length} bytes`);
