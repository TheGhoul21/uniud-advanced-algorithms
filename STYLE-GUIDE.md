# Style Guide — Advanced Algorithms Notes

Guidelines for writing, structuring, and illustrating these lecture notes.

## Writing Style

**Tone**: Knowledgeable guide, not textbook. Write as if you're walking someone through the material at a whiteboard. Use "we", "let's", "notice that". Never compress three ideas into one sentence.

**After every formal definition**: Add an intuitive paragraph that unpacks it piece by piece in plain language. Reference a concrete example by number. The definition is for precision; the paragraph is for understanding.

**Step-by-step over summary**: When describing an algorithm or process, list what happens at each step. "Two things can happen: ..." is better than a single abstract sentence covering all cases.

**Concrete before general**: Always show a specific example first, then state the general rule. "For instance, `nan` is a prefix of the suffix `nana`" before "every substring is a prefix of some suffix."

## Structure

**Formal definitions** stay formal — they're reference material. But they never stand alone. Every definition gets:
1. An intuitive walkthrough immediately after
2. A cross-reference to a concrete example/figure
3. Color-highlighted elements in the referenced figure

**Formaldetails boxes** for proofs and complexity analyses — wider than normal text, centered on the page, light teal background. Inner theorems/lemmas keep their normal styling (colored left bar).

**Intermezzo boxes** for historical notes, fun facts, and tangential connections — warm orange background. Keep them self-contained and interesting.

**Asides** (margin notes) for brief clarifications, one-liners, and connections to other concepts. Keep them short — if they overflow the margin, they're too long.

## Figures

**Every major concept gets a figure**. If you're describing a tree, draw the tree. If you're describing a process, show before/after.

**Cross-reference with colors**: Highlight specific elements in TikZ figures (e.g., violet edge for a transition, red dashed arrow for a suffix link) and reference them in the text: "the violet-highlighted edge shows g'(ca, c) = cac."

**Style consistency**:
- Blue: internal/branching nodes
- Orange: leaves
- Gray (dashed border): implicit/pass-through nodes
- Violet: highlighted transitions
- Red (dashed): failure/suffix links
- Green (dotted): output links
- Solid lines: tree edges

**Annotations on figures**: Use boxed labels with leader arrows for callouts. Never let annotations overlap with the figure content. Keep them outside the main structure.

**Scan direction arrows, pointers, comparison markers** must be clearly visible — bold, colored, not gray.

## Examples

**Recurring examples**: Use the same strings across related sections (`cacao` for suffix structures, `potato/tatoo/theater/other` for keyword trees, `he/she/his/hers` for Aho-Corasick). Familiarity reduces cognitive load.

**Verify properties on examples**: After stating a property (size, height, fan-out), verify it on the running example with actual numbers: "the tree has 23 edges, confirming the size bound."

**Show the failure case**: When motivating a new concept, show concretely what goes wrong without it. "We already knew that T[3,4] = `he`; going back to the root and re-reading them is redundant work."

## Connecting Concepts

**Bridge sections explicitly**: When a new structure generalizes an old one, say so directly. "A suffix trie is exactly the keyword tree of the set of all suffixes" with the formula. "Failure links are the direct multi-pattern generalisation of KMP's sp' values."

**"Why learn X if we have Y?"**: Address this whenever two algorithms solve similar problems. Boyer-Moore vs KMP, keyword tree vs running KMP per pattern.

**Historical context as intermezzos**: Who invented it, when, why, what tool it was built for. "Every time you run `grep -F`, you're using Aho-Corasick."

## Layout

**Oneside** (digital notes, not printed book). Wide right margin for asides. Formaldetails and intermezzos extend into the margin space, centered on the physical page.

**No dashed borders** on boxes — just colored backgrounds. Formaldetails = teal tint, Intermezzo = orange tint. Bold sans-serif headers with a small filled square icon.

**Theorem-like environments**: Colored left bar (2.5pt), light tinted background.
- Blue: theorems, lemmas, corollaries, propositions
- Teal: definitions
- Orange: examples
- Violet: exercises, problems
- Gray: remarks, notes, observations

## Notebooks

**One notebook per algorithm/topic**, not one giant monolith. Both `.qmd` (Quarto/Pyodide for web) and `.ipynb` (Jupyter with ipywidgets).

**Code hidden by default** (`echo: false` for qmd, `source_hidden` for ipynb). The reader sees only the interactive controls and output.

**Granular stepping**: Each step should show one atomic operation. For naive matching: one character comparison per step, with explicit backtrack steps. The student should see the repeated work, not just the result.

**Visual feedback**: Active path lit up, inactive parts grayed out. Color-coded status messages. Running counters for total comparisons and matches found.

**Match the notes' examples**: Default inputs in notebooks should use the same strings as the LaTeX notes.

## What NOT to Do

- Don't compress a walkthrough into a single dense sentence
- Don't let a formal definition stand without intuitive follow-up
- Don't use invisible gray for important visual elements
- Don't nest boxed environments with conflicting border styles
- Don't assume the reader connects abstract definitions to figures on their own — make the connection explicit with colors and cross-references
