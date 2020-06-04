import unittest

from ATK.StoryElement import StoryElement
from test.ATK.lib.testing.ATK_Test_Case import ATK_Test_Case


class TestStoryElement(ATK_Test_Case):
    def setUp(self):
        self.test_obj = StoryElement(transcript='Test', slide=1, file_path='/dev/null', is_cached=False)

    def test_creation(self):
        self.assertIsInstance(self.test_obj, StoryElement)

    def test_members(self):
        must_have_members = ['file_path', 'is_cached', 'slide', 'transcript', 'next_slide']
        actual_members = list(filter(lambda x: x[0] != '_', dir(self.test_obj)))
        self.assertTrue(all(mhm in actual_members for mhm in must_have_members))


if __name__ == '__main__':
    unittest.main()

