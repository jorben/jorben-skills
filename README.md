# jorben-skills

Jorben's private Claude Code plugin, used for accumulating and sharing skills and commands across devices.

## Usage

Add this marketplace in any Claude Code session:

```
/plugin marketplace add jorben/jorben-skills
```

Then install the plugins you need:

```
/plugin install jorben-skills@coding-studio
```

## Adding a New Skill

1. Choose the target plugin under `plugins/` (e.g., `graphics-studio`, `coding-studio`).
2. Create `plugins/<plugin-name>/skills/<skill-name>/SKILL.md` with frontmatter and instructions:

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

3. Commit and push. Skills are auto-discovered from the `skills/` directory under each plugin.

## Directory Structure

```
jorben-skills/
├── .claude-plugin/
│   └── marketplace.json              # Marketplace manifest
├── plugins/
│   ├── graphics-studio/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   └── skills/
│   │       └── zenmux-image-gen/
│   │           ├── SKILL.md
│   │           └── scripts/image_gen.py
│   ├── coding-studio/
│   │   ├── .claude-plugin/
│   │   │   └── plugin.json
│   │   ├── commands/
│   │   │   ├── commit.md
│   │   │   └── create-pr.md
│   │   └── skills/
│   │       └── project-docs-sync/
│   │           └── SKILL.md
│   └── video-studio/
│       ├── .claude-plugin/
│       │   └── plugin.json
│       └── .gitkeep
├── CLAUDE.md
├── README.md
└── .gitignore
```

## License

Private use only.
