import unittest

from ATK.Story_Element import ATK_Story_Element
from test.ATK.lib.testing.ATK_Test_Case import ATK_Test_Case


class TestStory_Element(ATK_Test_Case):
    def setUp(self):
        self.test_obj = ATK_Story_Element(transcript='Test', slide=1, file_path='/dev/null', is_cached=False)

    def test_creation(self):
        self.assertIsInstance(self.test_obj, ATK_Story_Element)

    def test_members(self):
        must_have_members = ['file_path', 'is_cached', 'slide', 'transcript']
        actual_members = list(filter(lambda x: x[0] != '_', dir(self.test_obj)))
        self.assertTrue(all(mhm in actual_members for mhm in must_have_members))


if __name__ == '__main__':
    unittest.main()

