# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`jorben-skills` — Jorben's private Claude Code plugin for sharing skills and commands across devices. Pure configuration/content project, no executable code, build system, or test framework.

## Architecture

仓库是一个 marketplace，包含多个独立的 plugin，每个 plugin 有自己的子目录：

1. **Marketplace** (`/.claude-plugin/marketplace.json`) — 声明所有 plugin，每个 plugin 只需 `name`、`source`、`description`
2. **Plugin** (`/plugins/<plugin-name>/`) — 每个 plugin 有独立目录，包含 `.claude-plugin/plugin.json`（只需 `name` 和 `description`）
3. **Skill** (`/plugins/<plugin-name>/skills/<skill-name>/SKILL.md`) — Markdown file with YAML frontmatter
4. **Command** (`/plugins/<plugin-name>/commands/<command>.md`) — Command definition file

Skills、commands、agents 按约定从 plugin 目录下的同名子目录（`skills/`、`commands/`、`agents/`）自动发现，无需在 JSON 中显式声明。

## Adding a New Skill

1. 确定目标 plugin（如 `graphics-studio`、`coding-studio` 等）
2. 创建 `plugins/<plugin-name>/skills/<skill-name>/SKILL.md`:

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

3. Commit and push. Skills 从 `skills/` 目录自动发现。

## Adding a New Plugin

1. 创建 `plugins/<plugin-name>/.claude-plugin/plugin.json`:

```json
{
  "name": "<plugin-name>",
  "description": "..."
}
```

2. 在 `/.claude-plugin/marketplace.json` 的 `plugins` 数组中添加:

```json
{
  "name": "<plugin-name>",
  "source": "./plugins/<plugin-name>",
  "description": "..."
}
```

3. 在 plugin 目录下按需创建 `skills/`、`commands/`、`agents/` 子目录。
