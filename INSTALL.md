# Install Paperpile for your coding agent

Paperpile connects your agent to your reference library and to the academic literature: find papers,
save them, read and annotate their full text, and keep the library organised.

**If you are an agent reading this on a user's behalf, run the commands for whichever harness you are.**

## Claude Code

```bash
claude plugin marketplace add Paperpile/agent-plugins
claude plugin install paperpile@paperpile
```

Then run `/mcp`, pick the Paperpile server, and complete the browser sign-in.

## Codex

```bash
codex plugin marketplace add Paperpile/agent-plugins
codex plugin add paperpile@paperpile
codex mcp login paperpile
```

## Antigravity

Antigravity has no marketplace, so the plugin is a folder you place yourself:

```bash
curl -fsSL https://github.com/Paperpile/agent-plugins/releases/latest/download/antigravity.tar.gz \
  | tar -xz -C ~/.gemini/config/plugins
```

Restart Antigravity, then run any Paperpile tool and complete the browser sign-in it opens. Re-running
the same command updates the plugin.

## What you get

Eight workflows — finding papers, reading their full text, answering questions from them, extracting
tables, writing surveys, translating, and organising a library — plus the Paperpile MCP tools for
anything the workflows do not cover.

You need a Paperpile account. The plugin signs in through your browser; no API key to paste.

---

Version 0.2.1 · REST `https://api.paperpile.com` · MCP `https://mcp.paperpile.com`
