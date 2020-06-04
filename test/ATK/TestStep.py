import unittest
from ATK.Step import ATK_Step
from test.ATK.lib.Stub_Class import Stub_Class
from test.ATK.lib.testing.ATK_Test_Case import ATK_Test_Case



class TestStep(ATK_Test_Case):

    def setUp(self):
        config = dict({
            'name': 'lowercase text',
            'start': 0,
            'end': 9
        })
        self.test_obj1 = ATK_Step(name='Get Upper', obj=Stub_Class(), calls=['to_upper'], args=[config], prereqs=[])
        self.test_obj2 = ATK_Step(name='Get Part', obj=Stub_Class(), calls=['part'], args=[config], prereqs=[])

    def test_creation(self):
        self.assertIsInstance(self.test_obj1, ATK_Step)
        self.assertIsInstance(self.test_obj2, ATK_Step)
        self.assertNotEqual(self.test_obj1, self.test_obj2)

    def test_members(self):
        must_have_members = ['args', 'calls', 'completed', 'name', 'obj', 'prereqs']
        actual_members = list(filter(lambda x: x[0] != '_', dir(self.test_obj1)))
        self.assertTrue(all(mhm in actual_members for mhm in must_have_members))

if __name__ == '__main__':
    unittest.main()

