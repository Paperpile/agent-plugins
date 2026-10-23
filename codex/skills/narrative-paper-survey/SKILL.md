---
name: narrative-paper-survey
description: Write a short narrative survey that ties together a specific set of papers — how the ideas developed and how the papers relate — introducing each paper formatted as a full Paperpile citation. Use when the user asks for an overview, a mini literature review, or the story of a field.
---

# Draft a narrative paper survey

This skill provides a structured workflow for drafting a brief, cohesive narrative that introduces and connects a specific set of research papers. Rather than producing pages of exhaustive text, the objective is to highlight the progression of ideas and present each paper using its full Paperpile-formatted citation within an accessible narrative structure.

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

## Handling empty-argument skill invocation

If this skill is invoked with no further instruction, do not guess at a task. Briefly describe what the skill does, then ask for the one thing you need to start — a topic, a set of papers, or a folder. Where the harness offers a structured question tool, use it; otherwise present numbered options and wait.

## Step-by-step workflow

1. **Define the scope and goal, find specific papers**

   - Identify the target set of papers (e.g., provided by the user, from a specific folder/label, or via a search result). If the scope is precise and well-defined within the user's library (e.g. a folder or label, or a specific list of papers), proceed. If the scope is thematic or not yet crisp, load the `find-papers` skill to search for papers to include.
   - Clarify the overarching theme, goal, or narrative thread the user wants to explore. If this is not obvious, ask the user to clarify.
   - This skill works best with a set of 5-20 papers. Too few, and the narrative will be sparse and incomplete. Too many, and the time and tokens required to summarize all full-text papers may test the user's patience or token budget.

2. **Fetch full-text content and extract evidence, using subagents**

   - For best results, all papers included in the survey should be saved in the user's Paperpile library so the full-text can be downloaded and analyzed in full detail. If some of the papers in scope are not yet saved, offer to save them now, using the `save_to_library` tool, and confirm with the user before proceeding.
   - Spin up a set of parallel generalist subagents, one for each paper in scope. Task each subagent with fetching the paper's full text and producing a compact, synthesis-oriented extraction guided by the user's desired focus and the scope of the survey.
   - **IMPORTANT**: Use the subagent prompt template below when prompting the subagents.

3. **Draft the narrative**

   - Collect outputs from all subagents.
   - Draft a high-level, concise narrative that ties the papers together.
   - First, focus on the ideal narrative structure: what key ideas, clusters of papers, or methods improvements help connect the in-scope papers over time?
   - Then, draft an outline with section headings. Evaluate that outline against the user's requested scope and the style guidelines below.
   - Finally, draft the full narrative report.

4. **Present and ask to save**
   - Present the narrative to the user in the chat.
   - Explicitly ask the user if they would like to save the generated overview as a `.md` or `.pdf` file in the current workspace.

## Narrative survey style guidelines

### Choose an organizing mode

Choose the synthesis mode that best fits the user's question and the available evidence before drafting the outline. Use these modes to guide the analysis, but describe the finished work as a formal review subtype only when its corpus, search, and analysis satisfy that methodology.

- **State-of-the-art:** Prefer this mode when explaining how a field developed. Organize the narrative around consequential changes in concepts, evidence, or research orientation. Answer three questions: Where is understanding now? How did it get here? Where should research go next?
- **Meta-ethnographic:** Use only for a corpus of qualitative studies when the goal is an interpretive synthesis. Compare and translate concepts across studies while preserving their contexts, then develop an insight that goes beyond restating the individual findings.
- **Meta-narrative:** Use when different disciplines or research traditions have framed the same topic in substantially different ways. Describe each tradition's assumptions, concepts, preferred methods, and development over time before comparing their agreements, tensions, and blind spots.
- **Critical:** State the theoretical or critical lens explicitly before using it to examine the literature. Apply the lens consistently to assumptions, omissions, power relations, or practical consequences. Clearly distinguish the papers' claims from the reviewer's interpretation.
- **Integrative:** Use when synthesizing studies with diverse empirical methods or comparing multiple theories. For empirical reviews, integrate evidence around common problems or constructs. For theoretical reviews, compare concepts and propositions, assess their limitations, and propose a refinement or extension.
- **Descriptive narrative:** Use a thematic or chronological narrative without a formal subtype label when the corpus or task does not support one of the methods above.

### Aim for synthesis rather than a catalog

- Organize sections around claims, turning points, debates, or explanatory themes. Not around one paper at a time. If the paper order could be rearranged without changing the argument, strengthen the narrative structure.
- Begin each section with its synthesis claim. Then show which papers support, qualify, contradict, or extend that claim and explain why they differ.
- Compare differences in definitions, populations, settings, methods, theoretical assumptions, and historical context when they help explain disagreement.
- Use chronology only when the sequence reveals a meaningful development. Otherwise, organize the review thematically and say so.
- Introduce each paper with its full Paperpile-formatted citation when first crediting its contribution, rather than collecting introductions in a list at the end.
- Preserve distinctions between what a study found, what its authors argued, and what the review infers across studies.

### Ground the narrative in the sources

- Carry at least one **verbatim quote** from every paper in scope through into the finished survey, and more from the papers doing the most argumentative work. A survey built only from your own paraphrase gives the reader nothing to check.
- Choose quotes that carry the claim the section is making — a stated limitation, a headline number, a sentence where the authors name what their model does or fails to do. Do not quote generic scene-setting from an abstract.
- Place each quote where it does work in the argument, next to the claim it supports, qualifies, or undercuts. Do not collect quotes into a block at the end.
- Every quote gets a Paperpile link into the source PDF, per the link format appendix — include the PDF page in both the `page` parameter and the link text. Add links for non-quoted specifics too — the figure, table, or section a number came from.
- Quotes must be verbatim and attributed to the correct paper and page. If a subagent's extraction gives you a quote you cannot place confidently, drop it rather than guessing the page.

### Represent the scope and evidence accurately

- State the review's question, scope, source corpus, and selection boundaries. Include search terms, sources, and date limits when known.
- Do not describe the review as exhaustive, comprehensive, or systematic unless a documented search and selection process justifies that claim.
- Indicate whether an important conclusion rests on one study, several independent studies, a consistent body of evidence, or a contested and heterogeneous literature.
- Report concrete results or outcome data when they are central to the argument; do not replace them with vague judgments such as "effective" or "promising."
- Give contradictory and null findings appropriate weight. Do not manufacture a smooth consensus where the evidence remains divided.
- Avoid causal or broadly generalizable conclusions that the underlying study designs do not support.

### Keep the narrative purposeful

- Open by explaining why the topic matters, what question the survey addresses, what literature it covers, and how the narrative is organized.
- Give more space to consequential contributions and unresolved tensions than to minor details. Do not allocate equal space to every paper by default.
- Use informative section headings that communicate the argument. When chronology carries the story, include date ranges in the headings.
- End by stating the current understanding, how it was reached, the most important unresolved questions, and specific directions warranted by the reviewed evidence.
- Keep the prose concise, readable, and accessible to a knowledgeable reader without relying on unnecessary academic jargon.

## Appendix: reference format

## Reference formatting

Whenever you present a paper to the user, use this four-line block. It is the format Paperpile users recognise, and it stays scannable in a terminal.

```
**Title**\
Author1 LN, Author2 LN, Author3 LN\
*Journal Abbrev* · Year · Article type · N,NNN citations\
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

**Eleven grand challenges in single-cell data science**\
Lähnemann D, Köster J, Szczurek E ... 14 more ... Schönhuth A, Rahmann S, Schreiber S\
*Genome Biol* · 2020 · Review · 1,098 citations\
[Website] · [View PDF]

- Frames the field's open problems; useful as an anchor for anything downstream of scRNA-seq.

---
```

### Note: citation counts

If you are presenting a small number of papers to the user and you don't already have citation counts available, you can make a quick call to `find_papers` with the DOI of each paper in the query_list to get citation counts.

## Appendix: link format

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

## Appendix: subagent prompt

Everything in square brackets below should be filled-in, based on the conversational context and the specific paper you're asking each agent to summarize.

<Begin: subagent prompt>
You are part of the Paperpile package of skills, meant to help users find, analyze, and read academic papers more effectively.

Your current task is to analyze the full-text of a single paper based on the instructions below.

In general, adhere to Paperpile's overall tone and style: be straightforward, specific, and concise. Avoid overly academic language, but consider your audience to be a seasoned academic in the field.

Please analyze the full-text contents of the following paper to help draft a narrative overview.

Task details:

- **Overarching Theme/Goal**: [The core goal or topic of the review, or N/A if not provided]
- **Synthesis Mode**: [The selected organizing mode and the reason it fits the review]
- **Comparison Dimensions**: [The concepts, outcomes, methods, populations, settings, or debates that matter most to the cross-paper synthesis]
- **Paper to analyze**: [Title, year, authors, citekey of the paper]

Guidelines:

- Report the `file_id` of the PDF you read at the top of your response, so the caller can build deep links into it.
- Use the `get_text_content` tool to fetch the full-text content from the paper, broken up by page ranges if needed. If no full-text content is available, use the `get_references_from_library` or `find_papers` tools to fetch the metadata and abstract.
- Extract only the material needed to compare this paper with the rest of the corpus. Do not produce a section-by-section summary.
- Identify the paper's relevant contribution, supporting evidence and methods, important limitations or boundary conditions, and relationship to the overarching theme.
- State whether the paper appears to support, qualify, challenge, or extend the review's developing account. Base this characterization only on the paper and the task details; mark relationships that require cross-paper evidence as unresolved.
- Preserve concrete outcome data when central to the argument. Distinguish reported findings, the authors' interpretation, and any inference you make for the review.
- Keep the complete extraction concise enough to scan alongside the outputs for all other papers.

Use the following output template in your response:

```
# Relevant Contribution

[State the paper's central contribution to the review in a short paragraph.]

# Evidence and Methods

[Summarize the evidence, study design, population or setting, and concrete outcomes needed to assess that contribution.]

# Limitations and Boundary Conditions

[List the qualifications that constrain how the paper should be interpreted or generalized.]

# Relationship to the Review

[Explain briefly how the paper supports, qualifies, challenges, or extends the developing account. Note relevant comparison dimensions and unresolved relationships.]

# Key Quotes

[List 3-5 direct quotes that best represent the paper's relevant contribution. Quote verbatim, and include the exact PDF page number for each — the page within the PDF, not the journal page. Favour quotes that state a contribution, a limitation, or a concrete result, since these will be carried into the finished survey.]
```

<End: subagent prompt>
