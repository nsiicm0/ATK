import unittest
from ATK.Story import Story
from ATK.StoryElement import StoryElement
from test.ATK.lib.testing.ATK_Test_Case import ATK_Test_Case


class TestStory(ATK_Test_Case):
    def setUp(self):
        self.test_obj = Story()
        self.test_element1 = StoryElement(transcript='Test 1', slide=1, next_slide=2, file_path='/dev/null', is_cached=False)
        self.test_element2 = StoryElement(transcript='Test 2', slide=2, next_slide=3, file_path='/dev/null', is_cached=False)
        self.test_element3 = StoryElement(transcript='Test 3', slide=3, next_slide=-1, file_path='/dev/null', is_cached=False)

    def test_creation(self):
        self.assertIsInstance(self.test_obj, Story)

    def test_adding(self):
        self.test_obj.add_line(self.test_element1)
        self.assertTrue(len(self.test_obj.get_lines()) == 1)
        self.assertIn(self.test_element1, self.test_obj.get_lines())
        self.test_obj.add_lines([self.test_element2, self.test_element3])
        self.assertTrue(len(self.test_obj.get_lines()) == 3)
        self.assertIn(self.test_element2, self.test_obj.get_lines())
        self.assertIn(self.test_element3, self.test_obj.get_lines())

    def test_tell(self):
        self.test_obj.add_lines([self.test_element1, self.test_element2, self.test_element3])
        slide_story = self.test_obj.tell_slide(2)
        self.assertEqual(len(slide_story), 1)
        self.assertEqual(slide_story[0], self.test_element2)

if __name__ == '__main__':
    unittest.main()
