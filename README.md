# handwriting-to-md

A Claude skill that turns handwritten PDFs (reMarkable exports, other tablets, scans) into editable Markdown. Claude reads your handwriting directly, with no OCR. Diagrams become Mermaid code or cropped images, and math becomes LaTeX (`$...$`).

Your wording stays as written: abbreviations, spelling and mixed languages are kept. When Claude can't read a word, it checks the web and then asks you, instead of guessing.

## Install

**Claude Code**

```
/plugin marketplace add kosinal/handwriting-to-md
/plugin install handwriting-to-md@handwriting-to-md
```

**Claude app (claude.ai, desktop)**

Go to **Customize → Plugins**, add the marketplace `kosinal/handwriting-to-md`, and install **handwriting-to-md**. Code execution must be on (Settings → Capabilities → *Create and edit files*).

## Use

```
/handwriting-to-md:convert notes.pdf
```

Or just ask: *"convert notes.pdf to markdown"*. In the Claude app, attach the PDF and ask.

The output is `notes.md`, saved next to the PDF. On the first run Claude asks how to draw diagrams (Mermaid or image) and remembers your choice. To change it later, ask *"switch diagrams to images"*.

Mermaid mode needs nothing. Image mode in the Claude app works out of the box. In Claude Code, image mode needs Python 3.9+ with either [uv](https://docs.astral.sh/uv/) (installs everything automatically) or `pypdfium2` and `pillow` installed.

## Example

- Diagram and notes: [`examples/home-lab.pdf`](examples/home-lab.pdf) → [`examples/home-lab.md`](examples/home-lab.md)
- Math: [`examples/statistics.pdf`](examples/statistics.pdf) → [`examples/statistics.md`](examples/statistics.md)

## License

[Apache 2.0](LICENSE)
