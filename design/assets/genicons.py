from PIL import Image

file_base = "CGOL game icon "

# 1. Open your largest square image as the base (e.g., 256x256)
main_img = Image.open(file_base + "256x256" + ".png")

# 2. Open all your other smaller sizes
sizes_to_include = [
    Image.open(file_base + "128x128" + ".png"),
    Image.open(file_base + "48x48" + ".png"),
    Image.open(file_base + "32x32" + ".png"),  # Recommended for taskbars
    Image.open(file_base + "24x24" + ".png"),
    Image.open(file_base + "16x16" + ".png")   # Recommended for window corners
]

# 3. Save them combined into a single .ico file
main_img.save("CGOL_game.ico", format="ICO", append_images=sizes_to_include)
print("Successfully created my_icon.ico!")
