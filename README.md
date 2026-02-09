# jorben-skills

Jorben's private Claude Code plugin marketplace, used for accumulating and sharing skills, commands, and other plugins across devices.

## Usage

Add this marketplace in any Claude Code session:

```
/plugin marketplace add jorben/jorben-skills
```

Then browse and install available plugins:

```
/plugin
```

## Adding a New Plugin

1. Create a directory under `plugins/`:

```
plugins/my-plugin/
├── .claude-plugin/
│   └── plugin.json
└── skills/
    └── my-skill/
        └── SKILL.md
```

2. Define the plugin manifest in `.claude-plugin/plugin.json`:

```json
{
  "name": "my-plugin",
  "version": "0.1.0",
  "description": "Description of my plugin",
  "author": {
    "name": "jorben",
    "github": "jorben"
  }
}
```

3. Write the skill in `SKILL.md` with frontmatter and instructions:

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

4. Register the plugin in the marketplace by adding an entry to `.claude-plugin/marketplace.json`:

```json
{
  "name": "my-plugin",
  "source": "./plugins/my-plugin",
  "description": "Description of my plugin"
}
```

5. Commit and push.

## Directory Structure

```
jorben-skills/
├── .claude-plugin/
│   ├── plugin.json          # Marketplace root manifest
│   └── marketplace.json     # Plugin directory listing
├── plugins/
│   └── <plugin-name>/       # Each plugin in its own directory
│       ├── .claude-plugin/
│       │   └── plugin.json  # Plugin manifest
│       └── skills/
│           └── <skill>/
│               └── SKILL.md # Skill definition
├── README.md
└── .gitignore
```

## License

Private use only.
