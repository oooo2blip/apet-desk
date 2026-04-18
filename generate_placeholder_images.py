from PIL import Image, ImageDraw, ImageFont
import os

images_dir = os.path.join(os.path.dirname(__file__), "images")
os.makedirs(images_dir, exist_ok=True)

def create_cat_image(state: str, size: int = 200):
    img = Image.new("RGBA", (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)
    
    center = size // 2
    cat_radius = 60
    ear_size = 25
    eye_size = 8
    nose_size = 6
    
    if state == "idle":
        body_color = (255, 165, 0, 255)
        inner_ear_color = (255, 182, 193, 255)
        eye_color = (0, 0, 0, 255)
        nose_color = (255, 192, 203, 255)
        draw.ellipse([center - cat_radius, center - cat_radius + 20,
                      center + cat_radius, center + cat_radius + 20],
                     fill=body_color)
        draw.ellipse([center - 45, center - 60,
                      center + 45, center + 10],
                     fill=body_color)
        draw.polygon([center - 35, center - 40,
                      center - 50, center - 70,
                      center - 20, center - 55],
                     fill=body_color)
        draw.polygon([center + 35, center - 40,
                      center + 50, center - 70,
                      center + 20, center - 55],
                     fill=body_color)
        draw.polygon([center - 35, center - 45,
                      center - 45, center - 60,
                      center - 28, center - 52],
                     fill=inner_ear_color)
        draw.polygon([center + 35, center - 45,
                      center + 45, center - 60,
                      center + 28, center - 52],
                     fill=inner_ear_color)
        draw.ellipse([center - 15, center - 25,
                      center - 15 + eye_size, center - 25 + eye_size],
                     fill=eye_color)
        draw.ellipse([center + 8, center - 25,
                      center + 8 + eye_size, center - 25 + eye_size],
                     fill=eye_color)
        draw.ellipse([center - nose_size, center - 12,
                      center + nose_size, center - 6],
                     fill=nose_color)
        draw.arc([center - 10, center - 10,
                  center + 10, center],
                 start=180, end=360, fill=(0, 0, 0, 255), width=2)
        draw.line([center - 35, center - 15, center - 18, center - 18],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center - 35, center - 10, center - 18, center - 12],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center + 18, center - 18, center + 35, center - 15],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center + 18, center - 12, center + 35, center - 10],
                  fill=(0, 0, 0, 255), width=2)
    
    elif state == "happy":
        body_color = (255, 165, 0, 255)
        inner_ear_color = (255, 182, 193, 255)
        nose_color = (255, 192, 203, 255)
        blush_color = (255, 182, 193, 200)
        draw.ellipse([center - cat_radius, center - cat_radius + 10,
                      center + cat_radius, center + cat_radius + 10],
                     fill=body_color)
        draw.ellipse([center - 45, center - 70,
                      center + 45, center],
                     fill=body_color)
        draw.polygon([center - 35, center - 50,
                      center - 50, center - 80,
                      center - 20, center - 65],
                     fill=body_color)
        draw.polygon([center + 35, center - 50,
                      center + 50, center - 80,
                      center + 20, center - 65],
                     fill=body_color)
        draw.polygon([center - 35, center - 55,
                      center - 45, center - 70,
                      center - 28, center - 62],
                     fill=inner_ear_color)
        draw.polygon([center + 35, center - 55,
                      center + 45, center - 70,
                      center + 28, center - 62],
                     fill=inner_ear_color)
        draw.arc([center - 15, center - 35,
                  center - 5, center - 20],
                 start=180, end=360, fill=(0, 0, 0, 255), width=3)
        draw.arc([center + 5, center - 35,
                  center + 15, center - 20],
                 start=180, end=360, fill=(0, 0, 0, 255), width=3)
        draw.ellipse([center - nose_size, center - 18,
                      center + nose_size, center - 12],
                     fill=nose_color)
        draw.arc([center - 15, center - 18,
                  center + 15, center - 5],
                 start=180, end=360, fill=(0, 0, 0, 255), width=3)
        draw.ellipse([center - 30, center - 25,
                      center - 18, center - 15],
                     fill=blush_color)
        draw.ellipse([center + 18, center - 25,
                      center + 30, center - 15],
                     fill=blush_color)
        draw.line([center - 35, center - 22, center - 18, center - 25],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center - 35, center - 17, center - 18, center - 19],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center + 18, center - 25, center + 35, center - 22],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center + 18, center - 19, center + 35, center - 17],
                  fill=(0, 0, 0, 255), width=2)
    
    elif state == "sad":
        body_color = (200, 150, 100, 255)
        inner_ear_color = (200, 150, 170, 255)
        eye_color = (0, 0, 0, 255)
        nose_color = (200, 150, 160, 255)
        tear_color = (100, 180, 255, 200)
        draw.ellipse([center - cat_radius, center - cat_radius + 20,
                      center + cat_radius, center + cat_radius + 20],
                     fill=body_color)
        draw.ellipse([center - 45, center - 60,
                      center + 45, center + 10],
                     fill=body_color)
        draw.polygon([center - 35, center - 30,
                      center - 50, center - 60,
                      center - 20, center - 45],
                     fill=body_color)
        draw.polygon([center + 35, center - 30,
                      center + 50, center - 60,
                      center + 20, center - 45],
                     fill=body_color)
        draw.polygon([center - 35, center - 35,
                      center - 45, center - 50,
                      center - 28, center - 42],
                     fill=inner_ear_color)
        draw.polygon([center + 35, center - 35,
                      center + 45, center - 50,
                      center + 28, center - 42],
                     fill=inner_ear_color)
        draw.ellipse([center - 15, center - 25,
                      center - 10, center - 18],
                     fill=eye_color)
        draw.ellipse([center + 10, center - 25,
                      center + 15, center - 18],
                     fill=eye_color)
        draw.ellipse([center - 12, center - 10,
                      center - 8, center - 5],
                     fill=tear_color)
        draw.ellipse([center + 8, center - 10,
                      center + 12, center - 5],
                     fill=tear_color)
        draw.ellipse([center - nose_size, center - 12,
                      center + nose_size, center - 6],
                     fill=nose_color)
        draw.arc([center - 10, center - 8,
                  center + 10, center + 2],
                 start=0, end=180, fill=(0, 0, 0, 255), width=2)
        draw.line([center - 35, center - 15, center - 18, center - 12],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center - 35, center - 10, center - 18, center - 8],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center + 18, center - 12, center + 35, center - 15],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center + 18, center - 8, center + 35, center - 10],
                  fill=(0, 0, 0, 255), width=2)
    
    elif state == "sleep":
        body_color = (255, 165, 0, 255)
        inner_ear_color = (255, 182, 193, 255)
        draw.ellipse([center - cat_radius, center - cat_radius + 20,
                      center + cat_radius, center + cat_radius + 20],
                     fill=body_color)
        draw.ellipse([center - 45, center - 40,
                      center + 10, center + 30],
                     fill=body_color)
        draw.polygon([center - 35, center - 20,
                      center - 50, center - 50,
                      center - 20, center - 35],
                     fill=body_color)
        draw.polygon([center - 35, center - 25,
                      center - 45, center - 40,
                      center - 28, center - 32],
                     fill=inner_ear_color)
        draw.line([center - 25, center - 10,
                   center - 15, center - 10],
                  fill=(0, 0, 0, 255), width=2)
        draw.line([center - 10, center - 10,
                   center, center - 10],
                  fill=(0, 0, 0, 255), width=2)
        try:
            font = ImageFont.truetype("arial.ttf", 16)
        except:
            font = ImageFont.load_default()
        draw.text((center + 20, center - 50), "Z", fill=(150, 150, 150, 255), font=font)
        draw.text((center + 35, center - 65), "z", fill=(150, 150, 150, 200), font=font)
        draw.text((center + 45, center - 75), "z", fill=(150, 150, 150, 150), font=font)
    
    return img

states = ["idle", "happy", "sad", "sleep"]
for state in states:
    img = create_cat_image(state)
    file_path = os.path.join(images_dir, f"{state}.png")
    img.save(file_path, "PNG")
    print(f"Created {file_path}")

print("\nPlaceholder images created successfully!")
print("You can replace these with your own PNG images.")
