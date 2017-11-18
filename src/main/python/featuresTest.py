import unittest
import features

class TestFeatures(unittest.TestCase):

    def test_no_patch(self):
        self.assertEqual(features.decrement_patch_versions('//app/main/foo.java#2'), '//app/main/foo.java#2')

    def test_patch(self):
        self.assertEqual(features.decrement_patch_versions('//app/210/patch/foo.java#2'), '//app/210/patch/foo.java#1')

    def test_multiple_digits(self):
        self.assertEqual(features.decrement_patch_versions('//app/210/patch/foo.java#11'), '//app/210/patch/foo.java#10')

if __name__ == '__main__':
    unittest.main()

