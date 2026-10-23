---
name: auto-highlight-papers
description: Go through a set of papers for a stated focus area and mark the key passages as PDF highlights in the user's Paperpile library, so they are bookmarked for deeper reading. Also the reference for getting at a paper's text at all — full-text search, get_text_content, or downloading PDFs with the Paperpile CLI. Use when the user wants papers gone through for a topic, or asks for the text, the PDF, or a local copy of a paper.
---

# Auto-highlight papers

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

## Handling empty-argument skill invocation

If this skill is invoked with no further instruction, do not guess at a task. Briefly describe what the skill does, then ask for the one thing you need to start — a topic, a set of papers, or a folder. Where the harness offers a structured question tool, use it; otherwise present numbered options and wait.

The researcher still does the reading. This skill finds the passages worth their attention and leaves a
highlight at each one, so the library carries the bookmarks afterwards.

## Step by step flow

### 1. Define the focus

You need a focus area or a statement of interest — the thing that makes a passage worth marking. If the
user has not given one, ask for it before reading anything. "Highlight the key parts" without a focus
produces highlights on whatever happened to be quotable, which is worse than none.

### 2. Understand the scope

Which papers: a folder, a label, a search, a list of citekeys. Confirm the shortlist before you start
reading — reading is the expensive half. Use the `find-papers` skill if the user described the papers
rather than naming them.

### 3. Find the passages

Two primary tools will help find the right passages to focus on:

- `search_library` - finds PDF passages matching one or more search terms. Supports parallel queries.
  - Start here when the focus is speciifc.
- `get_text_content` - extracts regions of text from PDFs.
  - Start here when you need to read a paper end-to-end.
  - Use this tool after `search_library` to read the surrounding context of a search result.

### 4. Highlight what matters

Aim for a handful per paper — three to six for a focused question. Prefer few, well-chosen passages
over broad coverage: a highlight on every paragraph is the same as no highlight at all. Mark the
sentence that carries the claim, not the paragraph around it.

### 5. Say what you did

Close with a short summary: the focus you worked to, how many papers you went through, and an
enumeration of what was highlighted — paper, section, and one line on why that passage. This is what
tells the researcher where to start reading, so it is not optional.

Name any paper you could not cover and why: no PDF attached, nothing matching the focus, a scanned
document with no extractable text.

## Tools and tips

### Analyzing the full text of a reference

**Search before you read.** Call `search_library` with the citekey and two or three phrasings of what
you want, in the words the paper would use. Five queries run in parallel in one call.

A `fulltext` hit carries `snippet`, `pageNumber` and `fileId` — what a Paperpile PDF link,
`highlight_text` and `get_text_content` all take.

**Read around the hit before relying on it.** The surrounding sentence can reverse a snippet's meaning,
so fetch an expanded region around the snippet (start with a few hundred bytes on each side) to gain more context. Take the `pageNumber` and `charOffsets` from a search result and pass to `get_text_content` as `{ page, start, end }`. Clamp the widened `start` at zero; a negative `start` is rejected.

Read a paper front to back only when that is the job, or when search comes up empty: no extractable
text, or an answer spread across a whole section.

### Leaving a highlight

`highlight_text` puts a real PDF highlight on a passage, so it survives in the library instead of only
in this conversation. Give it the `citekey` and the exact `text` — long enough to be unique in the
document — plus an optional `note`, and `color` (`yellow`, `red`, `blue`, `green`).

Use the `note` for why the passage matters. A highlight the researcher finds in three weeks with no
note is a sentence they have to re-derive.

A passage that crosses a page boundary comes back as one note per page. That is expected, not a
duplicate.
