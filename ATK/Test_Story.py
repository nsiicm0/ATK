import unittest
from ATK.Story import ATK_Story_Element, ATK_Story
from ATK.lib.testing.ATK_Test_Case import ATK_Test_Case


class Test_Story_Element(ATK_Test_Case):
    def setUp(self) -> None:
        self.test_obj = ATK_Story_Element(transcript='Test', slide=1, file_path='/dev/null', is_cached=False)

    def test_creation(self) -> None:
        self.assertIsInstance(self.test_obj, ATK_Story_Element)

    def test_members(self) -> None:
        must_have_members = ['file_path', 'is_cached', 'slide', 'transcript']
        actual_members = list(filter(lambda x: x[0] != '_', dir(self.test_obj)))
        self.assertTrue(all(mhm in actual_members for mhm in must_have_members))

class Test_Story(ATK_Test_Case):
    def setUp(self) -> None:
        self.test_obj = ATK_Story()
        self.test_element1 = ATK_Story_Element(transcript='Test 1', slide=1, file_path='/dev/null', is_cached=False)
        self.test_element2 = ATK_Story_Element(transcript='Test 2', slide=2, file_path='/dev/null', is_cached=False)
        self.test_element3 = ATK_Story_Element(transcript='Test 3', slide=3, file_path='/dev/null', is_cached=False)

    def test_creation(self) -> None:
        self.assertIsInstance(self.test_obj, ATK_Story)

    def test_adding(self) -> None:
        self.test_obj.add_line(self.test_element1)
        self.assertTrue(len(self.test_obj.get_lines()) == 1)
        self.assertIn(self.test_element1, self.test_obj.get_lines())
        self.test_obj.add_lines([self.test_element2, self.test_element3])
        self.assertTrue(len(self.test_obj.get_lines()) == 3)
        self.assertIn(self.test_element2, self.test_obj.get_lines())
        self.assertIn(self.test_element3, self.test_obj.get_lines())

if __name__ == '__main__':
    unittest.main()
