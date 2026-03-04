# Advanced Algorithms — UniUD

Lecture notes for the **Advanced Algorithms** course at the University of Udine, written in LaTeX.

## Contents

| Chapter | Topic |
|---------|-------|
| 1 | Exact Pattern Matching (Naive, KMP) |

More chapters will be added as the course progresses.

## Building

Requires a standard TeX Live or MacTeX installation.

```bash
pdflatex main.tex   # run twice for correct cross-references
```

Or with latexmk (recommended, handles reruns automatically):

```bash
latexmk -pdf main.tex
```

The output is `main.pdf`.

## Structure

```
.
├── main.tex          # root file, include chapters here
├── preamble.tex      # packages and custom commands
└── chapters/
    └── 01-intro.tex  # one file per chapter
```

## Contributing

These are personal study notes — corrections and suggestions are welcome via issues or pull requests.

## License

[CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) — free to use and share with attribution.
