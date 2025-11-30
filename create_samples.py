"""
Create sample fashion images for testing
Generates placeholder images with fashion item categories
"""

from PIL import Image, ImageDraw, ImageFont
import random
from pathlib import Path


def create_sample_fashion_image(category, index, save_path):
    """Create a placeholder fashion image"""
    # Random pastel color for each category
    colors = {
        'dress': [(255, 182, 193), (255, 192, 203), (255, 160, 180)],
        'shirt': [(173, 216, 230), (176, 224, 230), (135, 206, 235)],
        'pants': [(221, 160, 221), (218, 112, 214), (186, 85, 211)],
        'shoes': [(255, 218, 185), (255, 222, 173), (255, 228, 181)],
        'bag': [(152, 251, 152), (144, 238, 144), (143, 188, 143)],
        'jacket': [(255, 215, 0), (255, 223, 0), (255, 235, 0)],
        'skirt': [(255, 192, 203), (255, 182, 193), (255, 174, 185)],
        'accessory': [(230, 230, 250), (216, 191, 216), (221, 160, 221)]
    }

    # Create image
    width, height = 400, 600
    color = random.choice(colors.get(category, [(200, 200, 200)]))
    img = Image.new('RGB', (width, height), color=color)
    draw = ImageDraw.Draw(img)

    # Add text
    try:
        # Try to use a nice font
        font_large = ImageFont.truetype("arial.ttf", 60)
        font_small = ImageFont.truetype("arial.ttf", 30)
    except:
        # Fallback to default
        font_large = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw category name
    text = category.upper()
    bbox = draw.textbbox((0, 0), text, font=font_large)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    x = (width - text_width) // 2
    y = height // 2 - 50

    # Shadow effect
    draw.text((x + 3, y + 3), text, fill=(0, 0, 0, 128), font=font_large)
    draw.text((x, y), text, fill=(255, 255, 255), font=font_large)

    # Draw index
    index_text = f"Sample #{index + 1}"
    bbox = draw.textbbox((0, 0), index_text, font=font_small)
    text_width = bbox[2] - bbox[0]
    x = (width - text_width) // 2
    y = height // 2 + 50
    draw.text((x, y), index_text, fill=(255, 255, 255), font=font_small)

    # Add decorative border
    border_color = tuple(max(0, c - 50) for c in color)
    draw.rectangle([0, 0, width-1, height-1], outline=border_color, width=10)

    # Add some decorative elements
    for _ in range(20):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        size = random.randint(5, 20)
        overlay_color = tuple(min(255, c + random.randint(-30, 30)) for c in color)
        draw.ellipse([x1, y1, x1+size, y1+size], fill=overlay_color)

    # Save
    img.save(save_path, quality=95)


def main():
    """Generate sample fashion images"""
    print("🎨 Creating sample fashion images...")

    sample_dir = Path("sample_images")
    sample_dir.mkdir(exist_ok=True)

    categories = [
        'dress', 'shirt', 'pants', 'shoes', 'bag',
        'jacket', 'skirt', 'dress', 'shirt', 'accessory'
    ]

    for idx, category in enumerate(categories):
        filename = f"sample_{category}_{idx+1}.jpg"
        save_path = sample_dir / filename

        create_sample_fashion_image(category, idx, save_path)
        print(f"✓ Created {filename}")

    print(f"\n✅ Created {len(categories)} sample images in {sample_dir}/")
    print("You can now test the app with these samples!")


if __name__ == "__main__":
    main()
