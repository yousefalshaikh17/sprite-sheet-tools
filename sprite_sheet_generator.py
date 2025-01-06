import argparse
import pathlib
from PIL import Image
import os
import sys
import re
import json

def get_args():
    description = "Generates a sprite sheet using all sprites provided. It is recommended that all sprites are equally sized."
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-i",
                        "--input",
                        type=pathlib.Path,
                        required=True,
                        nargs='+',
                        help="path to each sprite sheet (or folder)")
    
    parser.add_argument("-o",
                        "--output",
                        type=pathlib.Path,
                        required=True,
                        help="path for output sprite sheet")
    
    parser.add_argument("-gs",
                        "--grid_size",
                        type=int,
                        nargs=2,
                        required=True,
                        help="grid size for each sheet")
    
    parser.add_argument("--sprite_padding",
                        type=int,
                        nargs=2,
                        default=(0,0),
                        help="padding to apply for all sprites")
    
    # Maybe other arguments for mesh optimization later on.
    return parser.parse_args()


def stitch_images(images, grid_size, padding=(0,0)):
    """
    Stitches all the images provided into one image.

    Parameters:
        images (list[PIL.Image.Image]): The path to the image file.
        grid_size (tuple): A tuple (row, col) representing the rows and columns of the stitched image.
        padding (tuple): A tuple (x, y) representing the padding between each image.

    Returns:
        stitched_immage (PIL.Image.Image): The stitched image.
    """
    
    # Get the width and height of all images
    widths, heights = zip(*(img.size for img in images))

    # Get number of rows and columns for the grid
    rows, cols = grid_size

    # Make sure we have enough images to fill the grid
    if len(images) > rows * cols:
        raise ValueError("The number of images exceeds the provided grid size")

    # Get max sprite size
    max_width = max(widths)
    max_height = max(heights)

    # Calculate the total width and height for the output image
    total_width = cols * max_width + (cols - 1) * padding[0]
    total_height = rows * max_height + (rows - 1) * padding[1]

    # Create a new blank image with RGBA mode to preserve transparency
    stitched_image = Image.new('RGBA', (total_width, total_height), (0,0,0,0))

    # Iterate over the images and paste them into the grid
    for idx, img in enumerate(images):
        # Calculate the position in the grid
        row = idx // cols
        col = idx % cols

        # Calculate the x and y position for this image
        x_offset = col * (max_width + padding[0])
        y_offset = row * (max_height + padding[1])

        # Paste the image at the correct position
        stitched_image.paste(img, (x_offset, y_offset))

    # Create metadata
    metadata = {
        "sprite_size": {
            "width": max_width,
            "height": max_height
        },
        "sprite_padding": {
            "horizontal": padding[0],
            "vertical": padding[1]
        },
        "grid_size": {
            "rows": rows,
            "cols": cols
        },
        "sheet_size": {
            "width": stitched_image.width,
            "height": stitched_image.height
        },
    }
        
    return stitched_image, metadata


def command_validation(args):
    """
    Validates arguments provided through the command line.
    """
    invalid_files = []
    # Verify that the inputs exist
    for input in args.input:
        if not input.exists():
            invalid_files.append(f"{input}")
    
    if len(invalid_files) > 0:
        return f"Error: These files do not exist: {', '.join(invalid_files)}"
    
    return None

def main():
    args = get_args()
    error_message = command_validation(args)
    if error_message is not None:
        print(error_message, file=sys.stderr)
        return

    images = []
    labels = []

    def process_path(path):
        if path.is_dir():
            for child in os.listdir(path):
                process_path(pathlib.Path(os.path.join(path, child)))
        else:
            # Open image and add to sheet
            # @TODO: Load each image one at a time with "lazy loading" to minimize peak memory usage.
            try:
                # Verify file
                image = Image.open(path)
                image.verify()
                image.close()

                # Process name and add to list
                processed_name = pathlib.Path(path.name).stem
                processed_name = re.sub(r'^\d+[\s_-]*', '', processed_name)
                if len(processed_name) == 0:
                    processed_name = None
                labels.append(processed_name)

                # Reopen Image
                image = Image.open(path)
                images.append(image.convert("RGBA"))
                image.close()
            except:
                print(f"Image '{path}' failed to load.")
                return False
        return True

    for path in args.input:
        if not process_path(path):
            return

    sprite_padding = args.sprite_padding
    grid_size = args.grid_size

    # Produce sprite sheet
    sheet, metadata = stitch_images(images, grid_size, sprite_padding)

    # Save sprite sheet
    output_path = args.output.with_suffix('')

    metadata["labels"] = labels

    try: 
        with open(str(output_path) + "-metadata.json", 'w') as file:
                json.dump(metadata, file, indent=4)
    except:
        print("failed to save sprite data")

    sheet.save(output_path.with_suffix('.png'), format="PNG")

    # Clean up
    for image in images:
        image.close()

    with open(str(output_path) + "-labels.txt", 'w') as label_file:
        for label in labels:
            if label is None:
                label = ""
            label_file.write(f"{label}\n")

    print("done.")


if __name__ == "__main__":
    main()