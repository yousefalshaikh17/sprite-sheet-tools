"""
tests for the sprite sheet splitter
"""
import unittest
import pathlib
from PIL import Image
from PIL.Image import Transpose
import sys
import os


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import sprite_sheet_splitter


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

class TestSpriteSheetSplitter(unittest.TestCase):
    """
    tests of sprite sheet splitter
    """

    def setUp(self):
        """
        build a full test class
        """
        data_directory = pathlib.Path(__file__).resolve().parent.joinpath("data")

        path = data_directory.joinpath("blank_image.png")
        test_existance(path)
        self.blank_image = Image.open(path)

        path = data_directory.joinpath("non_blank_image.png")
        test_existance(path)
        self.non_blank_image = Image.open(path)

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
        self.non_blank_image.close()
        self.blank_image.close()
        self.sprite_sheet_2x2.close()
        self.sprite_sheet_2x2_padded.close()
        for sprite in self.sprites:
            sprite.close()

    def test_blank_check1(self):
        """
        test checking if image is blank. This should result in blank.
        """
        prediction = sprite_sheet_splitter.image_is_blank(self.blank_image.convert('RGBA'))
        self.assertTrue(prediction, msg="sprite_sheet_split.test_blank_check1 (Image is actually blank.)")

    def test_blank_check2(self):
        """
        test checking if image is blank. This should result in non blank.
        """
        prediction = sprite_sheet_splitter.image_is_blank(self.non_blank_image.convert('RGBA'))
        self.assertFalse(prediction, msg="sprite_sheet_split.test_blank_check2 (Image is not actually blank.)")

    def test_sprite_sheet_split1(self):
        """
        test checking if image can be split properly.
        """
        sheet = self.sprite_sheet_2x2.convert("RGBA")
        sprite_size = (50,50)
        padding = (0,0)

        split_images = sprite_sheet_splitter.split_sprite_sheet(sheet, sprite_size, padding)
        self.assertEqual(len(split_images), 4, msg="sprite_sheet_split.test_sprite_sheet_split1 (Did not result in four images.)")
        self.assertTrue(sprite_size == split_images[0].size, msg="sprite_sheet_split.test_sprite_sheet_split1 (Image size does not match requirement.)")

        for i in range(4):
            self.assertTrue(
                images_are_equal(
                    split_images[i].convert("RGBA"),
                    self.sprites[i].convert("RGBA")
                ),
            msg="sprite_sheet_split.test_sprite_sheet_split1 (Images are not equal.)"
            )

    def test_sprite_sheet_split2(self):
        """
        test checking if image can be split properly. Similar to the first, but with padding.
        """
        sheet = self.sprite_sheet_2x2_padded.convert("RGBA")
        sprite_size = (50,50)
        padding = (20, 20)

        split_images = sprite_sheet_splitter.split_sprite_sheet(sheet, sprite_size, padding)
        self.assertEqual(len(split_images), 4, msg="sprite_sheet_split.test_sprite_sheet_split2 (Did not result in four images.)")
        self.assertTrue(sprite_size == split_images[0].size, msg="sprite_sheet_split.test_sprite_sheet_split2 (Image size mismatch.)")

        for i in range(4):
            self.assertTrue(
                images_are_equal(
                    split_images[i].convert("RGBA"),
                    self.sprites[i].convert("RGBA")
                ),
            msg="sprite_sheet_split.test_sprite_sheet_split2 (Images are not equal.)"
            )


    def test_sprite_sheet_split3(self):
        """
        test checking if image can be split properly. This time with a 4x1 sprite sheet.
        """
        sheet = self.sprite_sheet_4x1.convert("RGBA")
        sprite_size = (50,50)
        padding = (0,0)

        split_images = sprite_sheet_splitter.split_sprite_sheet(sheet, sprite_size, padding)
        self.assertEqual(len(split_images), 4, msg="sprite_sheet_split.test_sprite_sheet_split3 (Did not result in four images.)")
        self.assertTrue(sprite_size == split_images[0].size, msg="sprite_sheet_split.test_sprite_sheet_split3 (Image size does not match requirement.)")

        for i in range(4):
            self.assertTrue(
                images_are_equal(
                    split_images[i].convert("RGBA"),
                    self.sprites[i].convert("RGBA")
                ),
            msg="sprite_sheet_split.test_sprite_sheet_split3 (Images are not equal.)"
            )

    def test_sprite_sheet_split4(self):
        """
        test checking if image can be split properly. This time with a 4x1 sprite sheet, but with padding.
        """
        sheet = self.sprite_sheet_4x1_padded.convert("RGBA")
        sprite_size = (50,50)
        padding = (10,10)

        split_images = sprite_sheet_splitter.split_sprite_sheet(sheet, sprite_size, padding)
        self.assertEqual(len(split_images), 4, msg="sprite_sheet_split.test_sprite_sheet_split4 (Did not result in four images.)")
        self.assertTrue(sprite_size == split_images[0].size, msg="sprite_sheet_split.test_sprite_sheet_split4 (Image size does not match requirement.)")

        for i in range(4):
            self.assertTrue(
                images_are_equal(
                    split_images[i].convert("RGBA"),
                    self.sprites[i].convert("RGBA")
                ),
            msg="sprite_sheet_split.test_sprite_sheet_split4 (Images are not equal.)"
            )

    def test_sprite_sheet_split5(self):
        """
        test checking if image can be split properly. This time with a 1x4 sprite sheet.
        """
        sheet = self.sprite_sheet_4x1.transpose(Transpose.TRANSPOSE).convert("RGBA")
        sprite_size = (50,50)
        padding = (0,0)

        split_images = sprite_sheet_splitter.split_sprite_sheet(sheet, sprite_size, padding)
        self.assertEqual(len(split_images), 4, msg="sprite_sheet_split.test_sprite_sheet_split5 (Did not result in four images.)")
        self.assertTrue(sprite_size == split_images[0].size, msg="sprite_sheet_split.test_sprite_sheet_split5 (Image size does not match requirement.)")

        for i in range(4):
            self.assertTrue(
                images_are_equal(
                    split_images[i].convert("RGBA"),
                    self.sprites[i].convert("RGBA")
                ),
            msg="sprite_sheet_split.test_sprite_sheet_split5 (Images are not equal.)"
            )

    def test_sprite_sheet_split6(self):
        """
        test checking if image can be split properly. This time with a 1x4 sprite sheet, but with padding.
        """
        sheet = self.sprite_sheet_4x1_padded.transpose(Transpose.TRANSPOSE).convert("RGBA")
        sprite_size = (50,50)
        padding = (10,10)

        split_images = sprite_sheet_splitter.split_sprite_sheet(sheet, sprite_size, padding)
        self.assertEqual(len(split_images), 4, msg="sprite_sheet_split.test_sprite_sheet_split6 (Did not result in four images.)")
        self.assertTrue(sprite_size == split_images[0].size, msg="sprite_sheet_split.test_sprite_sheet_split6 (Image size does not match requirement.)")

        for i in range(4):
            self.assertTrue(
                images_are_equal(
                    split_images[i].convert("RGBA"),
                    self.sprites[i].convert("RGBA")
                ),
            msg="sprite_sheet_split.test_sprite_sheet_split6 (Images are not equal.)"
            )