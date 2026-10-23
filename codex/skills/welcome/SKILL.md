---
name: welcome
description: Introduce the Paperpile integration for Codex and suggest where to start. Use when the user asks what Paperpile can do here, or invokes this with no instruction of their own.
---

# Paperpile for Codex

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

If the user gave an instruction, skip the introduction and route them straight to the workflow that fits.

Otherwise, present the user with a brief introduction to "Paperpile for Codex". Use the following template. Text in square brackets is meant to guide your generation of actual text to be shown to the user.

<Begin: welcome message template>

[Short sentence describing what Paperpile for Codex does: allows you to use your agent to work with Paperpile more efficiently. Find papers online, interact with your library, analyze full-text manuscripts, etc.]

[Provide a bullet-point list of the main skills available in the Paperpile plugin: find-papers, organize-paper-library, scheduled-paper-search, deep-library-search. Each should contain a short (< 10 word) summary of what can be done with the skill. Describe scheduled-paper-search as available only on supported desktop surfaces; its own workflow determines whether the current surface qualifies.]

[A non-bullet point sentence listing other skills available: narrative-paper-survey, auto-highlight-papers, translate-paper.]

[Mention that beyond the guided workflows above, Paperpile provides more fine-grained MCP tools that your agent can use individually to interact with Paperpile. Mention the user can always ask for the list of Paperpile MCP tools.]

[Offer a short list of potential next steps for the user. Use the conversational context to suggest relevant next steps. Absent any direction, suggest find-papers as a good way to start. Or ask the user what's their current research goal, then suggest appropriate next steps.]

</End: welcome message template>

# Authentication

If a Paperpile tool reports that the user is not authenticated, say so and stop, sharing the following instructions:

Run `codex mcp login paperpile` and complete the browser sign-in. `codex mcp list` shows the server as `Not logged in` until you do.
