import unittest

from test.ATK import (
    TestStep,
    TestPipeline,
    TestStory_Element,
    TestStory
)

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(TestStep))
suite.addTests(loader.loadTestsFromModule(TestPipeline))
suite.addTests(loader.loadTestsFromModule(TestStory_Element))
suite.addTests(loader.loadTestsFromModule(TestStory))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)