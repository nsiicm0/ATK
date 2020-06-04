import unittest
from ATK.StoryDeveloper import StoryDeveloper
from test.ATK.lib.testing.ATK_Test_Case import ATK_Test_Case


class TestStoryDeveloper(ATK_Test_Case):
    def setUp(self):
        self.test_obj = StoryDeveloper()

    def test_develop(self):
        self.test_obj.start()
        self.test_obj.subtitle(topic='#Test')
        for i in range(10):
            self.test_obj.content(f'This is demo content #{str(i)}')
        self.test_obj.end()
        self.assertEqual(self.test_obj.slide_counter, 13)
        story = self.test_obj.story
        lines = story.get_lines()
        self.assertEqual(len(lines), 13)
        second_line = lines[1]
        self.assertIn('#Test', map(lambda x: x.replace('.', ''), second_line.transcript.split(' ')))

if __name__ == '__main__':
    unittest.main()
