import unittest

from test.ATK import (
    TestStep,
    TestPipeline,
    TestStoryElement,
    TestStory,
    TestStoryDeveloper
)

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(TestStep))
suite.addTests(loader.loadTestsFromModule(TestPipeline))
suite.addTests(loader.loadTestsFromModule(TestStoryElement))
suite.addTests(loader.loadTestsFromModule(TestStory))
suite.addTests(loader.loadTestsFromModule(TestStoryDeveloper))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)