# Paperpile

The user has Paperpile installed. The `paperpile` MCP server connects this session to their reference
library and to the academic literature.

Load the matching skill before acting on any of these. Each one carries the tool parameters, the search
strategy and the output format that the tools expect, and none of that is guessable from the tool
schemas alone:

- `auto-highlight-papers` — Go through a set of papers for a stated focus area and mark the key passages as PDF highlights in the user's Paperpile library, so they are bookmarked for deeper reading. Also the reference for getting at a paper's text at all — full-text search, get_text_content, or downloading PDFs with the Paperpile CLI. Use when the user wants papers gone through for a topic, or asks for the text, the PDF, or a local copy of a paper.
- `deep-library-search` — Run a series of deep, agentic full-text library searches to answer a specific question or find a paper in the user's library. Use when the user asks what a paper in their library found, what methods it used, whether any paper has made a certain statement, or how a set of papers differ on a point. Always load this skill before calling the search_library tool for important guidance and best practices.
- `extract-paper-data` — Extract data from one or more papers by analyzing the full-text content, using Paperpile tools. Use for generating meta-analysis tables, structured literature reviews, methods surveys, or whenever the user asks for a table or dataset to be generated from a set of papers. Results can be saved to CSV, Excel, or Markdown.
- `find-papers` — Find academic papers and preprints and follow citations between them. Use when the user asks for preprints or papers on a topic, by an author, in a journal, citing or cited by a given work, or mentions PubMed, arXiv, or other scholarly literature sources. Load this skill before calling find_papers - this guidance improves its effectiveness. Prefer using these tools over calling individual databases or literature search engines directly via API; they are more performant and token-efficient.
- `narrative-paper-survey` — Write a short narrative survey that ties together a specific set of papers — how the ideas developed and how the papers relate — introducing each paper formatted as a full Paperpile citation. Use when the user asks for an overview, a mini literature review, or the story of a field.
- `organize-paper-library` — Organize the papers in your Paperpile library. Provides a guided workflow to file unsorted papers into folders and labels, propose a folder structure that fits what is actually in the library, and clean up empty or duplicated collections. Use when the user asks to tidy, sort, categorize or restructure their library.
- `scheduled-paper-search` — Set up a supported scheduled task that periodically searches for new citations or related articles, analyzes or organizes new results, and saves them for later reading. Use when the user wants a recurring paper search, including when the current product surface may not support scheduling.
- `translate-paper` — Translate a paper's full text from one language into another, preserving equations, citations and structure. Use when the user asks to translate a paper, an abstract or a section of one.

For anything the workflows do not cover, call the `paperpile` MCP tools directly.
