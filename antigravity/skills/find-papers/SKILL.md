---
name: find-papers
description: Find academic papers and preprints and follow citations between them. Use when the user asks for preprints or papers on a topic, by an author, in a journal, citing or cited by a given work, or mentions PubMed, arXiv, or other scholarly literature sources. Load this skill before calling find_papers - this guidance improves its effectiveness. Prefer using these tools over calling individual databases or literature search engines directly via API; they are more performant and token-efficient.
---

# Find papers

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

## Library or literature

Decide from the conversation whether the user means papers they already have, or papers they do not.
"my library", "my folder", "papers I saved" mean library-scoped; anything else is usually the literature.
When it is genuinely ambiguous, search the library first — it is cheaper and a hit there is the better
answer.

**Library-scoped** — `search_library` for a query, `get_references_from_library` to lookup by IDs or
enumerate without a query.

Both narrow by `folder_id` or `label_id`, and `get_collections_from_library` turns a folder or label name
into the id they take. Resolve it every time: a name is not rejected, it simply matches nothing, which
reads exactly like an empty folder.

**Literature-scoped** — `find_papers` against the external catalogs, then `get_inbound_cites` and
`get_outbound_references` to walk outwards from anything promising.

If a library search comes back empty, say so before widening to the literature. Do not silently
substitute one for the other.

## The tools

These search and reference tools take `output_format`: `MARKDOWN` (default, compact reference cards),
`JSON` (structured metadata — ask for it when you need to read fields), and `MINIMAL` (one line per
paper, or per matching passage for `search_library`). Catalog and reference JSON includes full metadata;
library-search JSON includes concise citation metadata and all returned matches.

### find_papers

Searches external catalogs. `query` for a single search, `query_list` for up to 10 run in parallel and
deduplicated into one list. `duplicates_removed` appears only when something was actually merged, and
in `JSON` each paper carries the `query_index` that found it. `total` counts the papers returned;
`query_matches` reports how many each query matched in the catalog, which is the number to read when
deciding whether a query was too narrow or too broad to rerun as written. `limit` applies per query, up to 200. Filters: `year_range` (`"2020"` or `"2015-2024"`), `author`, `journal`, `min_citation_count`.
`sort` is `relevance` (default), `date` or `citation-count`.

Choose `engine` deliberately — it changes the results more than the query does:

- `semantic-scholar` (default) — best general free-text relevance, accurate citation counts.
- `open-alex` — use for author searches. It resolves a name to a specific researcher; Semantic Scholar
  matches the name as free text and returns papers that merely mention them. Also the only engine that
  sorts a citation list.
- `pubmed` — life sciences only, and no preprints. It carries no citation counts, so
  `min_citation_count` and `sort="citation-count"` are rejected outright rather than ignored.

Query syntax differs between them, and a query written for one is matched literally by another:
Semantic Scholar takes plain text only; OpenAlex ANDs terms and understands `OR`, `NOT` and
`"quoted phrases"`; PubMed takes its own full syntax, including field tags like `[tiab]` and automatic
MeSH mapping. `sort="date"` and `sort="citation-count"` on Semantic Scholar switch to a boolean matcher
over title and abstract that requires every term, and reach only the first 1,000 results.

Never put an author or journal name in `query`; use the `author` and `journal` parameters. If a search
returns nothing, try another engine before rewording — coverage differs more than ranking does.

A DOI in `query` is resolved to that one paper rather than searched, so pasting one in is safe.

Set `mark_in_library: true` when the user is deciding what to save or read, so results the user already
has come back tagged with their citekey. It makes the search slower, so leave it off otherwise.

### search_library

Searches the user's library across metadata, PDF full text and annotations. `q` takes plain terms,
quoted phrases (`"deep learning"`), and field prefixes: `title:`, `author:`, `abstract:`, `journal:`,
`year:`, `publisher:`, `pdf:`. `not:` excludes a term — `title:transformers not:review`.

Pass up to five `q` values to search in parallel; results stay grouped in input order. `limit` and
`offset` only work with a single `q`.

Narrow with `folder_id` or `label_id` (one or the other, never both). Set `search_full_text: false` to
search metadata only, which is the fix for a query that drags in every paper that merely mentions the
term in its PDF — but drop any `pdf:` clause at the same time, or the call is rejected.

`MARKDOWN` groups all returned matches under a reference card with citation metadata and file IDs.
`MINIMAL` gives one line per match with the citekey, location and excerpt, omitting file IDs. `JSON`
returns `data: [{ reference, matches }]`: `reference.id` identifies the paper, and its citation metadata
is separate from the highlighted matches. Batched queries return `{ results: [...] }` in input order.
Citation summaries use `published` for the publication date and `files` for attachment objects, as in
reference-list responses. The `primary` file is the main article PDF.

Each JSON match carries a `resultType`, and the fields are camelCase here, unlike the snake_case parameters:

- `reference_metadata` — matched on title, authors, year, journal or abstract; `matchedFields` says which.
- `fulltext` — matched inside the PDF. Carries `snippet`, `fileId`, `pageNumber`, and UTF-8 `charOffsets`.
  Take fulltext results and send to `get_text_content` with `{ page, start, end }` to get the surrounding context.
- `pdf_annotation` — matched in a highlight or note. Carries `snippet`, `fileId`, `pageNumber`, and `annotationId`; read the whole page with `get_text_content` for more context.

The matched terms come back wrapped in `**` inside `snippet` and metadata match fields. `total` counts
matching references across all pages when `count` asks for it; `resultCount` counts returned matches,
and `referenceCount` counts distinct references on this page. Count-only calls return no match cards.

Those `fileId` and `pageNumber` values are the useful part: they hand straight to `get_text_content`
(read the surrounding pages) or `highlight_text` (mark the passage), so a full-text search is the
cheapest way to find what is worth reading.

### get_inbound_cites and get_outbound_references

`get_inbound_cites` returns what cites a DOI — who built on the work. `get_outbound_references` returns
its reference list. Both page with `limit` (up to 50) and `offset`. Page on `has_more` rather than on
`total` — Semantic Scholar's citation endpoints do not report one.

Both tools can sort by `CITATION_COUNT` or `LATEST`, but **only on `open-alex`** — the sort is
ignored on the Semantic Scholar default, so pass the engine when the ordering is the point. A landmark
paper can have thousands of citations, so iterating through is infeasible: decide from the citation
count and what the user actually wants whether they need the most recent or the most influential, and
sort for that instead.

An empty reference list does not mean the paper cites nothing. Publishers withhold reference lists and
coverage differs between catalogs, so ask the other engine before reporting it as empty.

A DOI minted by arXiv (`10.48550/arXiv.…`) is frequently absent from OpenAlex even when the paper is
there, and the call fails outright rather than returning nothing. That is a coverage gap, not a paper
with no citations — retry on `semantic-scholar`, or use the DOI of the published version.

### lookup_papers

Full metadata for up to 100 DOIs, without saving anything. Useful to fill gaps — PubMed results have no
citation counts, so a follow-up `lookup_papers` gets them. DOIs with no record come back under
`not_found` rather than being dropped.

## Search strategy

**Run several queries in parallel.** When the request is broad or loosely worded, this is the single
biggest improvement you can make. Generate five or six plausible phrasings and pass them as
`query_list` (or up to five `q` values to `search_library`) rather than iterating one at a time.

**Vary the wording, not just the length.** Most academic databases use keyword-based search engines, so
use parallel search queries with variations in word choice. Also consider spelling variants (British and American).
Query for the concrete thing a methods section would say rather than the abstract concept the user
named.

**Match query length to what you want.** A short query of two or three words returns a broad pool to
browse; a long, title-like query is relevance-ranked and puts a specific paper at the top, which is
what you want when you already know which paper you are after. What you cannot do is get both from one
query: adding terms narrows the match set sharply, so breadth comes from running
several short queries in parallel rather than from one long one.

**Too few results** — drop keywords, or drop specificity: "mSandy2 chromophore p-hydroxybenzylidene
Leucine 63 rotamer" -> "mSandy2 chromophore structure".

**Too many, or too noisy** — add `year_range`, `min_citation_count`, a folder, or turn off
`search_full_text`.

**Author name variants** — give the full name in `author` and let Paperpile format it for the engine.
If nothing comes back, shorten rather than lengthen, and prefer family names: "Gregory Jordan" → "Jordan".

**Start from the anchor papers.** For most topical requests the best opening move is a broad query with
the default `relevance` sort and a `min_citation_count` floor. It surfaces a field's landmark work
without changing the ranking or which papers match. Try 100 for a field's notable work and 500 or more for landmarks:
`find_papers(query="codon model positive selection", min_citation_count=500)`.

When using citation count thresholds, restrict to papers at least a year or two old so citations have had time to accrue — six to twelve
months in fast-moving areas — when the request is about recent work: `find_papers(query="mutation rate estimation mammals", min_citation_count=100, year_range="2023-2025")`.

**Recent work** — when the user says "recent" or "lately", set `year_range` to the last year or two
rather than trusting relevance to surface new work. When they say "the latest", that is `sort="date"`.

**Preprints** — Semantic Scholar and OpenAlex both index arXiv, bioRxiv, and other preprint sources. For the latest from one of
them, query with `journal="arxiv"` or `journal="biorxiv"` and `sort="date"`.

## Workflows

### Find one specific paper

Aim for a query that puts the target in the top five to ten. Try, in order, whatever the user's input
supports: the title; a broad `query` with a specific `author`; `author` with `year_range`. If none of
that lands it, use your own web search to identify the paper, then come back with the DOI or exact
title — the catalogs are precise once you know what you are asking for, and poor at guessing.

Found it — present it in the format above, with a one-line summary drawn from the abstract unless the
user asked for something else. Then offer to save it with `save_to_library`.

Not found — say so plainly and ask for anything that narrows it: a coauthor, the year, where they saw
it. Google Scholar plus the Paperpile browser extension is the better route for a paper the catalogs do
not have.

### Track citations to a paper

The standing academic use case: what has cited my work, or work I follow.

For each paper, call `get_inbound_cites` on both `semantic-scholar` and `open-alex` — their coverage
differs — with `sort="LATEST"` on OpenAlex. Expect the OpenAlex call to fail for a preprint's arXiv
DOI; carry on with the Semantic Scholar results rather than reporting no citations. Merge, drop
duplicate DOIs, and present.

Then offer the obvious next steps: save the citing papers, or read them to find out _how_ they cite the
original (see the `deep-library-search` skill). For a standing alert rather than a one-off check,
point the user at Google Scholar alerts.

### Latest from an author or a journal

For an author, use `open-alex`. If the results look like a different person, that is exactly the failure
`open-alex` is meant to prevent — say so and ask the user to confirm an affiliation or a known paper.
`pubmed` is a reasonable second choice in the life sciences.

For a journal's latest issue, query with `journal` set, `sort="date"` and a high `limit`, on
`semantic-scholar`. Volume and issue are only in the `JSON` output, so ask for it if you need to group
by issue. Recent online-first papers often have neither yet — include them, and say which ones they are.

### Find related work

There is no "similar papers" tool, so build it from the parts:

1. Anchor on the paper or papers the user means — `lookup_papers` if you have DOIs,
   `search_library` if they are in the library, `find_papers` otherwise.
2. Read the anchors' abstracts and pull out the recurring terms, methods, authors and venues.
3. Run those through `find_papers` as a `query_list`, with a `year_range` or `min_citation_count`
   suited to the field.
4. Present each result with one line on _why_ it relates to the anchor. That line is the deliverable —
   a list without it is just another search.

### Find a folder's citation gaps

For a well-scoped folder, or a handful of anchor papers, the papers they _all_ lean on are a good
proxy for the field's foundations. The ones missing from the library are the gaps worth filling.

1. `get_references_from_library` with `folder_id` for the DOIs, or take the anchors the user named.
2. `get_outbound_references` on each, paging to the end — a partial list looks like a paper with few
   citations in common when it is only an unread page. Expect some publishers to withhold the list
   from Semantic Scholar; re-read those on `open-alex` before concluding anything.
3. Count how many anchors cite each DOI, drop the ones already in the library, and rank by that count.
4. Present the multi-cited works, then say which you would actually act on.

Two things to say out loud rather than let the count imply them. Reference lists differ wildly in
length — a Nature Methods brief communication cites eight works, a phylogenomics paper a hundred — so
a short-list paper barely participates and its own foundations go undetected; name the imbalance.
And a co-citation count promotes methodological furniture, the aligners and tree viewers everyone
cites, above the substantive work. Separate the two in what you present, and note anything a
threshold of two would have missed — a field's current review article is often cited by only one
anchor.

The result is only as good as the folder is coherent. On a folder holding several unrelated topics
the overlap is near zero, which is a finding about the folder rather than the literature.

### Survey how a field developed

Ask first if the request is one line: a subfield summary of ten papers and a hundred-paper review are
different jobs.

Find three to five highly-cited anchors from two or three years back (nine to twelve months in
fast-moving areas), then walk both directions from them — `get_outbound_references` for what they built
on, `get_inbound_cites` sorted by `CITATION_COUNT` on `open-alex` for what built on them. In
biomedicine a review article is usually the best anchor.

With twenty or so on-target papers, write the summary from their abstracts: how the ideas moved, not a
list. Put each paper's full reference block inline where you first mention its contribution.

## Answering a question, not just finding papers

If the request has a question inside it — "has anyone shown X", "which of these used method Y", "what
did the X paper find" — this skill only gets you the candidates. Use it first, then hand the results to
`deep-library-search`, which reads the full text.

## Next steps

Unless the user said what happens next, offer it:

1. **Save to the library** — `save_to_library`, organised into a folder or label.
2. **Ask a question** of the papers, answered from their full text (see `deep-library-search` skill)
3. **Summarise the trend** across a set of papers (see `narrative-paper-survey` skill)
4. **Extract data** from them into a table (see `extract-paper-data` skill)
5. **Create a periodic saved search** to continually find relevant papers, when the current product
   surface supports scheduling (load `scheduled-paper-search` before offering to create one)
6. **Find the citation gaps** — when the papers sit in a coherent folder, or the user has a few clear
   anchors, offer the co-citation pass above: what these papers all build on that is not yet saved.
