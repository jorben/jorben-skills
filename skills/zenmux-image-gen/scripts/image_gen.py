#!/usr/bin/env python3
"""
Zenmux Image Generation Script
Uses Google GenAI API for image generation, editing, and composition.
"""

import os
import sys
import argparse
import base64
from datetime import datetime
from pathlib import Path
import time

# Supported aspect ratios and their dimensions at different resolutions
ASPECT_RATIOS = {
    "1:1": {"1K": (1024, 1024), "2K": (2048, 2048), "4K": (4096, 4096)},
    "2:3": {"1K": (682, 1024), "2K": (1365, 2048), "4K": (2730, 4096)},
    "3:2": {"1K": (1024, 682), "2K": (2048, 1365), "4K": (4096, 2730)},
    "4:3": {"1K": (1024, 768), "2K": (2048, 1536), "4K": (4096, 3072)},
    "3:4": {"1K": (768, 1024), "2K": (1536, 2048), "4K": (3072, 4096)},
    "9:16": {"1K": (576, 1024), "2K": (1152, 2048), "4K": (2304, 4096)},
    "16:9": {"1K": (1024, 576), "2K": (2048, 1152), "4K": (4096, 2304)},
    "21:9": {"1K": (1024, 438), "2K": (2048, 877), "4K": (4096, 1754)},
}

DEFAULT_ASPECT_RATIO = "1:1"
DEFAULT_RESOLUTION = "1K"
MAX_RETRIES = 1


def get_env_config():
    """Get API configuration from environment variables."""
    api_base = os.environ.get("ZENMUX_API_BASE")
    api_key = os.environ.get("ZENMUX_API_KEY")
    model_id = os.environ.get("ZENMUX_MODEL_IMAGE")
    
    missing = []
    if not api_base:
        missing.append("ZENMUX_API_BASE")
    if not api_key:
        missing.append("ZENMUX_API_KEY")
    if not model_id:
        missing.append("ZENMUX_MODEL_IMAGE")
    
    if missing:
        print(f"Error: Missing required environment variables: {', '.join(missing)}")
        sys.exit(1)
    
    return api_base, api_key, model_id


def generate_filename(prefix="image", extension="png"):
    """Generate a filename with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{prefix}_{timestamp}.{extension}"


def load_image_as_base64(image_path: str) -> str:
    """Load an image file and return its base64 encoding."""
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def save_image_from_base64(base64_data: str, output_path: str):
    """Save base64 encoded image data to a file."""
    image_data = base64.b64decode(base64_data)
    with open(output_path, "wb") as f:
        f.write(image_data)


def create_genai_client(api_base: str, api_key: str):
    """Create and return a Google GenAI client."""
    try:
        from google import genai
    except ImportError:
        print("Error: google-genai package not installed.")
        print("Install with: pip install google-genai")
        sys.exit(1)
    
    client = genai.Client(
        api_key=api_key,
        http_options={"api_version": "v1", "base_url": api_base},
        vertexai=True
    )
    return client


def generate_image(
    prompt: str,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    output_path: str = None,
    filename: str = None,
    reference_images: list = None,
    edit_mode: bool = False,
):
    """
    Generate or edit an image using the Zenmux API.
    
    Args:
        prompt: Text description of the image to generate
        aspect_ratio: Image aspect ratio (1:1, 2:3, 3:2, 4:3, 3:4, 9:16, 16:9, 21:9)
        resolution: Image resolution (1K, 2K, 4K)
        output_path: Directory to save the image (default: current directory)
        filename: Custom filename (default: timestamp-based)
        reference_images: List of image paths for editing/composition
        edit_mode: Whether this is an edit operation
    
    Returns:
        Path to the saved image or None on failure
    """
    api_base, api_key, model_id = get_env_config()
    
    # Validate aspect ratio and resolution
    if aspect_ratio not in ASPECT_RATIOS:
        print(f"Error: Invalid aspect ratio '{aspect_ratio}'.")
        print(f"Supported ratios: {', '.join(ASPECT_RATIOS.keys())}")
        return None
    
    if resolution not in ASPECT_RATIOS[aspect_ratio]:
        print(f"Error: Invalid resolution '{resolution}'.")
        print(f"Supported resolutions: 1K, 2K, 4K")
        return None
    
    # Get dimensions
    width, height = ASPECT_RATIOS[aspect_ratio][resolution]
    
    # Prepare output path
    if output_path is None:
        output_path = os.getcwd()
    output_path = Path(output_path)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Prepare filename
    if filename is None:
        filename = generate_filename()
    if not filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
        filename += ".png"
    
    full_output_path = output_path / filename
    
    # Create client
    client = create_genai_client(api_base, api_key)
    
    # Prepare content for API call
    contents = []
    
    # Add reference images if provided (for editing/composition)
    if reference_images:
        from google.genai import types
        for img_path in reference_images:
            if os.path.exists(img_path):
                img_data = load_image_as_base64(img_path)
                # Determine mime type
                ext = Path(img_path).suffix.lower()
                mime_map = {'.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp'}
                mime_type = mime_map.get(ext, 'image/png')
                contents.append(types.Part.from_bytes(data=base64.b64decode(img_data), mime_type=mime_type))
            else:
                print(f"Warning: Reference image not found: {img_path}")
    
    # Add the prompt
    contents.append(prompt)
    
    # Make API call with retry logic
    last_error = None
    for attempt in range(MAX_RETRIES + 1):
        try:
            from google.genai import types
            
            # Build config with aspect ratio
            config = types.GenerateContentConfig(
                response_modalities=["image", "text"],
                image_config=types.ImageConfig(
                    aspect_ratio=aspect_ratio,
                ),
            )
            
            response = client.models.generate_content(
                model=model_id,
                contents=contents,
                config=config,
            )
            
            # Extract and save image from response
            if response.candidates:
                for part in response.candidates[0].content.parts:
                    # Check inline_data first (standard Google models)
                    if hasattr(part, 'inline_data') and part.inline_data and part.inline_data.data:
                        image_data = part.inline_data.data
                        with open(full_output_path, "wb") as f:
                            f.write(image_data)
                        print(f"Image saved to: {full_output_path}")
                        return str(full_output_path)
                    
                    # Check file_data (ming model returns base64 data URI)
                    if hasattr(part, 'file_data') and part.file_data:
                        file_uri = part.file_data.file_uri
                        if file_uri and file_uri.startswith('data:image'):
                            # Parse base64 data URI: data:image/png;base64,xxxxx
                            header, b64_data = file_uri.split(',', 1)
                            image_data = base64.b64decode(b64_data)
                            with open(full_output_path, "wb") as f:
                                f.write(image_data)
                            print(f"Image saved to: {full_output_path}")
                            return str(full_output_path)
            
            print("Error: No image data in response")
            return None
            
        except Exception as e:
            last_error = e
            if attempt < MAX_RETRIES:
                print(f"Attempt {attempt + 1} failed, retrying...")
                time.sleep(1)
            else:
                print(f"Error: Image generation failed after {MAX_RETRIES + 1} attempts")
                print(f"Last error: {last_error}")
                return None
    
    return None


def edit_image(
    prompt: str,
    source_image: str,
    aspect_ratio: str = None,
    resolution: str = DEFAULT_RESOLUTION,
    output_path: str = None,
    filename: str = None,
):
    """
    Edit an existing image based on a prompt.
    
    Args:
        prompt: Instructions for how to edit the image
        source_image: Path to the source image to edit
        aspect_ratio: Output aspect ratio (default: keep original)
        resolution: Output resolution
        output_path: Directory to save the result
        filename: Custom filename for the result
    
    Returns:
        Path to the saved edited image or None on failure
    """
    if not os.path.exists(source_image):
        print(f"Error: Source image not found: {source_image}")
        return None
    
    if aspect_ratio is None:
        aspect_ratio = DEFAULT_ASPECT_RATIO
    
    return generate_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        output_path=output_path,
        filename=filename,
        reference_images=[source_image],
        edit_mode=True,
    )


def compose_images(
    prompt: str,
    source_images: list,
    aspect_ratio: str = DEFAULT_ASPECT_RATIO,
    resolution: str = DEFAULT_RESOLUTION,
    output_path: str = None,
    filename: str = None,
):
    """
    Compose multiple images into one based on a prompt.
    
    Args:
        prompt: Instructions for how to compose the images
        source_images: List of paths to source images
        aspect_ratio: Output aspect ratio
        resolution: Output resolution
        output_path: Directory to save the result
        filename: Custom filename for the result
    
    Returns:
        Path to the saved composed image or None on failure
    """
    valid_images = []
    for img_path in source_images:
        if os.path.exists(img_path):
            valid_images.append(img_path)
        else:
            print(f"Warning: Image not found: {img_path}")
    
    if not valid_images:
        print("Error: No valid source images provided")
        return None
    
    return generate_image(
        prompt=prompt,
        aspect_ratio=aspect_ratio,
        resolution=resolution,
        output_path=output_path,
        filename=filename,
        reference_images=valid_images,
        edit_mode=False,
    )


def main():
    parser = argparse.ArgumentParser(description="Zenmux Image Generation Tool")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Generate command
    gen_parser = subparsers.add_parser("generate", help="Generate a new image from text")
    gen_parser.add_argument("prompt", help="Text description of the image")
    gen_parser.add_argument("--ratio", "-r", default=DEFAULT_ASPECT_RATIO, 
                          choices=list(ASPECT_RATIOS.keys()),
                          help=f"Aspect ratio (default: {DEFAULT_ASPECT_RATIO})")
    gen_parser.add_argument("--resolution", "-res", default=DEFAULT_RESOLUTION,
                          choices=["1K", "2K", "4K"],
                          help=f"Resolution (default: {DEFAULT_RESOLUTION})")
    gen_parser.add_argument("--output", "-o", help="Output directory")
    gen_parser.add_argument("--filename", "-f", help="Output filename")
    
    # Edit command
    edit_parser = subparsers.add_parser("edit", help="Edit an existing image")
    edit_parser.add_argument("prompt", help="Edit instructions")
    edit_parser.add_argument("source", help="Source image path")
    edit_parser.add_argument("--ratio", "-r", choices=list(ASPECT_RATIOS.keys()),
                           help="Output aspect ratio")
    edit_parser.add_argument("--resolution", "-res", default=DEFAULT_RESOLUTION,
                           choices=["1K", "2K", "4K"],
                           help=f"Resolution (default: {DEFAULT_RESOLUTION})")
    edit_parser.add_argument("--output", "-o", help="Output directory")
    edit_parser.add_argument("--filename", "-f", help="Output filename")
    
    # Compose command
    compose_parser = subparsers.add_parser("compose", help="Compose multiple images")
    compose_parser.add_argument("prompt", help="Composition instructions")
    compose_parser.add_argument("sources", nargs="+", help="Source image paths")
    compose_parser.add_argument("--ratio", "-r", default=DEFAULT_ASPECT_RATIO,
                              choices=list(ASPECT_RATIOS.keys()),
                              help=f"Output aspect ratio (default: {DEFAULT_ASPECT_RATIO})")
    compose_parser.add_argument("--resolution", "-res", default=DEFAULT_RESOLUTION,
                              choices=["1K", "2K", "4K"],
                              help=f"Resolution (default: {DEFAULT_RESOLUTION})")
    compose_parser.add_argument("--output", "-o", help="Output directory")
    compose_parser.add_argument("--filename", "-f", help="Output filename")
    
    args = parser.parse_args()
    
    if args.command == "generate":
        result = generate_image(
            prompt=args.prompt,
            aspect_ratio=args.ratio,
            resolution=args.resolution,
            output_path=args.output,
            filename=args.filename,
        )
    elif args.command == "edit":
        result = edit_image(
            prompt=args.prompt,
            source_image=args.source,
            aspect_ratio=args.ratio,
            resolution=args.resolution,
            output_path=args.output,
            filename=args.filename,
        )
    elif args.command == "compose":
        result = compose_images(
            prompt=args.prompt,
            source_images=args.sources,
            aspect_ratio=args.ratio,
            resolution=args.resolution,
            output_path=args.output,
            filename=args.filename,
        )
    else:
        parser.print_help()
        sys.exit(1)
    
    if result:
        sys.exit(0)
    else:
        sys.exit(1)


if __name__ == "__main__":
    main()
