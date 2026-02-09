---
name: zenmux-image-gen
description: Generate, edit, and compose images using Zenmux API (Google GenAI). Use when user asks to generate images, create illustrations, design graphics, draw pictures, edit existing images, or compose multiple images. Also invokable by other skills for automated image generation (e.g., frontend-design generating assets). Supports aspect ratios (1:1, 2:3, 3:2, 4:3, 3:4, 9:16, 16:9, 21:9) and resolutions (1K, 2K, 4K).
---

# Zenmux Image Gen

Image generation, editing, and composition using Zenmux API with Google GenAI protocol.

## Setup

### 1. Environment Variables

Required environment variables:
```bash
export ZENMUX_API_BASE="your-api-base-url"
export ZENMUX_API_KEY="your-api-key"
export ZENMUX_MODEL_IMAGE="your-model-id"
```

### 2. Activate Virtual Environment

This skill uses uv for dependency management. Before running any commands:

```bash
# Navigate to skill directory
cd /path/to/zenmux-image-gen

# Activate virtual environment
source .venv/bin/activate

# Or use uv run directly (auto-activates venv)
uv run python scripts/image_gen.py --help
```

If `.venv` doesn't exist, initialize it:
```bash
uv sync
```

## Quick Start

```bash
# Activate venv first
source .venv/bin/activate

# Generate image
python scripts/image_gen.py generate "A serene mountain landscape at sunset" --ratio 16:9 --resolution 2K

# Or use uv run (no manual activation needed)
uv run python scripts/image_gen.py generate "A serene mountain landscape at sunset" --ratio 16:9 --resolution 2K
```

## Commands

### Generate Image
```bash
uv run python scripts/image_gen.py generate "A futuristic cityscape" --ratio 16:9 --resolution 2K
```

### Edit Image
```bash
uv run python scripts/image_gen.py edit "Remove the background and replace with a beach scene" source.png
```

### Compose Images
```bash
uv run python scripts/image_gen.py compose "Blend these images into a collage" image1.png image2.png image3.png
```

## Supported Parameters

### Aspect Ratios
| Ratio | Use Case |
|-------|----------|
| 1:1   | Social media avatars, icons |
| 2:3   | Portrait photos, posters |
| 3:2   | Landscape photos |
| 4:3   | Presentations, traditional displays |
| 3:4   | Mobile wallpapers |
| 9:16  | Mobile stories, vertical video |
| 16:9  | Widescreen, presentations, banners |
| 21:9  | Ultra-wide banners, cinematic |

### Resolutions
| Resolution | Description |
|------------|-------------|
| 1K | Standard quality (~1024px on longest side) |
| 2K | High quality (~2048px on longest side) |
| 4K | Ultra high quality (~4096px on longest side) |

## Usage Patterns

### 1. Text-to-Image Generation

```python
from scripts.image_gen import generate_image

result = generate_image(
    prompt="A futuristic cityscape with flying cars",
    aspect_ratio="16:9",
    resolution="2K",
    output_path="./output",
    filename="city.png"
)
```

### 2. Image Editing

```python
from scripts.image_gen import edit_image

result = edit_image(
    prompt="Change the sky to a dramatic sunset",
    source_image="landscape.png",
    resolution="2K"
)
```

Common edit operations:
- Background replacement
- Color adjustments
- Object removal/addition
- Style transfer

### 3. Multi-Image Composition

```python
from scripts.image_gen import compose_images

result = compose_images(
    prompt="Create a seamless collage with vintage aesthetic",
    source_images=["photo1.png", "photo2.png"],
    aspect_ratio="16:9",
    resolution="2K"
)
```

## Output Handling

- **Default location**: Current working directory
- **Default filename**: `image_YYYYMMDD_HHMMSS.png`
- **Custom path**: `--output` or `output_path`
- **Custom filename**: `--filename` or `filename`

## Error Handling

Automatic retry: 1 retry on failure with 1s delay. Returns detailed error message if both attempts fail.

## Integration with Other Skills

```python
import subprocess
import os

skill_dir = "/path/to/zenmux-image-gen"

# Use uv run for isolated execution
subprocess.run([
    "uv", "run", "--directory", skill_dir,
    "python", "scripts/image_gen.py", "generate",
    "Abstract gradient background",
    "--ratio", "21:9",
    "--output", "./public/images",
    "--filename", "hero-bg.png"
])
```

## CLI Reference

```
image_gen.py generate <prompt> [options]
image_gen.py edit <prompt> <source> [options]
image_gen.py compose <prompt> <sources...> [options]

Options:
  --ratio, -r        Aspect ratio (1:1, 2:3, 3:2, 4:3, 3:4, 9:16, 16:9, 21:9)
  --resolution, -res Resolution (1K, 2K, 4K)
  --output, -o       Output directory
  --filename, -f     Output filename
```
