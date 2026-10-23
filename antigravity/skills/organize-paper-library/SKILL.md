---
name: organize-paper-library
description: Organize the papers in your Paperpile library. Provides a guided workflow to file unsorted papers into folders and labels, propose a folder structure that fits what is actually in the library, and clean up empty or duplicated collections. Use when the user asks to tidy, sort, categorize or restructure their library.
---

# Organise a paper library

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

## IMPORTANT RULE: no destructive actions without explicit user review and approval

No destructive or modifying actions (updates, creates, deletes) should EVER be taken without explicit user review and approval.

You must present the proposed changes clearly in markdown (e.g., a representative table showing what folders will be created or
how references will be tagged) and wait for the user to say "approve" or similar before executing any mutation tools.

Be especially careful with deletion: deleting a folder can detach many references at once. If `trash_references: true` is set,
everything moves to the trash. Never pass that flag unless the user explicitly asks for and reconfirms deletion.

## Where to start

Invoked with no direction, offer these and let the user pick:

1. **Analyze my library and give me a set of options** — Run a quick structural analysis and suggest high-priority organization tasks.
2. **Organize folders and labels** — Identify gaps in the folder/label structure and create new entries.
3. **Organize references** — Find untagged/unorganized papers and categorize them.
4. **Clean up duplicates and empty collections** — Find redundant entries and unused collections to tidy up the library.
5. **Something else** — Let the user describe custom requirements.

Highlight that no modifications will occur without approval.

## Workflows

### Analyze library structure and make recommendations

`get_collections_from_library` returns every folder and label with its hierarchy, colour and reference
count. `get_references_from_library` with `random_sample: true` and `limit: 100` gives a representative
sample of titles, journals and collections, which is what tells you what the library is actually about.
Stay on the default `MARKDOWN` output here — the `JSON` sample is several times larger and its extra
fields do not help a survey.

**Goal**: Get a bird's-eye view of the user's library and present a prioritized task list.

1. Call `get_collections_from_library` to retrieve all folders, labels, hierarchies, and item counts.
2. Call `get_references_from_library` with `random_sample: true`, `limit: 100` and
`output_format: "MINIMAL"` to understand the general domain/theme of references in the library.
3. Analyze:
  - Are there collections with 0 items?
  - Are there many papers not categorized in any folder or label?
  - Are there folders/labels with overlapping names (potential duplicates)?
  - Are there clear semantic themes in untagged papers that could fit into existing collections or warrant new ones?
4. Present a prioritized list of recommendations using markdown bullet points, detailing what actions you suggest and why.
  - Where it makes sense, recommend one or more of the specific guided workflows below.
  - For a library with minimal existing organization, recommend starting with "Organize folders and labels" followed by "Organize references".

## Organize folders and labels

**Goal**: Dynamically discover domain-specific organizational categories to recommend.

Read the current structure with `get_collections_from_library`, then sample with
`get_references_from_library` and pull out the recurring research themes, methods and subfields.

1. Call `get_collections_from_library` to map the current taxonomic layout.
2. Call `get_references_from_library` with `output_format: "MARKDOWN"`, `limit: 300` and `random_sample: true` to extract key research themes, disciplines, or keywords.
3. Identify semantic gaps. For instance, if the user has many papers on "transformer architectures" but no folder or label for NLP or Deep Learning, propose adding them.
4. Present the user a list of proposed new folders/labels with their parent/child hierarchies or colors. Format as a clean markdown tree structure.
5. **Wait for explicit user approval**.
6. Once approved, call `update_collections` with `action: "create"` to batch-create the new collections.

## Organize references

**Goal**: Help file away papers that are unsorted or lack folders and labels.

IMPORTANT: The goal is to organize as many references as possible. You should try very hard to align a given reference with a folder in the user's library. Each instance of a reference that is left unorganized MUST be reported back to the user as an exceptional event. This should be very rare.

When starting this workflow, first give the user a preview of how a set of 10 papers will be organized:

1. Call `get_references_from_library` with `output_format: "MARKDOWN"`, `filter_for_unorganized: true`, and `limit: 10` to get a set of unorganized references.
2. For each paper, analyze the title, abstract, and metadata to determine the best folders / labels.
3. Present a table containing: Paper Title, Proposed Folders, Proposed Labels.
  - Present the user with two options:
    a. Proceed with organizing the rest of your library.
    b. Clarify additional guidance or rules for library organization.
  - Wait for explicit user approval.
4. Invoke `update_references` to apply the folders & labels for the first 10 references

To handle organizing the rest of the repo, spawn a single general-purpose subagent with the prompt from the appendix.

### Subagent workflow for organizing references

IMPORTANT: This workflow describes how a subagent can autonomously walk through a user's library to automatically organize references which
need organization. If the current context is a subagent, IGNORE all other workflows and user interactions. Your job is to organize autonomously.

Workflow:
- Call the `get_collections_from_library` tool ONCE to get the full set of folders and labels.
- Process 10 references at a time:
  - Call the `get_references_from_library` tool with `limit: 10` and `filterForUnorganized: true`.
  - Identify the appropriate set of folder(s) and label(s) for the current set of 10 references, then call `update_references` to save the changes.
  - If any references were left unorganized, increment the skip value and include the "skipped" reference in the next message to the main agent.
- Send a message to the main agent with a status update after each 100 references are processed.
- Continue until you've processed all papers up to your TARGET_COUNT value.

IMPORTANT NOTES:
 - Do NOT write code to help with this task. Use your internal judgment and make Paperpile tool calls directly.


## Clean up duplicates & empty collections

**Goal**: Prune empty folders/labels, and merge duplicate collections or duplicate papers.

1. Call `get_collections_from_library`.
2. Identify:
   - Empty folders/labels (`item count: 0`).
   - Duplicate or near-identical collection names (e.g., "DeepLearning" and "Deep Learning").
4. Present the cleanup proposal:
   - Collections to delete.
   - Collections to merge (and where to reassign papers).
5. **Wait for explicit user approval.**
6. Once approved:
   - Call `update_collections` to delete empty/merged folders and labels.
   - Call `update_references` to reassign references from deleted/merged collections.


## Next

A tidy library is the point at which a saved search becomes useful — new papers on a topic landing in
the right folder. `find-papers` covers the search side.

- With a cleaned-up library, the user may want to set up a saved search that can continually find and
  save new papers in an appropriate place. Load the `scheduled-paper-search` skill first and offer this
  only when its support rules say the current product surface can create schedules.

## Appendix: subagent envelope

Give each subagent the envelope below with the bracketed values filled in, and nothing else.

Fill in everything in square brackets from the conversation and from the specific task you are handing over.

<Begin: subagent envelope>
You are part of Paperpile's research skills.

## Execution context

You are running as a **background library organization subagent** inside a larger `organize-paper-library` run.
Your first action must be to load the `organize-paper-library` skill that defines this job.

That skill describes a few different workflows and user approval flows. As the subagent, you must focus ONLY on the
"Subagent workflow for organizing references" section. That describes your main role and mode of operation.

## Task properties

- TARGET_COUNT: [target paper count, e.g. how many references should this subagent handle]
- Input from user: [any relevant input from the user on how references should be organized]

Use your own judgement and call the tools directly. Do not write a script for this, and do not load other skills beyond
`organize-paper-library`.

<End: subagent envelope>
