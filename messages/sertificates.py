from PIL import Image, ImageDraw, ImageFont
import os

# Font paths - simplified for server compatibility
# Place times.ttf in the project root directory for best results
FONT_PATH = "times.ttf"
DEFAULT_LINUX_FONT = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
TEMPLATE_PATH = "template.png"

def generate_certificate(fullname: str, score: int, total: int, output_path: str):
    """
    Generates a certificate for the participant.
    fullname: Name and surname of the participant
    score: Number of correct answers
    total: Total number of questions
    output_path: Path to save the generated image
    """
    if not os.path.exists(TEMPLATE_PATH):
        # Try to find it in the parent directory if called from a subdirectory
        if os.path.exists(os.path.join("..", TEMPLATE_PATH)):
            template_p = os.path.join("..", TEMPLATE_PATH)
        else:
            raise FileNotFoundError(f"Template image not found at {TEMPLATE_PATH}")
    else:
        template_p = TEMPLATE_PATH

    # Open the template
    img = Image.open(template_p)
    draw = ImageDraw.Draw(img)
    
    # Calculate percentage
    percentage = round((score / total) * 100) if total > 0 else 0
    
    # Load fonts - strictly prioritizing local files for reliability on server
    common_linux_paths = [
        DEFAULT_LINUX_FONT,
        "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    ]
    
    # Priority: 1. Locally uploaded times.ttf, 2. Locally uploaded arial.ttf, 3. Linux defaults
    font_test_paths = [FONT_PATH, "arial.ttf"] + common_linux_paths
    
    name_font = None
    result_font = None
    
    for path in font_test_paths:
        try:
            if os.path.exists(path) or path.startswith("/usr/"):
                name_font = ImageFont.truetype(path, 90)
                result_font = ImageFont.truetype(path, 30)
                # print(f"Successfully loaded font: {path}") # Debug
                break
        except Exception:
            continue
            
    if name_font is None:
        # Extreme fallback
        name_font = ImageFont.load_default()
        result_font = ImageFont.load_default()
        # print("Warning: No fonts found. Using default tiny font.")

    # 1. Draw Name
    name_text = fullname.upper()
    name_bbox = draw.textbbox((0, 0), name_text, font=name_font)
    name_w = name_bbox[2] - name_bbox[0]
    draw.text((1000 - name_w / 2, 620), name_text, font=name_font, fill=(28, 54, 107)) # Dark blue

    # 2. Draw Results
    result_text = f"{score}/{total} ({percentage}%)"
    # Rangini asosiy matn rangi (to'q ko'k) bilan bir xil qilamiz
    draw.text((1453, 795), result_text, font=result_font, fill=(28, 54, 107))
    # Save the result
    img.save(output_path)
    return output_path
