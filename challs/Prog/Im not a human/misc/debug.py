from PIL import Image, ImageDraw, ImageFont

base = Image.open("base.png").convert("RGBA")

overlay = Image.new("RGBA", base.size, (0, 0, 0, 0))
draw = ImageDraw.Draw(overlay)

slots = []

# --- Hotbar (9 slots) ---
hotbar_slots = []
for col in range(9):
    x = 48 + col * 48 + (col * 6)
    y = 426 + (48 // 2)
    hotbar_slots.append((x, y))

# --- Inventory (27 slots) ---
inventory_slots = []
for row in range(3):
    for col in range(9):
        x = 48 + col * 48 + (col * 6)
        y = 252 + (48 // 2) + row * 48 + (row * 6)
        inventory_slots.append((x, y))

# --- Armor (4 slots) ---
armor_slots = []
for row in range(4):
    x = 48
    y = 24 + (48 // 2) + row * 48 + (row * 6)
    armor_slots.append((x, y))

# --- Crafting (2x2 + output) ---
crafting_slots = []
for row in range(2):
    for col in range(2):
        x = 318 + col * 48 + (col * 6)
        y = 54 + (48 // 2) + row * 48 + (row * 6)
        crafting_slots.append((x, y))
crafting_slots.append((486, 108))  # Output slot

# --- Off-hand (1 slot) ---
offhand_slots = [(255, 210)]

# Combine all slots
slots.extend((*hotbar_slots, *inventory_slots, *armor_slots, *crafting_slots, *offhand_slots))

# Load font
try:
    font = ImageFont.truetype("DejaVuSans-Bold.ttf", 20)
except:
    font = ImageFont.load_default()

# Draw filled red rectangles with index numbers
for i, (x, y) in enumerate(slots):
    offset_x = x - 48 // 2
    offset_y = y - 48 // 2

    # Draw filled red square
    draw.rectangle(
        [offset_x, offset_y, offset_x + 47, offset_y + 47],
        fill=(128, 128, 128, 255)
    )

    # Center text using textbbox (works in Pillow ≥10)
    text = str(i)
    bbox = draw.textbbox((0, 0), text, font=font)
    
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    text_x = offset_x + (48 - text_w) / 2
    text_y = offset_y + (48 - text_h) / 2 - 4

    draw.text((text_x, text_y), text, fill=(255, 255, 255, 255), font=font)

# Merge overlay with base
result = Image.alpha_composite(base, overlay)

# Save output
result.save("debug_slots.png")
print("✅ Generated debug_slots.png with indexed red 48×48 rectangles.")
