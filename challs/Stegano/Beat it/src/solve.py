from PIL import Image

# Load the main image and the image to prepend
main_image_path = "hidden beat message.png"  # replace with your main image path
prepend_image_path = "spotify.jpg"  # replace with your left image path

main_img = Image.open(main_image_path)
left_img = Image.open(prepend_image_path)

# Get main image dimensions
width, height = main_img.size

# Resize the left image to match the height of the main image
left_img = left_img.resize((left_img.width, height))

# Number of vertical parts
num_parts = 7
part_width = width // num_parts

# Process slices
for i in range(num_parts):
    left = i * part_width
    right = (i + 1) * part_width if i < num_parts - 1 else width
    box = (left, 0, right, height)
    slice_img = main_img.crop(box)

    # Create new image with left image + slice
    combined_width = left_img.width + slice_img.width
    combined_img = Image.new("RGBA", (combined_width, height))
    combined_img.paste(left_img, (0, 0))
    combined_img.paste(slice_img, (left_img.width, 0))

    combined_img.save(f"new\\combined_slice_{i+1}.png")

print(f"All slices combined with the left image successfully!")
