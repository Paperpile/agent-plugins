---
name: scheduled-paper-search
description: Set up a supported scheduled task that periodically searches for new citations or related articles, analyzes or organizes new results, and saves them for later reading. Use when the user wants a recurring paper search, including when the current product surface may not support scheduling.
---

# Scheduled Paper Search

This skill guides the agent in working with the user to define the scope, goals, and mode of action of a scheduled literature search. This skill should be presented to the user as a guided workflow, with easy-to-select default options (use either the built-in question-asking tool or present numbered options, plus a "something else" option for customization).

Before beginning the workflow, apply the scheduling support rules for the current harness:

Codex Desktop supports scheduled tasks, but Codex CLI does not. The same compiled plugin is used in
both surfaces, so first check whether the current surface provides its platform scheduling or automation
tool. If it does not, tell the user to open Codex Desktop and stop; do not offer a cron job or pretend to
create a schedule.

In Codex Desktop, create the scheduled task from a task that belongs to a saved project. Before asking
for final approval, make sure that project's Paperpile plugin permission is set to **Allow all actions**
or an equivalent setting that lets every required Paperpile tool call run without interactive approval.
Scheduled runs cannot answer approval prompts. If either prerequisite is missing, explain how to fix it
and stop before creating the task.

IMPORTANT: Before creating or modifying any scheduled tasks, always present the user an exact description of what will be scheduled and request their approval. Make it easy for the user to approve by presenting the final approval options as "1. **Approve** this plan and create the scheduled search", "2. Modify the plan".

## Paperpile tone and style

Paperpile is a tool for academics. Be calm, efficient and specific, and assume a seasoned researcher in the field is reading. Be direct about what you did and did not find.

- No emojis.
- No hype or overly-enthusiastic conclusions.
- Bold and italics are fine where they aid scanning
- Say "I could not find it" rather than padding a weak result.

## Handling empty-argument skill invocation

If this skill is invoked with no further instruction, do not guess at a task. Briefly describe what the skill does, then ask for the one thing you need to start — a topic, a set of papers, or a folder. Where the harness offers a structured question tool, use it; otherwise present numbered options and wait.

## Initial interaction flow

When this skill is invoked without specific direction, present the user with a welcoming, structured message explaining your capabilities and describe the overall process of setting up a scheduled search:

1. **Define the search criteria and scope**
2. **Define the action to take on new results**
3. **Confirm and create the scheduled task**

If the system has any existing Paperpile scheduled searches, list them and mention that the user may ask to modify any of the existing searches.

Highlight that no modifications to their library will occur without approval of the plan.

## Workflow steps

### Step 1: define the search criteria and scope

**Goal**: Define a specific search prompt that will form the basis of the scheduled search task.

Before exiting this step, you MUST have a clear understanding of how to reproducibly search for papers that match the user's interests and expectations.

Confirm the search strategy and parameters with the user before proceeding: use the following template (slight modifications are allowed).
Text in square braces is commentary or guidance; it should be removed or replaced as appropriate.

 <Begin: search strategy template>
 Goal: [Brief description of the searh goal]

 [Include one or more of the following, depending on the user's stated criteria:]
 Keywords: [keywords to be included in the search, if any]
 Authors: [author(s) that will be included in the search, if any]
 Anchor paper(s): [author-year strings for papers that will ground the search, if any]

 Frequency: [daily / weekly / monthly]
 <Eng: search strategy template>

Work with the user to define the specific search criteria and patterns; load the `find-papers` skill for more details on search strategy and
how to best orchestrate Paperpile's literature search tools.

### Step 2: define the action to take on new results

The user may choose between the following options for defining what action should be taken with new search results:

1. Save to my library (Default). Save new references to your library, organized with an appropriate folder or label.
   Oftentimes, it makes sense to have the scheduled search apply some pre-screening or discretion to search results before saving.
   Be explicit about what instructions the scheduled search will be provided, and confirm with the user.
2. Save and analyze. Save new references to your library, as above, then analyze the full text to construct a short Markdown note
   to save in the `note` field, and also highlight quotes within the PDF that are directly relevant to the user's interest. This approach
   costs more tokens, but presents the user with more pre-screened context.
   If this option is selected, the scheduled task should load the `auto-highlight-papers` skill to proceed.
   Its prompt must say that `save_to_library` already waits for the PDF crawl and reports each
   reference's outcome in `pdf_crawl`: `none_found`, `restricted`, `blocked` and `error` are final.
   A reference still `pending` gets one further check 20–30 seconds later, unless its `stage` is
   `awaiting_client`, which means no Paperpile browser extension is online to crawl it. A scheduled run
   must retain the citation and record the observed blocker when no extractable PDF appears; it must not
   invent highlights or full-text conclusions.
3. Save to a shared library. Users may indicate a shared library they want to save new results to.
4. Something else. If the user wants a different action to be performed, they can describe it here.

### Step 3: Confirm and create the scheduled task

Using the appropriate platform-provided tool, create a scheduled task that will faithfully execute the instructions as agreed-upon with the user.

The task should be asked to first load the `scheduled-paper-search` skill, so it has access to the same information and guidance used to create
the task.

It should also be guided to save a text file with "seen" DOIs in a known persistent location, so the scheduled search agent can easily check
whether a given article is new or has been seen before and not saved to the user's library.

Provide the user a summary of the specific prompt that will be provided to the platform-provided scheduling tool. The user must approve before you
create the scheduled task.

If allowed by the platform, ask the user if they would like the tool to be triggered immediately in order to assess its behavior.
