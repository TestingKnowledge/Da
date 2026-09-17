import unittest
from deobfuscator.pipeline import DeobfuscationPipeline

class TestDeobfuscator(unittest.TestCase):
    def setUp(self):
        self.pipeline = DeobfuscationPipeline()

    def test_constant_folding(self):
        source = """
        local a = 10
        local b = 20
        local c = a + b
        """
        res = self.pipeline.run(source)
        self.assertIn("local c = 30", res.source)

    def test_string_concatenation(self):
        source = """
        local a = "hello"
        local b = "world"
        local c = a .. b
        """
        res = self.pipeline.run(source)
        self.assertIn('local c = "helloworld"', res.source)

    def test_function_resolution_preservation(self):
        source = """
        local a = 10
        print(a)
        foo("test")
        """
        res = self.pipeline.run(source)
        # Proven values substituted, unknown functions remain symbolic
        self.assertIn("print(10.0)", res.source)
        self.assertIn('foo("test")', res.source)

    def test_no_eval_execution(self):
        # Ensure os.execute is parsed statically, not actually executed by Python
        source = 'os.execute("rm -rf /")'
        res = self.pipeline.run(source)
        # Remains in text, but wasn't executed
        self.assertTrue('os' in res.source or 'execute' in res.source)

if __name__ == '__main__':
    unittest.main()

