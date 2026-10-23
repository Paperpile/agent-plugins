---
name: extract-paper-data
description: Extract data from one or more papers by analyzing the full-text content, using Paperpile tools. Use for generating meta-analysis tables, structured literature reviews, methods surveys, or whenever the user asks for a table or dataset to be generated from a set of papers. Results can be saved to CSV, Excel, or Markdown.
---

# Extract data from papers

This skill is a structured workflow to guide an agent through using Paperpile's literature exploration and full-text analysis tools to
extract specific data from several papers, informed by careful reading of the full-text content of each paper (when available).

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

## Handling empty-argument skill invocation

If this skill is invoked with no further instruction, do not guess at a task. Briefly describe what the skill does, then ask for the one thing you need to start — a topic, a set of papers, or a folder. Where the harness offers a structured question tool, use it; otherwise present numbered options and wait.

## Reference formatting

Whenever you present a paper to the user, use this four-line block. It is the format Paperpile users recognise, and it stays scannable in a terminal.

```
**Title**
Author1 LN, Author2 LN, Author3 LN
*Journal Abbrev* · Year · Article type · N,NNN citations
[Canonical link] · [View PDF link]
```

- **Title** — the full canonical title, bold.
- **Authors** — `Last F` or `Last FM`, no periods, comma separated. Show all of them up to five; beyond that show the first three, then `... N more ...`, then the last two. Consortium and working-group names are never abbreviated.
- **Metadata** — journal in italics using its NLM abbreviation (single-word titles are never abbreviated: *Nature*, *Science*, *Cell*, *eLife*), then year, then article type (`Journal article`, `Review`, `Preprint`, `Book chapter`), then the citation count with a thousands separator. Separate the fields with ` · `. Omit any field you do not have rather than guessing it — never print `0` or `N/A`. The article type comes from the reference's `type`: library results carry it in `MARKDOWN`, catalog results only in `JSON`.
- **Canonical link** — A link to the canonical publisher or preprint URL. Prefer the `https://doi.org/...` DOI link if available; otherwise, a preprint or PubMed link is acceptable. Use a Markdown link, with the anchor text one of the following: Website, PubMed, arXiv.
- **View PDF link** - For references in the user's Paperpile library with a main article PDF, include a PDF viewer link with the format `https://app.paperpile.com/view/?id=[file_id]`, where file_id is the Paperpile file ID. Make a `get_references_from_library` call with the citekey to get full metadata if the article PDF status is not known.

the canonical `https://doi.org/…` URL as a Markdown link. An arXiv preprint from the last three months may not have reached the DOI resolver yet; use its `https://arxiv.org/abs/…` URL instead. Drop the line if there is neither.

Put `---` before the first entry and after the last. Separators between entries are optional — use them when the list is long enough to need the visual break.

A comment about a paper goes on its own line after the link, as a `-` bullet.

```
---

**Eleven grand challenges in single-cell data science**
Lähnemann D, Köster J, Szczurek E ... 14 more ... Schönhuth A, Rahmann S, Schreiber S
*Genome Biol* · 2020 · Review · 1,098 citations
[Website] · [View PDF]

- Frames the field's open problems; useful as an anchor for anything downstream of scRNA-seq.

---
```

### Note: citation counts

If you are presenting a small number of papers to the user and you don't already have citation counts available, you can make a quick call to `find_papers` with the DOI of each paper in the query_list to get citation counts.

## Paperpile PDF links

Paperpile can deep-link into the PDF of any reference in the user's library, so a quote or a claim can be checked against the source in one click. Use these links liberally.

### URL format and parameters

```
https://app.paperpile.com/view/?id=[file_id]&page=[pdf_page]#hl=[encoded quote]
```

Parameters:

- `id` — **required.** The id of the reference's PDF attachment: the `file_id` in a reference's `files` array, or the `fileId` returned alongside a full-text search hit. It is **not** the reference id and **not** the citekey. Without a `file_id` you cannot build one of these links — cite the DOI instead.
- `library` — only include when the paper lives in a shared library rather than the user's personal one.
- `page` — the PDF page number. Include it whenever you know it.
- `#hl` — the passage to highlight, as a **URL fragment**, always last. It is a `#` fragment, not a `&` query parameter. Omit if there's not a
  quote that directly anchors this link.

### Three link styles

Choose between three link styles for Paperpile links: `quote link`, `named section`, or `page number`. Always use Markdown link formatting for Paperpile PDF links.

- Quote link: when the output includes quoted text from a source, include a link after the quotation. The anchor text should be a bracketed page number, e.g. "Quote from source text", [p. 12]
- Named section: when a sentence or paragraph is backed primarily by text within a named section of a paper, but a verbatim quote isn't shown
  in the main text, use this style. Example: "X, Y and Z facts [Methods, p. 8]".
- Page number: when a fact is located in or attributable to a specific page, but a named section isn't appropriate, e.g. "The authors used X
  system [p. 12]".


### Highlighting the exact passage

`#hl` opens the PDF scrolled to the passage with it highlighted. Always include this parameter when there's a verbatim quote shown in the main
text.

- **Pass the full quoted text, matching what you display, word for word.** Paperpile fuzzy-matches the value against the PDF. You MUST include
the first 5 and last 5 words from the quote in the `hl` value. You MAY omit some of the middle of the quote with a `...`, especially if the
quote is long.
- Omit special characters and parentheses from the `hl` value. Keep only the alphanumeric characters; the fuzzy match algorithm will handle
a few missing or different characters. Example: `the Bradford assay (Bio-Rad)` becomes `the%20Bradford%20assay%20Bio-Rad`.
- Encode what remains with `encodeURIComponent` semantics: spaces become `%20` (**not** `+`), `,` becomes `%2C`, `%` becomes `%25`.
- Do not paraphrase. Use only exact text from the source.
  - Example: `We%20found%20that%2094%25%20of%20the%20tests...lost%20significance%20after%20correction%20for%20multiple%20hypotheses`
- Always pair `#hl` with `&page=` when you know the page. The page number is what the reader sees in your prose, and it lands them in the right place even if the match fails.

### When to link

- **REQUIRED:** whenever you directly quote a source, attribute the quote with a canonical Paperpile link whose text includes the page within the PDF, and optionally the author-year string if contextually relevant.
  - Example quote: "We wish to suggest a structure for the salt of deoxyribose nucleic acid" [Watson and Crick 1953, p. 1](https://app.paperpile.com/view/?id=[file_id]&page=1#hl=We%20wish%20to%20suggest%20a%20structure%20for%20the%20salt%20of%20deoxyribose%20nucleic%20acid)
  - If the source paper is obvious from the context, omit the author-year and use just the page number. Example: "We wish to suggest a structure" [p. 1](https://app.paperpile.com/view/?id=[file_id]&page=1#hl=We%20wish%20to%20suggest%20a%20structure)
  - Example of a long quote elided in the middle, with both anchors intact: "This structure has novel features … considerable biological interest" [Watson and Crick 1953, p. 1](https://app.paperpile.com/view/?id=[file_id]&page=1#hl=This%20structure%20has%20novel%20features...considerable%20biological%20interest)
- **HIGHLY ENCOURAGED:** add links for other statements that relate to a specific part of the source text — sections, figures, tables, facts, themes, conclusions. The more links the better, as they help the user jump to the source to verify information.
- Always review your finished output for quotes that are missing a link, for `#hl` values containing a parenthesis, and for `#hl` values that are missing their closing anchor — every `#hl` must end with the verbatim final words of the passage.

### Link text

Prefer a Markdown link whose text is the author-year, the page number, or a section name — whichever the surrounding prose needs. Never emit a bare Paperpile URL.

- Bad: `https://app.paperpile.com/view/?id=[file_id]`
- Good: [Watson and Crick 1953, p. 1](https://app.paperpile.com/view/?id=[file_id]&page=1#hl=...)
- Okay: https://doi.org/10.1234/xyz — raw DOI or publisher links are fine, and are the right fallback when the paper has no PDF in the library.

### Page numbers

Always use the page number **within the PDF**, which is usually a small number, not the page number within the journal or volume, which can be much higher. The same number goes in both the `page` parameter and the link text, so they always agree.

- Bad: p. 2242
- Good: p. 2

When a full-text tool reports a page number it is already the PDF page. When you read a page number off the printed page of a scanned article, convert it: subtract the article's first journal page and add one.

## Who is reading this

This skill is loaded by two kinds of reader, and which one you are decides what you do with it.

- **The orchestrator** - the main conversation thread. You run Steps 1 to 4 in order: resolve the set of
  papers, agree the columns and size with the user, dispatch one subagent per paper, then assemble and
  publish the table.
- **A per-paper extraction subagent** - dispatched by the orchestrator in Step 3. Your envelope prompt
  says so explicitly and names a single paper. You execute **only** the per-paper extraction contract in
  Step 3, and you never run Steps 1, 2 or 4.

If nothing in your prompt named you a per-paper extraction subagent, you are the orchestrator.

A subagent that starts assembling the table, running `build_table.py` or publishing an artifact has
misread its role. The orchestrator does that once, after every subagent has returned. Equally, an
orchestrator that reads the papers itself rather than dispatching has skipped the parallelism that
makes this workflow tractable.

## Step 1: Identify the exact set of papers in scope

This workflow depends on having a specific set of papers identified as in-scope for analysis and saved to the user's
Paperpile library. Typically 5-10 papers is a good number for data extraction; too many more and the full-text analysis stage
will take more time and the results become hard to interpret. (Of course, the user may request a larger number -- just warn them
in advance of the token spend and wait time for a larger-scale analysis.)

A few possible ways the user may specify which papers are in scope:

- A folder or label in their Paperpile library (this is easy and preferred) - use `get_collections_from_library` to resolve the
  collection to an ID, then `get_references_from_library` to fetch the paper
- A set of citekeys, titles, or DOIs to analyze - use `search_library` with full_text off to find those papers in their library.
- A general topic or research group of interest - confirm with the user they'd like to search for papers to include, then re-route
  to the `find_papers` skill to find and save papers before returning to the data extraction task.

Once you have the set, scan the titles for members that do not fit the framing of the request. A folder often collects papers for
several reasons at once, and a paper that shares the folder but not the topic still costs a full extraction to process. Name any
outliers to the user at the Step 2 confirmation and ask whether to include them - do not silently drop them, and do not silently
spend a subagent on them.

## Step 2: define the table size and set of columns

Before proceeding, get confirmation from the user on their desired set of table columns, and also how much information or text they'd be
comfortable seeing within each table cell. It's best to present the user with a reasonable default set of columns and offer a table
size based on your judgment, but let the user know what can be easily adjusted or tweaked before proceeding.

For table size, use a basic S / M / L t-shirt sizing guideline. Each size carries a **hard character ceiling per cell**.

| Size | Per cell | Ceiling | Use when |
| --- | --- | --- | --- |
| **S** | A few words up to a short sentence | **120 characters** | Basic facts across a larger number of studies |
| **M** | A sentence or two | **250 characters** | Some detail per column, without an overwhelming amount of text |
| **L** | A short paragraph, with exact methods, numbers or formulas | **600 characters** | A reference document for future work |

Rules for applying the ceiling:

- **Count only user-visible text.** Markdown link syntax does not count: `[p. 12](http://…)` counts as the 5 characters `p. 12`.
  Links are free, so keep adding them.
- The ceiling is a maximum, not a goal. Be concise where you can.
- If a value genuinely will not fit - a pipeline with fourteen named tools at M - keep the most important items, end with
  `and others`, and let the extraction notes carry the full list. Do not exceed the ceiling to be complete.
- Warn the user that an L table is harder to read and interpret, but is useful as a reference.

**Cost scales with columns x size, not size alone.** Ten columns at M is around 2,500 characters per paper, which is a lot of table.
As a rough guide, keep to about 6 columns at M or L, and up to 10 at S. If the user wants more columns than that, allow them to override this rule of thumb.

Start with a basic set of columns you might include by default for most studies, for example:

- Paper identifier / DOI
- Authors (short list, with 'et al.' as needed)
- Publication year
- Study design
- Primary objective

Decide on additional colummns based on the user's expressed intent as well as the domain and nature of the papers in scope.

If you need to learn more about the papers in scope, call the `lookup_papers` tool to get complete metadata.

Domain-specific column examples:

- Computational biology: model organism, primary data type, algorithm / pipeline, benchmark dataset
- Social scienes: sample size, demographics, intervention, outcome measure, effect size
- Qualitative research: theoretical framework, data collection methods, key themes, author's core argument

IMPORTANT: you MUST share the list of columns and table size, and request confirmation from the user before proceeding to the next step.
The confirmation is also where you tell them the estimated time cost, since Step 3 is slow and they should not discover that after it
has started. Use the following template message:

<BEGIN: template message>
Here are the proposed columns to be filled in by analyzing your papers:

- Study ID / DOI
- Authors
- Publication year
- Study design
- Primary objective
- [... other columns]

And the proposed amount of extracted content is Medium (a sentence or two per cell).

Reading the full text of [N] papers will take roughly [X] minutes. Please confirm before we proceed, or suggest any changes.
<END: template message>

### How long it takes

Give an estimate in the confirmation message. Papers are read concurrently, one subagent each, so **wall-clock time is roughly set by
the slowest paper, not the total** - going from 5 papers to 10 barely moves it. Assembling the output afterwards costs a fairly fixed
5-7 minutes on top.

| Size | Per paper | Tokens per paper |
| --- | --- | --- |
| S | 2-3 minutes | ~40k *(estimated)* |
| M | 3.5-5.5 minutes | 70-125k *(measured, n=5)* |
| L | 8-10 minutes | ~180k *(estimated)* |

**A typical run of 5-10 papers at M takes 10-15 minutes end to end.** Say so plainly. These timings are just estimates and should be treated as rough.

Above about 10 papers, warn the user explicitly about the token spend before starting, and note that concurrency is capped - beyond
roughly a dozen subagents the remainder queue and run in a second wave, so wall clock starts to climb.

## Step 3: Read full text and store interim results

Search or scan through the full text content of each paper to extract the column value for each paper. If any paper doesn't have full-text
content available, you may rely on the abstract & metadata (but this limitation must be indicated and emphasized to the user).

### Analyzing the full text of a reference

**Search before you read.** Call `search_library` with the citekey and two or three phrasings of what
you want, in the words the paper would use. Five queries run in parallel in one call.

A `fulltext` hit carries `snippet`, `pageNumber` and `fileId` — what a Paperpile PDF link,
`highlight_text` and `get_text_content` all take.

**Read around the hit before relying on it.** The surrounding sentence can reverse a snippet's meaning,
so fetch an expanded region around the snippet (start with a few hundred bytes on each side) to gain more context. Take the `pageNumber` and `charOffsets` from a search result and pass to `get_text_content` as `{ page, start, end }`. Clamp the widened `start` at zero; a negative `start` is rejected.

Read a paper front to back only when that is the job, or when search comes up empty: no extractable
text, or an answer spread across a whole section.

### Use subagents for many papers

If more than 5 papers are in scope and the current harness supports subagents, parallelize the extraction across subagents, one paper per subagent, so they run concurrently. Each subagent writes its own extraction notes file and returns the filename plus the "extracted"
data to the orchestrator. Make sure the subagent has access to the right skills, tool and file permissions to complete the task.

If possible, run subagents with the next-smaller or cheaper model compared to the orchestrator model. This will help with runtime and cost.

**Use the envelope template in the appendix rather than improvising a prompt per paper.** The envelope is deliberately short: it
carries only what differs between papers, and tells the subagent to load this skill for everything that does not.

### The per-paper extraction contract

**This subsection is what a per-paper extraction subagent executes**. The orchestrator does not work through it directly, unless it is
processing a small number of papers itself.

Each paper should produce two distinct outputs:

  - A set of freeform, detailed `extraction notes` meant to collect relevant facts, ideas, and quotes from the source material
    relating to each column.
  - A final set of `extracted data` column values, distilling each column's extraction notes into a summative value that adheres
    to the table size and column definition.

#### Extraction notes

 - Extraction notes should capture each distinct data point, source quotation, idea, or concept from the source text that relates
to each column.
 - Use bullet points, not paragraphs.
 - Include at least one high-quality source quotation for each non-bibliographic column. Quotations should get a Paperpile style PDF link at the end.
 - If possible, include a bullet mentioning which named section of the paper is most relevant to this column and which PDF page it's on, e.g.: "Relevant section: Discussion, p. 8"

#### Extracted data

 - Each extracted value must respect the table size named in your envelope, per the size definitions above. Count user-visible text only. The
   URLs from Markdown-formatted links don't count, only the anchor text.
 - For each non-bibliographic column, aim to include at least one Paperpile PDF link pointing to a supporting quotation, section or page.
 - It's fine to report when the paper does not have data for a column, e.g. "No repository accession was given"
 - If a column genuinely does not apply to your paper, write "Not applicable" with one clause saying why,
   rather than stretching an unrelated method into the cell.
 - Aim for at least one Paperpile link per extracted data entry. Never use the main text content as anchor text for a Paperpile link; only use
   the bracketed page number or section name style, e.g. "[p. 12]".
 - For references to external resources (e.g. GitHub repos, dataset links, DOIs, etc.), use Markdown-formatted links.

#### Output file

Write your notes to `[scratch_dir]/[citekey]-extraction-notes.md`, using the scratch directory named in
your envelope.

```
# [citekey]

## Notes

### [Column name]
- [Extraction notes for this column]

## Extracted

- **[Column name]**: [the value, within the character ceiling, with links]
[One bullet per column, in the order given in your envelope.]
```

The `## Extracted` block is parsed by a script. Each bullet must be exactly `- **Column name**: value`,
using the column names from your envelope verbatim and in order. A renamed or missing column is
reported as an error.

#### What to return

Your final message must be exactly:

1. The path to the notes file you wrote.
2. The full `## Extracted` block, verbatim, with the links intact.

No preamble and no summary of your process. Do not build the table, do not run `build_table.py`, and do
not publish anything - that is Step 4, and it belongs to the orchestrator.

## Step 4: assemble the table and report back to the user

**One row per paper, always.** Papers are rows and attributes are columns, in every rendering of the results - the Markdown table in
the conversation, the HTML file, and any export. This is the convention for extraction tables and the user should not have to
transpose anything in their head.

At the top of your response, summarize the task and share a list of the papers which were analyzed, each shown in the Paperpile reference format.
Be sure to indicate if any papers didn't have full text available, as that will limit the accuracy.

Show the table, or a representative slice with the row count if it is too wide or too long for the
conversation. This table should be in Markdown format, with Paperpile PDF links included.

### Building the HTML

Use `build_table.py`, which ships in this skill's directory. Do not hand-write a converter - assembling Markdown links into HTML by
hand is where these runs lose time and break links, and the script already handles the parsing, the escaping and the checks.

Write a config file, then run it:

```
python3 [skill_dir]/build_table.py config.json           # writes the HTML
python3 [skill_dir]/build_table.py config.json --check   # validates only, writes nothing
```

The script reads the `## Extracted` block from each `[citekey]-extraction-notes.md`, emits one row per paper with the reference list
below the table, and validates as it goes. The header comment in the script documents the config keys. Its styling is deliberately
plain; do not add a design pass on top of it.

**Set `"size"` to the S / M / L size you agreed in Step 2.** The script then enforces that size's per-cell ceiling, counting
user-visible characters and ignoring the URLs behind links, and reports any cell that is over along with how far over it is. It is
the authoritative check, so nobody downstream needs to count characters by hand.

The script will report errors and warnings. Warnings do not block, but each one names a real defect worth fixing at the source:
a parenthesis inside `#hl`, an anchor ending in `...` with no closing text, a `+` where `%20` belongs. If the script reports
errors, fix the notes files and re-run it.

### Where to put it

**If the harness supports artifacts, publish there first** - it gives the user a shareable page rather than a file path.
Publish the file that `build_table.py` produced, unchanged. Its plain styling is the intended look for these tables, so skip any
separate design step and do not restyle the output.

If artifacts are not available, save HTML to the working directory with an informative name, like `[topic] - [date] - extracted data.html`.

Also, construct a complete reference of all extraction notes by concatenating each of the individual notes files together. Save the concatenated file to a Markdown file with a similar name scheme, like `[topic] - [date] - extraction notes.md`.

Share links to the just-saved files to the user, and also mention that they can export the table to different formats if they prefer: CSV, Excel, Markdown and LaTeX are all reasonable options to offer. (Note: strip the Paperpile PDF links from output formats like CSV which can't easily display formatted links.)

## Appendix: subagent envelope

Give each subagent the envelope below with the bracketed values filled in, and nothing else.

Fill in everything in square brackets from the conversation and from the specific paper you are handing
over.

<Begin: subagent envelope>
You are part of Paperpile's research skills.

## Execution context

You are running as a **per-paper extraction subagent** inside a larger `extract-paper-data` run covering
[N] papers. Your first action must be to load the `extract-paper-data` skill that defines this job.

That skill describes a four-step workflow. **You are executing the per-paper extraction contract in
Step 3, and nothing else.** Steps 1 and 2 are already done - the papers and the columns below were
settled before you were dispatched. Step 4 belongs to the orchestrator: do not assemble the table, do
not run `build_table.py`, do not publish an artifact, and do not write a report for the user.

Follow the contract as written. The values below are what is specific to your paper.

## Your paper

- **Citekey**: [citekey]
- **file_id**: [file_id] - use this for every PDF link you write
- **Title**: [title]
- **Published**: [journal], [year]. DOI [doi]

## Columns to extract

[Numbered list of the agreed columns. Give each one a short gloss saying what belongs in it, so every
paper is read against the same definition.]

## Table size

**[S / M / L]** - see the ceiling for that size in the contract.

## Scratch directory

`[scratch_dir]`
<End: subagent envelope>
