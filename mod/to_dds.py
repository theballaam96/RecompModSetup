from PIL import Image

if __name__ == "__main__":
    img = Image.open("thumb.png")
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    img.save("thumb.dds", format="DDS")