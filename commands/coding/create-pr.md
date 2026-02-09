---
argument-hint: [--draft] [--base=main|master] [--style=simple|full] [--language=english|chinese]
description: Create pull requests via GitHub MCP tools with well-formatted PR title and description
---

**LANGUAGE INSTRUCTION**: When executing this command, check the command arguments for `--language=chinese`. If present, generate ALL PR titles and descriptions in Simplified Chinese. Otherwise, use English.

# Claude Command: Create PR via MCP

This command helps you create well-formatted pull requests using GitHub MCP tools, with automatic fallback to GitHub CLI (`gh`).

## Usage

Basic usage:
```
/create-pr
```

With options:
```
/create-pr --draft
/create-pr --base=main
/create-pr --style=full
/create-pr --language=chinese
```

## Command Options

- `--draft`: Create the pull request as a draft
- `--base=<branch>`: Specify the base branch (default: auto-detect main/master from remote)
- `--style=simple|full`:
  - `simple` (default): Creates concise PR title and brief description
  - `full`: Creates detailed PR description with comprehensive sections
- `--language=english|chinese`:
  - `english` (default): Generates PR content in English
  - `chinese`: Generates PR content in Simplified Chinese

## What This Command Does

1. **Pre-flight checks**:
   - Verify current directory is a git repository
   - Check for uncommitted changes and warn user
   - Ensure current branch is not the main/master branch
   - Verify branch has commits ahead of base branch

2. **Detect base branch**:
   - If `--base` specified, use that branch
   - Otherwise, auto-detect default branch from remote (main or master)
   - Fetch latest changes: `git fetch origin`

3. **Analyze changes**:
   - Get all commits between base branch and current branch: `git log <base>..HEAD`
   - Get full diff against base branch: `git diff <base>...HEAD`
   - Identify changed files and their categories
   - Determine the overall nature of changes (feature, fix, refactor, etc.)

4. **Generate PR content**:
   - Create PR title following Conventional Commits style
   - Generate PR description based on style setting
   - Include summary of changes, test plan, and relevant metadata

5. **Push branch to remote**:
   - Check if branch exists on remote
   - Push with upstream tracking: `git push -u origin <branch>`

6. **Create pull request**:
   - **Primary**: Use GitHub MCP tool `mcp__github__create_pull_request`
   - **Fallback**: If MCP unavailable, use GitHub CLI `gh pr create`
   - Return the PR URL to user

## Tool Selection Strategy

### Primary: GitHub MCP Tools

Use `mcp__github__create_pull_request` when available:
```
mcp__github__create_pull_request({
  owner: "<repo-owner>",
  repo: "<repo-name>",
  title: "<pr-title>",
  body: "<pr-description>",
  head: "<current-branch>",
  base: "<base-branch>",
  draft: <true|false>
})
```

### Fallback: GitHub CLI

If MCP tools are unavailable, use `gh pr create`:
```bash
gh pr create --title "<pr-title>" --body "<pr-description>" --base "<base-branch>" [--draft]
```

## PR Title Format

### Simple Style (Default)
```
<type>[optional scope]: <emoji> <description>
```
Example: `feat(auth): ✨ Add OAuth2 authentication flow`

### Characteristics
- Use present tense, imperative mood ("Add" not "Added")
- Keep under 72 characters
- Capitalize first letter of description
- No period at end

## PR Description Format

### Simple Style
```markdown
## Summary
<1-3 bullet points describing the changes>

## Test Plan
<Brief testing checklist>

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Full Style
```markdown
## Summary
<Comprehensive description of what this PR does>

## Changes
<Detailed list of changes organized by category>

## Motivation
<Why these changes are needed>

## Testing
<Detailed test plan with checkboxes>

## Screenshots (if applicable)
<Add screenshots for UI changes>

## Breaking Changes
<List any breaking changes, or "None">

## Related Issues
<Reference related issues: Closes #123, Refs #456>

## Checklist
- [ ] Code follows project style guidelines
- [ ] Tests have been added/updated
- [ ] Documentation has been updated
- [ ] No new warnings or errors introduced

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## PR Types & Emojis

| Type | Emoji | Description | When to Use |
|------|-------|-------------|-------------|
| `feat` | ✨ | New feature | Adding new functionality |
| `fix` | 🐛 | Bug fix | Fixing an issue |
| `docs` | 📝 | Documentation | Documentation only changes |
| `style` | 🎨 | Code style | Formatting, missing semi-colons, etc |
| `refactor` | ♻️ | Code refactoring | Neither fixes bug nor adds feature |
| `perf` | ⚡️ | Performance | Performance improvements |
| `test` | ✅ | Testing | Adding missing tests |
| `chore` | 🔧 | Maintenance | Changes to build process or tools |
| `ci` | 👷 | CI/CD | Changes to CI configuration |
| `build` | 📦 | Build system | Changes affecting build system |
| `revert` | ⏪ | Revert | Reverting previous commit |

## Workflow

1. **Check language parameter**: Determine the language for PR content by checking command arguments.

2. **Validate environment**:
   ```bash
   # Check if in git repo
   git rev-parse --is-inside-work-tree

   # Get current branch
   git branch --show-current

   # Check for uncommitted changes
   git status --porcelain
   ```

3. **Detect repository info**:
   ```bash
   # Get remote URL and parse owner/repo
   git remote get-url origin

   # Detect default branch
   git remote show origin | grep 'HEAD branch'
   ```

4. **Analyze changes**:
   ```bash
   # Fetch latest
   git fetch origin

   # Get commit log
   git log origin/<base>..HEAD --oneline

   # Get diff summary
   git diff origin/<base>...HEAD --stat

   # Get full diff for analysis
   git diff origin/<base>...HEAD
   ```

5. **Generate PR content**:
   - Analyze commits to determine PR type
   - Summarize changes across all commits
   - Create title following conventional format
   - Generate description based on style setting

6. **Push branch**:
   ```bash
   git push -u origin <current-branch>
   ```

7. **Create PR**:
   - Try MCP tool first: `mcp__github__create_pull_request`
   - If fails or unavailable, fallback to: `gh pr create`

8. **Output result**:
   - Display PR URL to user
   - Show PR number and title

## Best Practices

### DO:
- ✅ Ensure all commits are pushed before creating PR
- ✅ Write clear, descriptive PR titles
- ✅ Include test plan in description
- ✅ Reference related issues
- ✅ Keep PRs focused on single concern
- ✅ Add screenshots for UI changes
- ✅ Document breaking changes clearly

### DON'T:
- ❌ Create PR from main/master branch
- ❌ Create PR with uncommitted changes
- ❌ Use vague titles like "Fix bug" or "Update code"
- ❌ Mix unrelated changes in single PR
- ❌ Forget to push branch before creating PR
- ❌ Include sensitive information in PR description

## Error Handling

### Common Issues and Solutions

1. **Not a git repository**:
   - Error: "fatal: not a git repository"
   - Solution: Navigate to a git repository first

2. **No remote configured**:
   - Error: "No remote 'origin' found"
   - Solution: Add remote with `git remote add origin <url>`

3. **Branch already has PR**:
   - Error: "A pull request already exists"
   - Solution: Update existing PR or create new branch

4. **No commits to create PR**:
   - Error: "No commits between base and head"
   - Solution: Make commits before creating PR

5. **MCP tools unavailable**:
   - Automatically fallback to GitHub CLI
   - Ensure `gh` is installed and authenticated

6. **GitHub CLI not authenticated**:
   - Error: "gh: Not logged in"
   - Solution: Run `gh auth login` first

## Examples

### Simple Feature PR
```
Title: feat(api): ✨ Add user profile endpoint

## Summary
- Add GET /api/users/:id/profile endpoint
- Include user preferences and settings in response
- Add caching for improved performance

## Test Plan
- [ ] Verify endpoint returns correct user data
- [ ] Test with invalid user ID
- [ ] Verify cache behavior

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

### Full Style Bug Fix PR
```
Title: fix(auth): 🐛 Resolve session timeout issue

## Summary
Fix an issue where user sessions were expiring prematurely due to incorrect
timestamp comparison in the session validation middleware.

## Changes
### Backend
- Fix timestamp comparison in `src/middleware/auth.js`
- Update session refresh logic in `src/services/session.js`

### Tests
- Add unit tests for session timeout scenarios
- Add integration tests for session refresh flow

## Motivation
Users reported being logged out unexpectedly after short periods of
inactivity. Investigation revealed the session timeout calculation was
using local time instead of UTC, causing premature expiration.

## Testing
- [ ] Verify session persists for expected duration
- [ ] Test across different timezones
- [ ] Verify refresh token rotation works correctly
- [ ] Run full auth test suite

## Breaking Changes
None

## Related Issues
Closes #234
Refs #198

## Checklist
- [x] Code follows project style guidelines
- [x] Tests have been added/updated
- [x] Documentation has been updated
- [x] No new warnings or errors introduced

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

## Important Notes

- Default style is `simple` for quick PR creation
- Default language is `english` for PR content
- Use `--language=chinese` to generate Simplified Chinese PR content
- Use `full` style for:
  - Complex features
  - Bug fixes requiring explanation
  - Breaking changes
  - Changes affecting multiple systems
- Always review the generated PR content before confirming
- The tool will intelligently suggest `full` style when appropriate
- PR URL will be displayed upon successful creation
