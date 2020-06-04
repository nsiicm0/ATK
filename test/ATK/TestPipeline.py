import unittest
from ATK.Step import ATK_Step
from ATK.Pipeline import ATK_Pipeline
from test.ATK.lib.Stub_Class import Stub_Class
from test.ATK.lib.testing.ATK_Test_Case import ATK_Test_Case
from ATK.lib.Exceptions import ATK_Pipeline_Dependency_Exception


class TestPipeline(ATK_Test_Case):

    def setUp(self):
        config = dict({
            'name': 'lowercase text',
            'start': 0,
            'end': 9
        })
        self.test_obj = ATK_Pipeline()
        self.test_element1 = ATK_Step(name='Get Upper', obj=Stub_Class(), calls=['to_upper'], args=[config], prereqs=[])
        self.test_element2 = ATK_Step(name='Get Part', obj=Stub_Class(), calls=['part'], args=[config], prereqs=['Get Upper'])

    def test_creation(self):
        self.assertIsInstance(self.test_obj, ATK_Pipeline)

    def test_add_single(self):
        self.test_obj.add_step(self.test_element1)
        self.assertTrue(len(self.test_obj.execution_steps) == 1)

    def test_add_multiple(self):
        self.test_obj.add_multiple_steps([self.test_element1, self.test_element2])
        self.assertTrue(len(self.test_obj.execution_steps) == 2)

    def test_prereqs_pass(self):
        self.test_obj.add_multiple_steps([self.test_element1, self.test_element2])
        with self.assertNotRaises(ATK_Pipeline_Dependency_Exception):
            self.test_obj.run()

    def test_prereqs_fail(self):
        self.test_obj.add_multiple_steps([self.test_element2, self.test_element1])
        with self.assertRaises(ATK_Pipeline_Dependency_Exception):
            self.test_obj.run()

if __name__ == '__main__':
    unittest.main()
