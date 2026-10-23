---
name: translate-paper
description: Translate a paper's full text from one language into another, preserving equations, citations and structure. Use when the user asks to translate a paper, an abstract or a section of one.
---

# Translate a paper

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

## Handling empty-argument skill invocation

If this skill is invoked with no further instruction, do not guess at a task. Briefly describe what the skill does, then ask for the one thing you need to start — a topic, a set of papers, or a folder. Where the harness offers a structured question tool, use it; otherwise present numbered options and wait.

## 1. Confirm the paper and the languages

Which paper, and into which language. `lookup_papers` fills in metadata from a DOI if you only have
that.

## 2. Get the text

Translation needs the whole document as a file, so this is the case for downloading rather than reading
through the MCP tools. See the `auto-highlight-papers` skill:

```bash
paperpile files download --citekey [citekey] --to ./papers
```

`paper.md` in the reference's folder is the source text.

If the paper has no PDF, say so. A PDF on the user's disk can be attached with
`paperpile files upload <path> --reference-id <id> --primary`; otherwise they attach it themselves
from the Paperpile app or the browser extension. Either way the download works on the next attempt.

## 3. Plan the translation

Run one subagent over the whole document to produce two things before any translating starts: a glossary
of the domain terms, and a split of the paper into segments.

Subagents run through the CLI's subagent framework, at most 10 at once.

- Grant each one file reads and the Paperpile MCP tools. Subagents only get the tools the main agent hands them.
- Give each one the prompt below with the bracketed values filled in, and nothing else. It should not load other skills.

The glossary is what keeps the translation coherent. Without it the same term comes out three ways
across a long paper, which is the failure a reader notices first.

## 4. Translate the segments in parallel

One subagent per segment, each writing `segment-1.md`, `segment-2.md` and so on to the working
directory.

## 5. Assemble

Concatenate the segments in order into `[author][year]-[language code].md`, delete the per-segment
files, and tell the user they were scratch.

Summarise what happened — how the paper was split, anything the translation had to drop — and show the
first few lines. Then offer other formats: PDF, LaTeX, or whatever the user needs.

<Begin: planning subagent prompt>
You are part of Paperpile's research skills. Read one paper in full and prepare it for translation.

- **Paper**: [title, year, authors]
- **Source language**: [source]
- **Target language**: [target]
- **Full text**: [path to paper.md]

Produce two things.

**A glossary.** Scan for the terms that recur and the terms a general translator would get wrong:
technical vocabulary, field-specific concepts, named methods and datasets, acronyms. Give each one a
single agreed translation. This is what stops the same concept being rendered three different ways in
three sections.

**A segmentation.** Split the paper into roughly equal parts of about 1,000 words, but move the
boundaries to fall on section breaks — a segment that ends mid-argument translates badly.

Reply in this shape:

```
## Glossary

### Concepts
source term → target term

### Technical terms
source term → target term

### Methods and datasets
source term → target term (a named method or dataset usually keeps its name; say so rather than translating it)

### Acronyms
source term → target term (keep the abbreviation / expand it, whichever the target language does)

## Segments

- Segment 1: lines 0-200
  - Sections: Abstract, Introduction
  - Output: segment-1.md
- Segment 2: lines 201-500
  - Sections: Methods
  - Output: segment-2.md
```
<End: planning subagent prompt>

<Begin: translation subagent prompt>
You are a precise academic translator. Translate one segment of a paper.

- **Paper**: [title, year, authors]
- **Source language**: [source]
- **Target language**: [target]
- **Full text**: [path to paper.md]
- **Segment**: lines [start]-[end], covering [sections]
- **Write to**: [output filename]

Read only your line range, translate it, and write the result as Markdown to the output file.

Leave untranslated, verbatim: equations and formulas, URLs and DOIs, author names and proper nouns,
citations ("Smith et al. 2023"), code, and figure or table labels that carry a number ("Figure 1",
"Table 2a").

Apply the glossary exactly. Where you meet a related term that is not in it, follow the same pattern the
glossary sets.

Match the register of academic writing in the target language. Keep the technical distinctions the
author drew — do not simplify a hedge into a claim. Keep the sentence structure close to the original
where the target language allows.

Formatting: clean Markdown. Keep paragraph breaks, drop the line breaks inside paragraphs, and use
Markdown headings for the paper's own section hierarchy.

Drop, with a placeholder in place: page markers ("--- Page 1 of 12 ---"), running headers and footers,
tables (`[Table 1 not translated]`) and block equations (`[Equation not translated]`). Text extraction
does not preserve their structure well enough to translate them faithfully.

Report back: which sections you translated, the file you wrote, and anything that gave you trouble.

Glossary:

[glossary]
<End: translation subagent prompt>
