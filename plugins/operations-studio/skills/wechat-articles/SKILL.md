---
name: wechat-articles
description: >-
  Fetch WeChat Official Account (公众号) article data via JZL API. Provides
  three capabilities: (1) get today's publishing status, (2) get historical
  article list with pagination, (3) convert article short links to long links
  with biz extraction. Requires JZL_API_KEY env var.
  TRIGGER when: user asks to check a WeChat official account's articles,
  get publishing status, list historical posts, convert WeChat article links,
  or extract biz from article URLs.
  DO NOT TRIGGER for: WeChat mini-program analysis, WeChat Pay, or general
  social media tasks unrelated to 公众号 articles.
author: jorben
version: 0.1.0
tags:
  - operations
  - wechat
  - public-account
  - articles
---

# WeChat Articles (公众号文章获取)

Fetch article data from WeChat Official Accounts (微信公众号) using the JZL API.

## Prerequisites

- **Environment variable**: `JZL_API_KEY` must be set with a valid API key
- **Runtime**: Python 3.10+, managed via `uv`

## Capabilities

### 1. Today's Publishing Status (当天发文情况)

Check whether a public account has published articles today and get details.

### 2. Historical Article List (历史发文列表)

Retrieve the full article history with pagination (5 posts per page).

### 3. Short Link → Long Link (短链接转长链接)

Convert a WeChat article short URL to its full long URL, and automatically extract the account's `__biz` parameter.

## How to Use

All three commands are provided by a single Python script. Run it via `uv run`:

```bash
# Ensure API key is set
export JZL_API_KEY="your_key_here"

SCRIPT_DIR="<path-to-this-skill>/wechat_articles.py"

# 1. Today's publishing status — identify account by name, biz, or url (at least one required)
uv run "$SCRIPT_DIR" today --name "公众号名称"
uv run "$SCRIPT_DIR" today --biz "MjM5MTM1NjUzNA=="
uv run "$SCRIPT_DIR" today --url "https://mp.weixin.qq.com/s/xxxxx"

# 2. Historical article list — supports --page for pagination
uv run "$SCRIPT_DIR" history --name "公众号名称"
uv run "$SCRIPT_DIR" history --name "公众号名称" --page 2
uv run "$SCRIPT_DIR" history --biz "MjM5MTM1NjUzNA==" --page 3

# 3. Short link to long link (auto-extracts biz)
uv run "$SCRIPT_DIR" short2long "https://mp.weixin.qq.com/s/yZKzTuuol-1M0zFKlJqSqg"
```

The script path relative to this skill is:
```
plugins/operations-studio/skills/wechat-articles/wechat_articles.py
```

## Account Identification

All query commands (`today`, `history`) accept three ways to identify an account — **at least one is required**:

| Parameter | Description | Example |
|-----------|-------------|---------|
| `--name`  | Account name or wxid | `"人民日报"` |
| `--biz`   | Account biz (base64 of 8-10 digit number) | `"MjM5MTM1NjUzNA=="` |
| `--url`   | Any article URL from the account | `"https://mp.weixin.qq.com/s/..."` |

**Recommendation**: `--biz` is the most reliable identifier. If you only have a name, be aware that duplicate names may exist. If you only have a short link URL, consider using `short2long` first to get the biz, then use `--biz` for subsequent queries.

## API Rate Limit

**QPS limit: 5 requests/second**. The script enforces this automatically with built-in rate limiting. If you still receive code `-1`, wait 5 seconds before retrying.

## Response Field Reference

### Today / History — Article Fields

| Field | Description |
|-------|-------------|
| `data[i].title` | Article title |
| `data[i].url` | Article link (short link since 2024-12-01) |
| `data[i].digest` | Article summary |
| `data[i].cover_url` | Cover image URL |
| `data[i].post_time_str` | Publish time (human-readable) |
| `data[i].post_time` | Publish timestamp |
| `data[i].position` | Position in the post (1 = headline) |
| `data[i].original` | 1: original, 0: not declared, 2: repost |
| `data[i].types` | 9: mass-send (群发), 1: publish (发布) |
| `data[i].item_show_type` | 0: article, 5: video, 7: audio, 8: image, 10: text |
| `data[i].is_deleted` | 0: normal, 1: deleted |

### Today / History — Pagination & Meta

| Field | Description |
|-------|-------------|
| `total_num` | Total post count (mass-send + publish) |
| `total_page` | Total pages (5 posts per page) |
| `now_page` | Current page number |
| `now_page_articles_num` | Number of articles on current page |
| `masssend_count` | Total mass-send count |
| `publish_count` | Total publish count |
| `cost_money` | API cost for this request |
| `remain_money` | Remaining account balance |

### Short2Long — Response Fields

| Field | Description |
|-------|-------------|
| `short_url` | Input short link |
| `long_url` | Converted long link |
| `extracted_biz` | Account biz extracted from long URL (added by script) |
| `cost_money` | API cost (0.02/request) |

## Error Codes

| Code | Meaning | Action |
|------|---------|--------|
| `0` | Success | — |
| `-1` | QPS exceeded (>5/s) | Wait 5s, retry |
| `100` | Missing parameter | Provide at least one of biz/name/url |
| `104` | Article deleted | Check the link |
| `105` | Account not found / banned | Try using biz or url instead of name |
| `110` | No more articles in pagination | Stop paginating |
| `10002` | Invalid API key | Check JZL_API_KEY |
| `20001` | Insufficient balance | Top up account |
| `20003` | Malformed URL (& not encoded) | Ensure `&` is encoded as `%26` in url param |

## Typical Workflows

### Workflow A: Monitor a specific account

```
1. uv run ... today --name "某公众号"          → Check if it published today
2. uv run ... history --name "某公众号"        → Browse recent articles
3. uv run ... history --name "某公众号" --page 2  → Load more articles
```

### Workflow B: Got a short link, need full info

```
1. uv run ... short2long "https://mp.weixin.qq.com/s/xxx"
   → Get long_url + extracted_biz
2. uv run ... today --biz "<extracted_biz>"    → Check account's today status
3. uv run ... history --biz "<extracted_biz>"  → Browse history
```

### Workflow C: Batch historical scan

```
for page in 1 2 3 4 5:
    uv run ... history --biz "xxx" --page $page
    # Parse data[i].title, data[i].url, data[i].post_time_str
    # Stop when total_page is reached
```

**Note**: Since 2024-12-01, all article links returned by history API are short links. Use `short2long` to convert if you need the full URL with biz parameters.
