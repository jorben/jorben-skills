# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`jorben-skills` — Jorben's private Claude Code plugin for sharing skills and commands across devices. Pure configuration/content project, no executable code, build system, or test framework.

## Architecture

仓库本身既是 marketplace 也是唯一的 plugin，skills 直接放在根目录：

1. **Marketplace** (`/.claude-plugin/marketplace.json`) — Marketplace registry, plugin source 指向 `"."`（仓库根目录）
2. **Plugin** (`/.claude-plugin/plugin.json`) — Plugin manifest with metadata
3. **Skill** (`/skills/<skill-name>/SKILL.md`) — Markdown file with YAML frontmatter containing instructions for Claude

Skills are auto-discovered from the directory structure, 无需在 plugin.json 中手动声明。

## Adding a New Skill

创建 `skills/<skill-name>/SKILL.md`:

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
