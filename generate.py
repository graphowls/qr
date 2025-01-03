import os
import argparse
import PIL
from PIL import Image, ImageDraw
import qrcode
from qrcode.image.styledpil import StyledPilImage
from qrcode.image.styles import moduledrawers
from qrcode.image.styles.moduledrawers import (
    RoundedModuleDrawer,
    VerticalBarsDrawer,
    SquareModuleDrawer,
    CircleModuleDrawer,
    GappedSquareModuleDrawer,
)
from qrcode.image.styles.colormasks import SolidFillColorMask, SquareGradiantColorMask


if not hasattr(Image, "Resampling"):
    Image.Resampling = Image
# Now PIL.Image.Resampling.BICUBIC is always recognized.


primary_accent = (29, 29, 184)
mask_accent = (29, 29, 180)
offwhite = (255, 255, 255)


# Custom function for eye styling. These create the eye masks
def style_inner_eyes(img):
    img_size = img.size[0]
    eye_size = 70  # default
    quiet_zone = 40  # default
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((60, 60, 90, 90), fill=255)  # top left eye
    draw.rectangle((img_size - 90, 60, img_size - 60, 90), fill=255)  # top right eye
    draw.rectangle((60, img_size - 90, 90, img_size - 60), fill=255)  # bottom left eye
    return mask


def style_outer_eyes(img):
    img_size = img.size[0]
    eye_size = 70  # default
    quiet_zone = 40  # default
    mask = Image.new("L", img.size, 0)
    draw = ImageDraw.Draw(mask)
    draw.rectangle((40, 40, 110, 110), fill=255)  # top left eye
    draw.rectangle((img_size - 110, 40, img_size - 40, 110), fill=255)  # top right eye
    draw.rectangle(
        (40, img_size - 110, 110, img_size - 40), fill=255
    )  # bottom left eye
    draw.rectangle((60, 60, 90, 90), fill=0)  # top left eye
    draw.rectangle((img_size - 90, 60, img_size - 60, 90), fill=0)  # top right eye
    draw.rectangle((60, img_size - 90, 90, img_size - 60), fill=0)  # bottom left eye
    return mask


def generate_qr(url: str, is_mask: bool = False, is_round: bool = False):
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)

    qr.add_data(url)

    qr_inner_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        # eye_drawer=RoundedModuleDrawer(radius_ratio=1),
        color_mask=SolidFillColorMask(back_color=offwhite, front_color=primary_accent),
        module_drawer=RoundedModuleDrawer() if is_round else GappedSquareModuleDrawer(),
    )

    qr_outer_eyes_img = qr.make_image(
        image_factory=StyledPilImage,
        # eye_drawer=RoundedModuleDrawer(radius_ratio=1)
    )

    logo_path = (
        "assets/graphowls-rounded-logo.png"
        if is_round
        else "assets/graphowls-square-logo.png"
    )

    if is_mask:
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer()
            if is_round
            else GappedSquareModuleDrawer(),
            embeded_image_path=logo_path,
            color_mask=SquareGradiantColorMask(edge_color=mask_accent),
            back_color=offwhite,
        )
    else:
        qr_img = qr.make_image(
            image_factory=StyledPilImage,
            module_drawer=RoundedModuleDrawer()
            if is_round
            else GappedSquareModuleDrawer(),
            embeded_image_path=logo_path,
            back_color=offwhite,
        )

    inner_eye_mask = style_inner_eyes(qr_img)
    outer_eye_mask = style_outer_eyes(qr_img)

    qr_inner_eyes_img.save("./inner_eyes_img.png")
    qr_outer_eyes_img.save("./qr_outer_eyes_img.png")
    qr_img.save("./qr_img.png")

    qr_inner_eyes_img = Image.open("./inner_eyes_img.png")
    qr_outer_eyes_img = Image.open("./qr_outer_eyes_img.png")
    qr_img = Image.open("./qr_img.png")

    intermediate_img = Image.composite(qr_inner_eyes_img, qr_img, inner_eye_mask)
    final_image = Image.composite(qr_outer_eyes_img, intermediate_img, outer_eye_mask)
    final_image.save("qr.png")

    for f in ["./inner_eyes_img.png", "./qr_outer_eyes_img.png", "./qr_img.png"]:
        os.remove(f)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="GraphOwls QR", description="Generate QR codes for the graphowls project"
    )

    parser.add_argument("url", default="https://graphowls.com")
    parser.add_argument("-m", "--mask", default=False, action="store_true")
    parser.add_argument("-r", "--rounded", default=False, action="store_true")

    args = parser.parse_args()

    generate_qr(url=args.url, is_mask=args.mask, is_round=args.rounded)
