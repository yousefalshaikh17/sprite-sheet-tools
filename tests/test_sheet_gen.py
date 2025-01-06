"""
tests for the sprite sheet generator
"""
import unittest
import pathlib
from PIL import Image
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sprite_sheet_generator


def test_existance(file_path):
    """
    test if file exists and raise ValueError if not
    Args:
        file_path (pathlib.Path)
    Raises:
        ValueError if does not exist
    """
    if not file_path.exists():
        raise ValueError(f"Test cannot be run as data file {str(file_path)} doesn't exist!")
    
def images_are_equal(image1, image2):
    # Check if the images have the same size
    if image1.size != image2.size:
        return False

    # Check if the images have the same mode
    if image1.mode != image2.mode:
        return False

    # Normalize both images to RGBA for consistent comparison
    image1 = image1.convert("RGBA")
    image2 = image2.convert("RGBA")

    # Compare bytes
    if image1.tobytes() != image2.tobytes():
        return False

    return True

def test_metadata(self, metadata, expected_sheet_size, grid_size, padding, sprite_size):
    self.assertEqual(
        expected_sheet_size,
        (metadata["sheet_size"]["width"], metadata["sheet_size"]["height"]),
        msg="sprite_sheet_split.test_sprite_sheet_gen1 (Metatable sheet size did not match expected size.)"
        )
    
    self.assertEqual(
        grid_size,
        (metadata["grid_size"]["rows"], metadata["grid_size"]["cols"]),
        msg="sprite_sheet_split.test_sprite_sheet_gen1 (Metatable grid size did not match assigned size.)"
        )
    
    self.assertEqual(
        padding,
        (metadata["sprite_padding"]["horizontal"], metadata["sprite_padding"]["horizontal"]),
        msg="sprite_sheet_split.test_sprite_sheet_gen1 (Metatable padding did not match assigned padding.)"
        )
    
    self.assertEqual(
        sprite_size,
        (metadata["sprite_size"]["width"], metadata["sprite_size"]["weight"]),
        msg="sprite_sheet_split.test_sprite_sheet_gen1 (Metatable sprite size did not match expected sprite size.)"
        )

class TestSpriteSheetGenerator(unittest.TestCase):
    """
    tests of sprite sheet generator
    """

    def setUp(self):
        """
        build a full test class
        """
        data_directory = pathlib.Path(__file__).resolve().parent.joinpath("data")

        path = data_directory.joinpath("2x2_sprite_sheet.png")
        test_existance(path)
        self.sprite_sheet_2x2 = Image.open(path)

        path = data_directory.joinpath("2x2_sprite_sheet_padded_20.png")
        test_existance(path)
        self.sprite_sheet_2x2_padded = Image.open(path)

        path = data_directory.joinpath("4x1_sprite_sheet.png")
        test_existance(path)
        self.sprite_sheet_4x1 = Image.open(path)

        path = data_directory.joinpath("4x1_sprite_sheet_padded_10.png")
        test_existance(path)
        self.sprite_sheet_4x1_padded = Image.open(path)

        sprites = []
        for i in range(1,5):
            path = data_directory.joinpath(f"sprite_entry_{i}.png")
            test_existance(path)
            sprites.append(Image.open(path))
        self.sprites = sprites
        

    def tearDown(self):
        """
        clean up
        """
        self.sprite_sheet_2x2.close()
        self.sprite_sheet_2x2_padded.close()
        self.sprite_sheet_4x1.close()
        self.sprite_sheet_4x1_padded.close()
        for sprite in self.sprites:
            sprite.close()

    def test_sprite_sheet_gen1(self):
        """
        test checking if image can be generated properly.
        """
        sprites = self.sprites
        padding = (0,0)
        grid_size = (2,2)
        sprite_size = sprites[0].size
        expected_sheet_size = (100,100)
        
        sprite_sheet, metadata = sprite_sheet_generator.stitch_images(sprites, grid_size, padding)
        
        self.assertEqual(expected_sheet_size, sprite_sheet.size, msg="sprite_sheet_split.test_sprite_sheet_gen1 (Sheet size did not match expected size.)")

        self.assertTrue(
            images_are_equal(
                sprite_sheet.convert("RGBA"),
                self.sprite_sheet_2x2.convert("RGBA")
            ),
            msg="sprite_sheet_split.test_sprite_sheet_gen1 (Resulting sprite sheet is not equal.)"
            )

        # Metadata check
        test_metadata(self, metadata, expected_sheet_size, grid_size, padding, sprite_size)

    def test_sprite_sheet_gen2(self):
        """
        test checking if image can be generated properly. This time padding is applied.
        """
        sprites = self.sprites
        padding = (20,20)
        grid_size = (2,2)
        sprite_size = sprites[0].size
        expected_sheet_size = (120,120)
        
        sprite_sheet, metadata = sprite_sheet_generator.stitch_images(sprites, grid_size, padding)
        
        self.assertEqual(expected_sheet_size, sprite_sheet.size, msg="sprite_sheet_split.test_sprite_sheet_gen2 (Sheet size did not match expected size.)")

        self.assertTrue(
            images_are_equal(
                sprite_sheet.convert("RGBA"),
                self.sprite_sheet_2x2_padded.convert("RGBA")
            ),
            msg="sprite_sheet_split.test_sprite_sheet_gen2 (Resulting sprite sheet is not equal.)"
            )

        # Metadata check
        test_metadata(self, metadata, expected_sheet_size, grid_size, padding, sprite_size)


    def test_sprite_sheet_gen3(self):
        """
        test checking if image can be generated properly. This time grid size is adjusted.
        """
        sprites = self.sprites
        padding = (0,0)
        grid_size = (1,4)
        sprite_size = sprites[0].size
        expected_sheet_size = (200,50)
        
        sprite_sheet, metadata = sprite_sheet_generator.stitch_images(sprites, grid_size, padding)

        self.assertEqual(expected_sheet_size, sprite_sheet.size, msg="sprite_sheet_split.test_sprite_sheet_gen3 (Sheet size did not match expected size.)")
        
        self.assertTrue(
            images_are_equal(
                sprite_sheet.convert("RGBA"),
                self.sprite_sheet_4x1.convert("RGBA")
            ),
            msg="sprite_sheet_split.test_sprite_sheet_gen3 (Resulting sprite sheet is not equal.)"
            )

        # Metadata check
        test_metadata(self, metadata, expected_sheet_size, grid_size, padding, sprite_size)


    def test_sprite_sheet_gen4(self):
        """
        test checking if image can be generated properly. This time the resulting sheet is padded and grid size is adjusted.
        """
        sprites = self.sprites
        padding = (10,10)
        grid_size = (1,4)
        sprite_size = sprites[0].size
        expected_sheet_size = (230,50)
        
        sprite_sheet, metadata = sprite_sheet_generator.stitch_images(sprites, grid_size, padding)

        self.assertEqual(expected_sheet_size, sprite_sheet.size, msg="sprite_sheet_split.test_sprite_sheet_gen4 (Sheet size did not match expected size.)")
        
        self.assertTrue(
            images_are_equal(
                sprite_sheet.convert("RGBA"),
                self.sprite_sheet_4x1_padded.convert("RGBA")
            ),
            msg="sprite_sheet_split.test_sprite_sheet_gen4 (Resulting sprite sheet is not equal.)"
            )

        # Metadata check
        test_metadata(self, metadata, expected_sheet_size, grid_size, padding, sprite_size)

        