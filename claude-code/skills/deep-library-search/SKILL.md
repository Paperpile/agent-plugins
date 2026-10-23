---
name: deep-library-search
description: Run a series of deep, agentic full-text library searches to answer a specific question or find a paper in the user's library. Use when the user asks what a paper in their library found, what methods it used, whether any paper has made a certain statement, or how a set of papers differ on a point. Always load this skill before calling the search_library tool for important guidance and best practices.
---

# Deep library search

This skill provides documentation and guidance for performing an iterative, deep search of a user's library,
making use of Paperpile's full-text search capabilities to deeply interrogate the contents of a user's collected
references. The major mode of action is to search full-text for certain keywords, then extract surrounding
portions of the full-text content to better understand the context and meaning of each resulting match.

This deep agentic search process helps ensure a user's question is answered with source-grounded information
from within each paper, not merely from abstracts or from the agent's memory.

Each claim reported to the user should be traceable (and, if possible, linked) to a specific quote or section
from within a paper that was actually read by the agent.

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

## Handling empty-argument skill invocation

If this skill is invoked with no further instruction, do not guess at a task. Briefly describe what the skill does, then ask for the one thing you need to start — a topic, a set of papers, or a folder. Where the harness offers a structured question tool, use it; otherwise present numbered options and wait.

## Shared libraries

Every library tool works on the personal library unless told otherwise. When the user means a shared
one — "the lab's library", "our group's folder" — call `get_libraries` first and pass the id it returns
as `library_id` to `search_library`, `get_references_from_library`, `get_text_content`,
`highlight_text`, `save_to_library`, `update_references` or `update_collections`. The catalog tools
search the literature rather than a library and take no `library_id` at all.

`get_collections_from_library` is the exception that already spans them: it returns folders and labels
from every shared library you can reach, unless you set `include_shared_libraries: false`.

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

## search_library in detail

This tool searches three things at once: the reference's own metadata, the text inside its PDF, and any
highlights or notes on that PDF.

### Writing the query

`q` takes plain words, quoted phrases, and field prefixes.

| Form          | Example                                   | Matches                                 |
| ------------- | ----------------------------------------- | --------------------------------------- |
| Plain words   | `substitution rate`                       | Records containing both words, anywhere |
| Quoted phrase | `"episodic diversifying selection"`       | Those words, in that order              |
| Field prefix  | `title:codon`, `author:Yang`, `year:2000` | That field only                         |
| PDF text only | `pdf:"maximum likelihood"`                | The body text of the PDF                |
| Exclusion     | `not:review`                              | Drops records containing the word       |

The prefixes are `title:`, `author:`, `abstract:`, `journal:`, `year:`, `publisher:` and `pdf:`. There
are no others. An invented prefix — `note:`, `keyword:`, `doi:` — is not an error; it simply matches
nothing at all, which looks exactly like an empty library. If a query returns zero results, check that
every prefix in it is on that list before concluding anything.

`not:` is blunter than it looks. It excludes a paper if the word appears _anywhere_ in the record,
including deep inside the PDF, not just in the field you were narrowing. `title:codon not:substitution`
returns nothing in a library full of codon papers, because every one of them says "substitution"
somewhere on page four. Use `not:` on words that would only ever appear in the metadata, and check the
result count before trusting it.

Pass up to five separate queries as an array and they run in parallel, with results grouped in the
order you gave them. This is the single biggest improvement you can make to a vague request — see the
strategies below.

### Other search_library tool parameters

- **`output_format`** selects `MARKDOWN` (default, reference cards with all returned matches), `MINIMAL`
  (one line per match, with citekey and location but no file ID), or `JSON` (citation metadata grouped
  with structured matches). Use `JSON` when you need exact file or annotation identifiers.
- **`search_full_text: false`** turns off PDF text and annotations, leaving only the reference details.
  This is the fix for a query that drags in every paper merely mentioning the term in passing. Remove
  any `pdf:` clause at the same time — the combination is rejected outright, not ignored.
- **`folder_id`** or **`label_id`** narrows to a collection. One or the other, never both. Get the id
  from `get_collections_from_library`, and resolve it every single time: a folder _name_ passed here is
  not rejected, it just matches nothing.
- **`limit`** and **`offset`** page through results, and count _papers_, not matching passages. They
  only work with a single query — passing them alongside an array of queries is rejected.
- **`count`** decides whether you get a total: `"skip"` (the default, no total), `"include"` (results
  and total), `"only"` (the total alone). Use `"only"` when the question is "how many of my papers
  mention X" — it is far cheaper than fetching them.
- **`include_trashed`** brings back deleted references. Leave it off unless the user is hunting for
  something they think they deleted.

### Reading the results

One paper can have several matches: its metadata, passages from its PDF, and highlights or notes.
The default `MARKDOWN` output groups them under one citation card per reference. `MINIMAL` has one line
per match, so the same citekey can occur more than once; deduplicate citekeys before counting papers.

In `JSON`, each query returns `data: [{ reference, matches }]`. `reference.id` identifies the paper;
the reference includes its citekey, canonical title, abbreviated authors, journal, publication date
(`published`), type and available link identifiers. Attachments use the standard `files` objects,
including their `id`, `name` and `primary` flag. Highlighted fields belong to `matches`, not to that citation metadata.
An array of queries returns `{ results: [...] }` in input order. Result fields are camelCase,
unlike the snake_case parameters going in.

Each match has a `resultType`:

- **`reference_metadata`** — matched on title, authors, year, journal or abstract. `matchedFields` says
  which. Carries the title, authors, year, journal and abstract.
- **`fulltext`** — matched inside the PDF. Carries `snippet`, `fileId`, `pageNumber`, and `charOffsets`.
- **`pdf_annotation`** — matched in one of the user's own highlights or notes, plus an `annotationId`.
  These are worth calling out when you find them: the user already marked that passage as important.

`total` is the number of matching papers across all pages and only appears when `count` asks for it.
`resultCount` counts returned matches; `referenceCount` counts distinct references returned on this
page. A count-only response has a total but no matches — it does not mean nothing matched.

Matched words come back wrapped in `**` inside the text. Strip that before quoting anything.

`fileId`, `pageNumber` and `charOffsets` can be handed straight to `get_text_content` to read the
surrounding context. Once you have a file ID, page number, and quoted text in hand, you can pass to
`highlight_text` to mark the passage permanently. Or, create a Paperpile link so the user can click
through to that exact spot.

## get_text_content in detail

When searching a user's library, `get_text_content` can be useful to extract the text surrounding a search
result to better understand the context. Or, if you've found a matching paper or section that needs reading
in more detail, you can fetch a longer stretch of text for deep analysis.

Name the paper by `citekey` (or `reference_id`) to extract from the main PDF; `file_id` picks a specific
attachment.

`ranges` accepts up to 50 ranges from a given file:

- `{ "page": 4, "start": 100, "end": 500 }` — page-local UTF-8 bytes, start inclusive/end exclusive.
- `{ "page": 4 }` — the whole page.
- `{ "page_start": 4, "page_end": 9 }` — fetches pages 4 to 9, inclusive (six total pages of text).
- `{ "page_start": 1, "page_end": 2, "start": 3000, "end": 550 }` — page 1 from byte 3000 onward and the first 550 bytes of page 2.

Omit `ranges` to read all available pages. `start` must be zero or more; a negative `end` counts back from that page's end.

For a `fulltext` search hit, pass its `fileId` as `file_id`, `pageNumber` as `page`, and `charOffsets`
as `start`/`end`. Widen with `Math.max(0, start - context)`: a negative `start` is rejected. For missing offsets or annotation hits, fetch the whole page.

Text is normalized for search, so accents and ligatures may differ from the PDF. These byte offsets
belong to this extraction and file; use page numbers/passages for citations. Missing extraction
returns an error unless the host has a compatible fallback. Reading several files takes separate calls.

For papers with no PDF attached, and for downloading PDFs to disk in bulk, see the
`auto-highlight-papers` skill.

## Search strategy

### Settle the scope before searching

Three different questions look alike and need different work. Decide which one you have.

| The user means                           | Where to look                                          |
| ---------------------------------------- | ------------------------------------------------------ |
| "What did that paper say about X?"       | Their library, or the few papers they named            |
| "Which of my papers on X used method Y?" | A folder, a label, or a search of their library        |
| "Has anyone ever shown X?"               | The published literature — use the `find-papers` skill |

If the conversation does not make this obvious, ask before searching. Do not read a folder because it
happened to be nearby, and do not quietly widen a library question into a literature-wide one.

A reasonable default when it is genuinely ambiguous: search the library first. It is faster, and a hit
there is the better answer anyway, because the user can open the PDF and check it.

### A good default: find the passage, then read around it

This is the move that makes the whole skill work, and it is worth doing in this order every time.

1. **`search_library`** finds short passages inside the PDFs — a sentence fragment at a time. Enough to
   tell you _which_ paper and _which_ page, not enough to answer anything.
2. **`get_text_content`** then reads the surrounding context or full pages, so you can see the claim in context,
   quote it accurately, and check that it says what the fragment suggested.

Search finds a narrow match; reading confirms in wider context. `get_text_content` takes up to 50 ranges
per tool call, so you can parallelize extraction from multiple search results at once.

### General best practices

**Run several queries at once.** Generate four or five plausible phrasings and pass them as an array
rather than trying one, reading the results, and trying another. Library search is keyword-based, so
wording matters more than you would expect.

**Vary the search vocabulary, not the length.** Search for the words a methods section would actually use, not
the concept the user named. Include British and American spellings, the abbreviation and the expansion,
the tool name and the technique name.

**Start narrow, then broaden.** A specific quoted phrase either lands the paper or returns nothing, and
both outcomes are informative. When it returns nothing, drop to two or three plain words. When _that_
returns nothing, the paper is probably not in the library — say so rather than searching a fifth time.

**Too many results, or too noisy** — restrict to a folder, set `search_full_text: false`, or add a
`not:` term. A term that appears in every paper's reference list is the usual culprit.

**Half-remembered papers.** When the user recalls an idea rather than a title, the detail they remember
is usually buried in the discussion, not the abstract — this is exactly what full-text search is for.
Run their description several ways in parallel, and ask for the one extra detail that would narrow it:
roughly when they read it, who wrote it, what it was about.

### Answering a specific question from several papers

When there are more than three or four candidate papers, and the question needs extended reading rather
than a single lookup, hand each paper to its own subagent — a separate helper working on that one paper
alone — and collect their answers. Each returns whether its paper answers the question, with quotes.

Subagents run through the Task tool, general-purpose type, at most 10 at once.

- Do not start them in the background: a subagent may need approval to read files in a subdirectory, and a backgrounded one cannot ask for it.
- Give each one the prompt below with the bracketed values filled in, and nothing else. It should not load other skills.

Say up front which papers you are reading and roughly how many, so the user can stop you if the scope
is wrong. Papers that could not be read are simply missing from the answer: name them.

### When the library does not have the answer

If the question was never really about the user's own collection — "has anyone shown X", "is there work
on X" — a library search is only the first half. Say plainly what the library did and did not have,
then use the `find-papers` skill to search the published literature.

Do not silently substitute one for the other. "Nothing in your library, but three papers in the
literature" and "three papers" are very different answers.

### Knowing when to stop

If two or three rounds of searching and reading have not produced a clean answer, stop and report what
you have and have not found, then ask whether to keep going. Do not spend ten minutes silently combing
the literature before checking in.

## Presenting the answer

**Quote the papers directly.** A summary in your own words gives the user nothing to check. Use the
paper's own sentence wherever the exact wording carries the claim — a headline number, a stated
limitation, the authors saying what their method does or does not do — and give every quote a Paperpile
link into the PDF at the right page, per the Paperpile PDF links guidance above. Add links for specifics you
did not quote too: the figure a number came from, the section a method is described in.

**Treat full-text search results as quotes.** When presenting a `fulltext` hit, quote its `snippet` and
link directly to that passage in the PDF, even in a brief list of search results. Use the hit's `fileId`
and `pageNumber`, and set the `#hl` fragment to the snippet text you display, stripped of search
`**` markup and encoded according to the Paperpile PDF links guidance above. Use the matching
attachment, which may be a supplementary PDF. Prefer these quote links wherever a search excerpt
helps explain why a paper is relevant; they let the user open and verify the exact passage in one click.

Abstract matches can be quote-linked too when the reference has a PDF. Resolve the PDF attachment's
ID from the reference's `files` and use the verbatim abstract passage you display as `#hl`, with the
same markup removal and encoding rules. Include the PDF page when known; an abstract metadata match
alone does not establish its page number.

**IMPORTANT: Present a reference for each paper contributing to the answer**, formatted in Paperpile style.
Present each formatted reference when you introduce it for the first time in the response.

**Highlight where papers disagree.** This is usually an interesting jumping-off point for a researcher, if prior
work disagrees about a particular point or conclusion.

**Be explicit about what you could not establish**: papers with no PDF, a question the text does not
settle, a claim resting on a figure you cannot read. An honest partial answer beats a confident one
built on two papers out of five.

## Next steps

Unless the user has already said what happens next, offer whichever of these fits:

1. **Save the evidence** — `highlight_text` marks the supporting passages in the PDFs, with a note on
   why each matters, so the reasoning outlives this conversation. Offer this whenever the answer rested
   on specific passages.
2. **Write it up as a narrative** — the `narrative-paper-survey` skill turns the papers you just read
   into a short piece on how the ideas connect.
3. **Build a table** — the `extract-paper-data` skill, when the question turned out to have one answer
   per paper worth lining up side by side.
4. **Find what is missing** — the `find-papers` skill, to search the literature for work the library
   does not have, and save it.

## Appendix: subagent prompt

Fill in everything in square brackets from the conversation and the specific paper you are handing over.

<Begin: subagent prompt>
You are part of Paperpile's research skills. Read the full text of one paper and answer a question from it.

Be straightforward, specific and concise. Your reader is a seasoned academic in the field.

- **Question**: [the user's question, verbatim]
- **Paper**: [title, year, authors, citekey]

How to work:

- Report the `file_id` of the PDF you read at the top of your response, so the caller can build links
  into it.
- Use `search_library` with a `pdf:` term to locate the relevant passages, then `get_text_content` to
  read the pages around them. Read the section the question lives in — a question about method is
  answered by the methods section — rather than the whole paper.
- If the paper has no PDF, say so and answer from the abstract if you can, marking it clearly as an
  abstract-only answer.
- Quote the paper rather than paraphrasing wherever the exact wording carries the claim.
- If the paper does not answer the question, say so. Do not stretch a partial match into an answer.

Reply in this shape:

```
# File

[The file_id of the PDF you read, or "no PDF".]

# Answer

[Whether and how this paper answers the question. Two or three sentences.]

# Notes

[Bullets: your reasoning, relevant figures or tables, caveats, sample sizes — whatever a reader needs
to judge the answer.]

# Quotes

[Direct quotes supporting the above, verbatim, each with the page number within the PDF.]
```

<End: subagent prompt>
