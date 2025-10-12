from PIL import Image
import random

base = Image.open("base.png").convert("RGBA")
pane = Image.open("pane.png").convert("RGBA")

hotbar_slots = [(48, 450), (102, 450), (156, 450), (210, 450), (264, 450), (318, 450), (372, 450), (426, 450), (480, 450)]
inventory_slots = [(48, 276), (102, 276), (156, 276), (210, 276), (264, 276), (318, 276), (372, 276), (426, 276), (480, 276), (48, 330), (102, 330), (156, 330), (210, 330), (264, 330), (318, 330), (372, 330), (426, 330), (480, 330), (48, 384), (102, 384), (156, 384), (210, 384), (264, 384), (318, 384), (372, 384), (426, 384), (480, 384)]
armor_slots = [(48, 48), (48, 102), (48, 156), (48, 210)]
crafting_slots = [(318, 78), (372, 78), (318, 132), (372, 132), (486, 108)]
offhand_slots = [(255, 210)]

slots = [*hotbar_slots, *inventory_slots, *armor_slots, *crafting_slots, *offhand_slots]

slot_x, slot_y = random.choice(slots)

offset_x = slot_x - pane.width // 2
offset_y = slot_y - pane.height // 2

base.alpha_composite(pane, (offset_x, offset_y))

base.save("inventory_with_pane.png")
print(f"Pane placed at slot ({slot_x}, {slot_y} | {slots.index((slot_x, slot_y))}) and saved as inventory_with_pane.png")
