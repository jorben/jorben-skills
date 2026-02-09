# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`jorben-skills` — Jorben's private Claude Code plugin marketplace for sharing skills, commands, and plugins across devices. Pure configuration/content project, no executable code, build system, or test framework.

## Architecture

Three-level hierarchy:

1. **Marketplace** (`/.claude-plugin/`) — Root manifest (`plugin.json`) and plugin registry (`marketplace.json`)
2. **Plugin** (`/plugins/<name>/.claude-plugin/plugin.json`) — Individual plugin with metadata
3. **Skill** (`/plugins/<name>/skills/<skill-name>/SKILL.md`) — Markdown file with YAML frontmatter containing instructions for Claude

Skills are auto-discovered from the directory structure,无需在 plugin.json 中手动声明。

## Adding a New Plugin

1. 创建 `plugins/<name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<name>",
  "version": "0.1.0",
  "description": "...",
  "author": {
    "name": "jorben",
    "github": "jorben"
  }
}
```

2. 创建 `plugins/<name>/skills/<skill-name>/SKILL.md`:

```markdown
---
name: <skill-name>
description: ...
author: jorben
version: 0.1.0
tags:
  - tag1
---

# Skill Title

Instructions for Claude...
```

3. 在 `.claude-plugin/marketplace.json` 的 `plugins` 数组中注册:

```json
{
  "name": "<name>",
  "source": "./plugins/<name>",
  "description": "..."
}
```
