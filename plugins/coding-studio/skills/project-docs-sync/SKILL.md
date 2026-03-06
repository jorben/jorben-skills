---
name: project-docs-sync
description: >-
  Proactively detect when project documentation files (README.md, AGENTS.md,
  CLAUDE.md) need updating based on code changes during coding sessions.
  Automatically applies targeted, surgical updates to keep docs in sync with
  code evolution. Only modifies files that already exist in the project.
  TRIGGER: activates in the background after significant code changes are made --
  new features, dependency changes, architecture modifications, API changes,
  configuration updates. DO NOT TRIGGER for: internal refactors, test-only
  changes, formatting, or when docs themselves were just edited.
author: jorben
version: 0.1.0
tags:
  - documentation
  - automation
  - proactive
  - coding-workflow
---

# Project Docs Sync

Automatically keep project documentation in sync with code changes. This skill runs **proactively in the background** during coding sessions — it is not invoked explicitly by the user.

When significant code changes are detected (new features, dependency updates, architecture changes, etc.), this skill analyzes which documentation files need updating and applies minimal, targeted edits to keep them current.

## Trigger Conditions

### SHOULD Trigger When

- A new feature, module, or component was implemented
- A new API endpoint or CLI command was added or changed
- Package dependencies were added, removed, or significantly updated (`package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `requirements.txt`, etc.)
- Project configuration changed (environment variables, build scripts, CI/CD pipelines)
- Architecture changed (new directories, renamed modules, changed data flow patterns)
- Installation or setup steps changed
- A previously documented workflow, command, or convention was altered
- New tools, frameworks, or services were integrated

### SHOULD NOT Trigger When

- Only internal implementation details changed (refactoring within a function body)
- Only test files were added or modified
- Only code style / formatting changes were made
- Changes are trivially small (typo fixes, variable renames, comment edits)
- Documentation files themselves were the only files edited (avoid infinite loop)
- Changes are work-in-progress that the user is still actively iterating on

### How to Detect Changes

Use git commands to understand what changed:

```bash
# See what files changed recently
git diff --name-only HEAD~3..HEAD
git diff --name-only HEAD~1..HEAD

# See staged changes
git diff --cached --name-only

# Get change statistics
git diff --stat HEAD~1..HEAD

# Review recent commit messages for context
git log --oneline -5
```

Classify changes by looking at which files were modified:
- **Dependency files**: `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `requirements.txt`, `Gemfile`
- **Config files**: `.env.example`, `docker-compose.yml`, `Makefile`, `tsconfig.json`, CI configs
- **Public API surfaces**: route definitions, exported functions, CLI argument parsers
- **Architecture indicators**: new directories under `src/`, new top-level modules, changed entry points

## Pre-Update Discovery

Before making any edits, perform these checks:

### Step 1: Check Which Target Files Exist

Search for documentation files in the **project root** (the current working directory, NOT this skill's repository):

- `README.md`
- `AGENTS.md`
- `CLAUDE.md`

**CRITICAL: Only proceed for files that already exist. NEVER create new documentation files.**

### Step 2: Read Each Existing File

For each target file that exists:
1. Read the entire file to understand its current structure (headings, sections)
2. Note the writing language (English, Chinese, or mixed)
3. Note the formatting style (heading levels, list styles, code block usage)
4. Identify which sections are relevant to the detected changes

### Step 3: Analyze the Code Changes

Using the git diff output:
1. Summarize what specifically changed in the code
2. Map each change to which documentation sections it might affect
3. Determine whether the change adds new information or modifies existing information
4. Assess whether the change is significant enough to warrant a doc update

## File-Specific Rules

Each documentation file serves a different audience. Avoid duplicating the same information across files.

### README.md — User-Facing Documentation

**Audience**: End users, new contributors, anyone discovering the project.

**What to update**:
- Project description and feature list
- Installation and setup instructions
- Usage examples and quick-start guides
- API reference or endpoint documentation
- Configuration options and environment variables
- Dependency and prerequisite lists
- Contributing guidelines (if setup steps changed)

**When to update**:
- New user-facing feature was added
- Setup or installation steps changed
- New dependencies require user action
- API or CLI interface changed
- Configuration options were added or removed

**When NOT to update**:
- Internal architecture changes with no user-facing impact
- Developer tooling changes (those go in CLAUDE.md/AGENTS.md)

### CLAUDE.md — Claude Code Development Instructions

**Audience**: Claude Code (Anthropic's AI coding assistant).

**What to update**:
- Project architecture overview and directory structure
- Build, test, lint, and run commands
- Code conventions and patterns
- Key file paths and module responsibilities
- Workflow guidelines for development tasks
- Environment setup for development

**When to update**:
- New modules or directories added to the project
- Build or test commands changed
- New code conventions were established
- Architecture patterns were modified
- Development workflow changed

### AGENTS.md — Codex / OpenAI Agent Instructions

**Audience**: OpenAI Codex and similar AI coding agents.

**What to update**:
- Project context for autonomous coding
- File organization and module responsibilities
- Testing and verification instructions
- Code style and conventions
- Key architectural decisions

**When to update**:
- Same triggers as CLAUDE.md
- Present information in a format suitable for the AGENTS.md conventions
- Maintain the file's own structure and voice — do not simply copy from CLAUDE.md

### Cross-File Rule

If the same information is relevant to multiple files, present it at the appropriate level for each audience:
- **README.md** explains "how to use"
- **CLAUDE.md / AGENTS.md** explain "how to develop"

Example: A new Redis dependency might appear in:
- README.md: "Prerequisites: Redis 7.0+" in the setup section
- CLAUDE.md: "Start Redis before running tests: `redis-server`" in the commands section

## Update Strategy

### Surgical Editing Principles

1. **Use the Edit tool** — never rewrite entire files with the Write tool
2. **Minimal changes** — modify only the lines that need updating
3. **Preserve structure** — do not reorganize sections, change heading levels, or alter document layout
4. **Match existing style**:
   - If the file uses `-` for lists, use `-` (not `*` or `+`)
   - If code blocks specify a language, specify the language
   - Match indentation (2 spaces vs 4 spaces vs tabs)
   - Match the language (write in English if the file is in English, Chinese if in Chinese)
5. **For new information with no existing section**:
   - Add under the most appropriate existing heading
   - If no heading fits, add a new section following the file's hierarchy
   - Place new sections in a logical position (not just appended at the end)
6. **For outdated information**:
   - Update references to match the new state
   - Remove references to features/commands that no longer exist
   - Do not leave stale or contradictory documentation

### What NOT to Do

- Do not add boilerplate or filler text
- Do not add sections for completeness if the information is not relevant
- Do not reformat or restructure sections that are not affected by the change
- Do not add auto-generated timestamps or "last updated" markers
- Do not add comments like "<!-- Updated by project-docs-sync -->"

## Safety Guardrails

1. **Never create files** — only edit files that already exist in the project root
2. **Never delete files** — only modify content within existing files
3. **Minimal edits** — change the fewest lines necessary to bring docs in sync
4. **Preserve structure** — do not reorganize, reorder, or restructure documents
5. **No sensitive information** — never add API keys, tokens, passwords, internal URLs, or file paths that could be security-sensitive
6. **No speculation** — only document what the code actually does, based on the diff and source code. Do not guess about intended behavior
7. **Idempotency** — running the check twice with the same code state should not produce additional changes
8. **Respect user edits** — if the user manually edited a doc file in the same session, do not overwrite their changes
9. **Background operation** — do not interrupt the user's workflow. Apply changes silently and provide a brief, non-intrusive summary

## Execution Workflow

```
Step 1: DETECT CHANGES
  ├─ Run: git diff --name-only HEAD~1..HEAD
  ├─ Run: git diff --cached --name-only (for staged changes)
  ├─ Run: git diff --stat HEAD~1..HEAD
  └─ Classify changed files by category (feature, config, deps, architecture)

Step 2: EVALUATE SIGNIFICANCE
  ├─ Apply trigger conditions (see "Trigger Conditions" section)
  ├─ If changes are below threshold → exit silently, do nothing
  └─ If significant → proceed to Step 3

Step 3: DISCOVER TARGET FILES
  ├─ Check for README.md in project root
  ├─ Check for AGENTS.md in project root
  ├─ Check for CLAUDE.md in project root
  └─ If none exist → exit silently

Step 4: READ AND ANALYZE
  ├─ Read each existing target file completely
  ├─ Understand current structure, style, and language
  ├─ Read relevant source code changes (git diff -p for specific files)
  └─ Map changes → affected documentation sections

Step 5: APPLY UPDATES
  ├─ For each file needing changes:
  │   ├─ Identify exact section(s) to modify
  │   ├─ Use Edit tool for surgical changes
  │   └─ Verify surrounding content is preserved
  └─ Skip files where no update is needed

Step 6: NOTIFY (brief, non-intrusive)
  └─ Example: "Synced docs: updated README.md setup section (new Redis dependency),
     updated CLAUDE.md architecture section (new notification module)"
```

## Examples

### Example 1: New Dependency Added

**Change**: `package.json` gained `"redis": "^4.6.0"` as a dependency.

**README.md** has a "Prerequisites" section:
```markdown
## Prerequisites
- Node.js 18+
- PostgreSQL 15+
```

**Action**: Edit to add Redis:
```markdown
## Prerequisites
- Node.js 18+
- PostgreSQL 15+
- Redis 7.0+
```

### Example 2: New API Endpoint

**Change**: New file `src/routes/webhooks.ts` with `POST /api/v2/webhooks` endpoint.

**README.md** has an "API Reference" section listing existing endpoints.

**Action**: Add the new endpoint following the existing format in that section.

### Example 3: Build Command Changed

**Change**: `Makefile` updated — `make build` renamed to `make build-all`.

**CLAUDE.md** has:
```markdown
## Common Commands
- Build: `make build`
```

**Action**: Edit to update:
```markdown
## Common Commands
- Build: `make build-all`
```

### Example 4: New Module Added

**Change**: New directory `src/services/notifications/` created with notification service implementation.

**CLAUDE.md** has an "Architecture" section with directory tree.

**Action**: Add the new module entry to the directory tree, with a brief description following the existing format.

### Example 5: No Action Needed

**Change**: Internal refactor — `src/utils/helpers.ts` functions renamed for clarity. No public API change. No new dependencies. No architecture change.

**Action**: Do nothing. Internal refactors don't warrant documentation updates.
