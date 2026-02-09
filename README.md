# jorben-skills

Jorben's private Claude Code plugin, used for accumulating and sharing skills and commands across devices.

## Usage

Add this marketplace in any Claude Code session:

```
/plugin marketplace add jorben/jorben-skills
```

Then install the plugin:

```
/plugin install jorben-skills@jorben-skills
```

## Adding a New Skill

1. Create `skills/<skill-name>/SKILL.md` with frontmatter and instructions:

```markdown
---
name: my-skill
description: What the skill does
author: jorben
version: 0.1.0
tags:
  - tag1
---

# My Skill

Instructions for the skill...
```

2. Commit and push.

## Directory Structure

```
jorben-skills/
├── .claude-plugin/
│   ├── plugin.json          # Plugin manifest
│   └── marketplace.json     # Marketplace registry
├── skills/
│   └── <skill-name>/
│       └── SKILL.md         # Skill definition
├── CLAUDE.md
├── README.md
└── .gitignore
```

## License

Private use only.
