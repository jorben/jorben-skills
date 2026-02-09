---
argument-hint: [--verify=yes|no] [--style=simple|full] [--type=feat|fix|docs|style|refactor|perf|test|chore|ci|build|revert] [--language=english|chinese]
description: Create well-formatted commits with conventional commit messages
---

**LANGUAGE INSTRUCTION**: When executing this command, check the command arguments for `--language=chinese`. If present, generate ALL commit messages in Simplified Chinese. Otherwise, use English.

# Claude Command: Commit

This command helps you create well-formatted commits following the Conventional Commits specification.

## Usage

Basic usage:
```
/commit
```

With options:
```
/commit --verify=no
/commit --style=full
/commit --style=full --type=feat
```

## Command Options

- `--verify`: Pre-commit checks (lint, build, generate:docs)
  - `no` (default): Skip pre-commit checks
  - `yes`: Perform pre-commit checks
- `--style=simple|full`: 
  - `simple` (default): Creates concise single-line commit messages
  - `full`: Creates detailed commit messages with body and footer sections
- `--type=<type>`: Specify the commit type (overrides automatic detection)
- `--language=english|chinese`:
   - `english` (default): Generates commit messages in English
   - `chinese`: Generates commit messages in Simplified Chinese

## What This Command Does

1. **Merge latest remote main branch**:
   - Detect the default branch name (master or main) from remote
   - Fetch latest changes from remote: `git fetch origin`
   - Merge the latest remote main branch: `git merge origin/<main|master>`
   - Resolve any merge conflicts if necessary before proceeding

2. **Pre-commit checks** (when `--verify=yes`):
   - **Auto-detect project build tool first**: Check for package.json, pyproject.toml, Makefile, Cargo.toml, go.mod, etc.
   - **Determine the package manager**: For Node.js projects, check lock files (package-lock.json → npm, pnpm-lock.yaml → pnpm, yarn.lock → yarn)
   - **Read available scripts/targets**: Check package.json scripts, Makefile targets, or equivalent before executing
   - **Execute appropriate commands based on detected configuration**:
     - Lint: Run the project's lint command if available
     - Test: Run the project's test command if available
     - Build: Run the project's build command if available
   - **IMPORTANT**: Do NOT hardcode or assume commands like `npm run test`. Always verify the exact commands from the project configuration first.

3. **File staging**:
   - Check staged files with `git status`
   - If no files staged, automatically add all modified/new files with `git add`

4. **Change analysis**:
   - Run `git diff` to understand changes
   - Detect if multiple logical changes should be split
   - Suggest atomic commits when appropriate

5. **Commit message creation**:
   - **CRITICAL: Language Detection** - First, check if `--language=chinese` is present in the command arguments. If so, generate ALL commit messages in Simplified Chinese. If not specified or `--language=english`, generate in English.
   - Generate messages following Conventional Commits specification
   - Apply appropriate emoji prefixes
   - Add detailed body/footer in full style mode

## Conventional Commits Format

### Simple Style (Default)
```
<type>[optional scope]: <emoji> <description>
```
Example: `feat(auth): ✨ add JWT token validation`

### Full Style
```
<type>[optional scope]: <emoji> <description>

<body>

<footer>
```

Example:
```
feat(auth): ✨ add JWT token validation

Implement JWT token validation middleware that:
- Validates token signature and expiration
- Extracts user claims from payload
- Adds user context to request object
- Handles refresh token rotation

This change improves security by ensuring all protected
routes validate authentication tokens properly.

BREAKING CHANGE: API now requires Bearer token for all authenticated endpoints
Closes: #123
```

## Commit Types & Emojis

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

## Body Section Guidelines (Full Style)

The body should:
- Explain **what** changed and **why** (not how)
- Use bullet points for multiple changes
- Include motivation for the change
- Contrast behavior with previous behavior
- Reference related issues or decisions
- Be wrapped at 72 characters per line

Good body example:
```
Previously, the application allowed unauthenticated access to
user profile endpoints, creating a security vulnerability.

This commit adds comprehensive authentication middleware that:
- Validates JWT tokens on all protected routes
- Implements proper token refresh logic
- Adds rate limiting to prevent brute force attacks
- Logs authentication failures for monitoring

The change follows OAuth 2.0 best practices and improves
overall application security posture.
```

## Footer Section Guidelines (Full Style)

Footer contains:
- **Breaking changes**: Start with `BREAKING CHANGE:`
- **Issue references**: `Closes:`, `Fixes:`, `Refs:`
- **Co-authors**: `Co-authored-by: name <email>`
- **Review references**: `Reviewed-by:`, `Approved-by:`

Example footers:
```
BREAKING CHANGE: rename config.auth to config.authentication
Closes: #123, #124
Co-authored-by: Jane Doe <jane@example.com>
```

## Scope Guidelines

Scope should be:
- A noun describing the section of codebase
- Consistent across the project
- Brief and meaningful

Common scopes:
- `api`, `auth`, `ui`, `db`, `config`, `deps`
- Component names: `button`, `modal`, `header`
- Module names: `parser`, `compiler`, `validator`

## Commit Splitting Strategy

Automatically suggest splitting when detecting:
1. **Mixed types**: Features + fixes in same commit
2. **Multiple concerns**: Unrelated changes
3. **Large scope**: Changes across many modules
4. **File patterns**: Source + test + docs together
5. **Dependencies**: Dependency updates mixed with features

## Best Practices

### DO:
- ✅ Write in present tense, imperative mood ("add" not "added")
- ✅ Keep first line under 50 characters (72 max)
- ✅ Capitalize first letter of description
- ✅ No period at end of subject line
- ✅ Separate subject from body with blank line
- ✅ Use body to explain what and why vs. how
- ✅ Reference issues and breaking changes

### DON'T:
- ❌ Mix multiple logical changes in one commit
- ❌ Include implementation details in subject
- ❌ Use past tense ("added" instead of "add")
- ❌ Make commits too large to review
- ❌ Commit broken code (unless WIP)
- ❌ Include sensitive information

## Examples

### Simple Style Examples
```bash
feat: ✨ add user registration flow
fix: 🐛 resolve memory leak in event handler
docs: 📝 update API endpoints documentation
refactor: ♻️ simplify authentication logic
perf: ⚡️ optimize database query performance
chore: 🔧 update build dependencies
```

### Full Style Example
```bash
feat(auth): ✨ implement OAuth2 authentication flow

Add complete OAuth2 authentication system supporting multiple
providers (Google, GitHub, Microsoft). The implementation
follows RFC 6749 specification and includes:

- Authorization code flow with PKCE
- Refresh token rotation
- Scope-based permissions
- Session management with Redis
- Rate limiting per client

This provides users with secure single sign-on capabilities
while maintaining backwards compatibility with existing
JWT authentication.

BREAKING CHANGE: /api/auth endpoints now require client_id parameter
Closes: #456, #457
Refs: RFC-6749, RFC-7636
```

## Workflow

1. **Check language parameter**: Determine the language for commit messages by checking command arguments. If `--language=chinese` is present, use Simplified Chinese. Otherwise, use English.
2. **Merge latest remote main branch**: Fetch and merge the latest changes from remote main/master branch to ensure the local branch is up-to-date.
3. **Run pre-commit checks** (if `--verify=yes`): Auto-detect project build tools and execute appropriate lint/test/build commands.
4. Analyze changes to determine commit type and scope
5. Check if changes should be split into multiple commits
6. For each commit:
   - Stage appropriate files
   - Generate commit message based on style setting
   - If full style, create detailed body and footer
   - Execute git commit with generated message
7. Provide summary of committed changes

## Important Notes

- Default style is `simple` for quick, everyday commits
- Default language is `english` for commit messages
- Use `--language=chinese` to generate Simplified Chinese commit messages
- Use `full` style for:
  - Breaking changes
  - Complex features
  - Bug fixes requiring explanation
  - Changes affecting multiple systems
- The tool will intelligently detect when full style might be beneficial and suggest it
- Always review the generated message before confirming
- Pre-commit checks help maintain code quality
