import unittest

from test_sheet_split import TestSpriteSheetSplitter
from test_sheet_gen import TestSpriteSheetGenerator

def make_suite():
    """
    make a unittest TestSuite object
        Returns
            (unittest.TestSuite)
    """
    suite = unittest.TestSuite()

    suite.addTest(TestSpriteSheetSplitter('test_blank_check1'))
    suite.addTest(TestSpriteSheetSplitter('test_blank_check2'))
    suite.addTest(TestSpriteSheetSplitter('test_sprite_sheet_split1'))
    suite.addTest(TestSpriteSheetSplitter('test_sprite_sheet_split2'))
    suite.addTest(TestSpriteSheetSplitter('test_sprite_sheet_split3'))
    suite.addTest(TestSpriteSheetSplitter('test_sprite_sheet_split4'))
    suite.addTest(TestSpriteSheetSplitter('test_sprite_sheet_split5'))
    suite.addTest(TestSpriteSheetSplitter('test_sprite_sheet_split6'))

    suite.addTest(TestSpriteSheetGenerator('test_sprite_sheet_gen1'))
    suite.addTest(TestSpriteSheetGenerator('test_sprite_sheet_gen2'))
    suite.addTest(TestSpriteSheetGenerator('test_sprite_sheet_gen3'))
    suite.addTest(TestSpriteSheetGenerator('test_sprite_sheet_gen4'))

    return suite

def run_all_tests():
    """
    run all tests in the TestSuite
    """
    runner = unittest.TextTestRunner()
    runner.run(make_suite())

if __name__ == '__main__':
    run_all_tests()
