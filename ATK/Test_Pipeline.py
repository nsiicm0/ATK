import unittest
from ATK.Pipeline import ATK_Step, ATK_Pipeline, ATK_Pipeline_Dependency_Exception
from ATK.lib.testing.ATK_Test_Case import ATK_Test_Case

class Stub_Class(object):

    def to_upper(self, **kwargs) -> str:
        return kwargs['name'].upper()

    def part(self, **kwargs) -> str:
        return kwargs['name'][kwargs['start']:kwargs['end']]

class Test_Step(ATK_Test_Case):

    def setUp(self) -> None:
        config = dict({
            'name': 'lowercase text',
            'start': 0,
            'end': 9
        })
        self.test_obj1 = ATK_Step(name='Get Upper', obj=Stub_Class(), calls=['to_upper'], args=[config], prereqs=[])
        self.test_obj2 = ATK_Step(name='Get Part', obj=Stub_Class(), calls=['part'], args=[config], prereqs=[])

    def test_creation(self) -> None:
        self.assertIsInstance(self.test_obj1, ATK_Step)
        self.assertIsInstance(self.test_obj2, ATK_Step)
        self.assertNotEqual(self.test_obj1, self.test_obj2)

    def test_members(self) -> None:
        must_have_members = ['args', 'calls', 'completed', 'name', 'obj', 'prereqs']
        actual_members = list(filter(lambda x: x[0] != '_', dir(self.test_obj1)))
        self.assertTrue(all(mhm in actual_members for mhm in must_have_members))

class Test_Pipeline(ATK_Test_Case):

    def setUp(self) -> None:
        config = dict({
            'name': 'lowercase text',
            'start': 0,
            'end': 9
        })
        self.test_obj = ATK_Pipeline()
        self.test_element1 = ATK_Step(name='Get Upper', obj=Stub_Class(), calls=['to_upper'], args=[config], prereqs=[])
        self.test_element2 = ATK_Step(name='Get Part', obj=Stub_Class(), calls=['part'], args=[config], prereqs=['Get Upper'])

    def test_creation(self) -> None:
        self.assertIsInstance(self.test_obj, ATK_Pipeline)

    def test_add_single(self) -> None:
        self.test_obj.add_step(self.test_element1)
        self.assertTrue(len(self.test_obj.execution_steps) == 1)

    def test_add_multiple(self) -> None:
        self.test_obj.add_multiple_steps([self.test_element1, self.test_element2])
        self.assertTrue(len(self.test_obj.execution_steps) == 2)

    def test_prereqs_pass(self) -> None:
        self.test_obj.add_multiple_steps([self.test_element1, self.test_element2])
        with self.assertNotRaises(ATK_Pipeline_Dependency_Exception):
            self.test_obj.run()

    def test_prereqs_fail(self) -> None:
        self.test_obj.add_multiple_steps([self.test_element2, self.test_element1])
        with self.assertRaises(ATK_Pipeline_Dependency_Exception):
            self.test_obj.run()

if __name__ == '__main__':
    unittest.main()
