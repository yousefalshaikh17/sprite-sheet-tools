import argparse
import pathlib
from PIL import Image
import os
import sys
import shutil
import json

def get_args():
    description = "Splits all sprites in a sprite sheet into their own files."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-i",
                        "--input",
                        type=pathlib.Path,
                        required=True,
                        help="path to the sprite sheet file")
    
    parser.add_argument("-o",
                        "--output",
                        type=pathlib.Path,
                        required=True,
                        help="path to the output folder")
    
    parser.add_argument("--sprite_size",
                        type=int,
                        nargs=2,
                        required=False,
                        help="size of each sprite. Not required if metadata file is provided. Overrides metadata parameters.")
    
    parser.add_argument("--sprite_padding",
                        type=int,
                        nargs=2,
                        required=False,
                        help="padding to apply for all sprites. Overrides metadata parameters. Defaults to (0,0)")
    
    parser.add_argument("-labels",
                        "--label_path",
                        type=pathlib.Path,
                        required=False,
                        help="optional path to a label file to label each file. Overrides metadata parameters.")
    
    parser.add_argument("-separator",
                        "--file_name_separator",
                        type=str,
                        default=" ",
                        required=False,
                        help="separator on resulting file names when a label is provided. (Example: ' ', '-', '_')")
    
    parser.add_argument("--clear_directory",
                        type=bool,
                        default=False,
                        required=False,
                        help="determines whether the output directory should be cleared before inserting new sprites.")
    
    parser.add_argument("--ignore_metadata",
                        type=bool,
                        action="store_true",
                        help="determines whether to use metadata if found in the same directory.")
    
    parser.add_argument("--disinclude_blank_sprites",
                        type=bool,
                        action="store_true",
                        help="determines whether blank sprites should be disincluded.")
    
    return parser.parse_args()


def get_image_section(image, position, size):
    """
    Opens an image and retrieves a 100x100 part at a specific position.

    Parameters:
        image_path (str): The path to the image file.
        position (tuple): A tuple (x, y) representing the top-left corner of the desired section.
        size (tuple): A tuple (width, height) representing the size of the section.

    Returns:
        cropped_img (PIL.Image.Image): The cropped image section.
    """
    
    # Calculate the coordinates of the box to crop (left, upper, right, lower)
    left = position[0]
    top = position[1]
    right = left + size[0]
    bottom = top + size[1]
    
    # Crop the image
    cropped_img = image.crop((left, top, right, bottom))
    
    return cropped_img

def split_sprite_sheet(image, size, padding = (0,0)):

    sprite_width, sprite_height = size
    padding_x, padding_y = padding

    images = []

    image_index = 0
    for y in range(0, image.size[0] - sprite_width + 1, sprite_width + padding_x):
        for x in range(0, image.size[1] - sprite_height + 1, sprite_height + padding_y):
            image_index += 1

            cropped_img = get_image_section(image, (x,y), size)
            images.append(cropped_img)
    
    return images

def image_is_blank(image):
    """
    Checks if the PIL Image is transparent/blank.

    Parameters:
        image (PIL.Image.Image): The image object.

    Returns:
        is_blank (bool): Whether the image is blank or not.
    """
    # @TODO: Handle off scale that RGBA isnt used.
    alpha_channel = image.getchannel("A")
    alpha_values = list(alpha_channel.getdata())
    return all(alpha == 0 for alpha in alpha_values)

def process_arguments(args):
    """
    Validates and process arguments provided through the command line.
    """
    # Process labels
    labels = []
    if args.label_path is not None:
        if not args.label_path.exists():
            return f"Error: label file {args.input} does not exist!"
        with open(args.label_path, 'r') as label_file:
            labels = [line.strip() for line in label_file.readlines()]
    args.labels = labels

    if not args.ignore_metadata:
        metadata_file = args.input.with_name(args.input.stem + "-metadata.json")
        if metadata_file.exists():
            print("Found attached metadata.")
            with open(metadata_file, 'r') as file:
                data = json.load(file)
            
            if args.sprite_size is None:
                args.sprite_size = (data["sprite_size"]["width"], data["sprite_size"]["height"])
                print(f"sprite_size overrided by metadata to {args.sprite_size}")
            if args.sprite_padding is None:
                args.sprite_padding = (data["sprite_padding"]["horizontal"], data["sprite_padding"]["vertical"])
                print(f"sprite_padding overrided by metadata to {args.sprite_padding}")
            if args.label_path is None and "labels" in data:
                args.labels = data["labels"]
                print(f"labels were overrided by metadata.")

    
    # Check if either metadata or sprite size are provided.
    if args.sprite_size is None:
        return "Error: sprite size was not provided."
    
    # Apply default value to padding if it hasn't been defined in args or metadata.
    if args.sprite_padding is None:
        args.sprite_padding = (0,0)

    # Verify that the inputs exist
    if not args.input.exists():
        return f"Error: sprite sheet file {args.input} does not exist!"
    return None


def main():
    args = get_args()
    error_message = process_arguments(args)
    if error_message is not None:
        print(error_message, file=sys.stderr)
        return
    
    # Open image
    try:
        with Image.open(args.input) as image:
            image = image.convert("RGBA")
    except:
        print("Image failed to load.")
        return
    
    sprite_size = args.sprite_size
    sprite_padding = args.sprite_padding
    labels = args.labels

    # Verify that image size is greater than sprite size
    if image.size[0] >= sprite_size[0] and image.size[1] >= sprite_size[1]:
        
        # Clear directory if requested.
        if args.clear_directory:
            if os.path.exists(args.output):
                shutil.rmtree(args.output)

        # Ensure the folder exists
        if not os.path.exists(args.output):
            os.makedirs(args.output)

        # Split the sheet into individual sprites.
        sprites = split_sprite_sheet(image, sprite_size, sprite_padding)

        label_separator = args.file_name_separator

        # If there is a number mismatch, warn the user.
        if len(labels) != len(sprites):
            print(f"[ WARNING ]  label count does not match sprite count. ({len(labels)} != {len(sprites)})")

        for i,sprite in enumerate(sprites):
            if args.disinclude_blank_sprites and image_is_blank(sprite):
                continue
            
            # Determine ideal label name
            if len(labels) > i and labels[i] is not None and len(labels[i]) > 0:
                file_name = label_separator.join([str(i+1), labels[i]])
            else:
                file_name = str(i+1)

            # Save sprite file
            save_path = os.path.join(args.output, f"{file_name}.png")
            sprite.save(save_path, format="PNG")

            # Close the image
            sprite.close()

    else:
        print("sheet is smaller than input sprite size.")

    image.close()
    print("done.")

if __name__ == "__main__":
    main()