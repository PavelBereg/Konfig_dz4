import unittest
from assem_inter import Assembler, Interpretator

class TestAssemblerInterpreter(unittest.TestCase):
    def setUp(self):
        self.memory_range = 1024
        self.assembler = Assembler(self.memory_range)
        self.interpreter = Interpretator(self.memory_range)

    def test_load_constant(self):
        source_code = "LOAD_CONSTANT 42 10"
        machine_code, log = self.assembler.assemble(source_code)
        self.interpreter.execute(machine_code)
        self.assertEqual(self.interpreter.registers[10], 42)
        self.assertEqual(self.interpreter.memory[10], 42)

    def test_load_memory(self):
        source_code = """
        LOAD_CONSTANT 42 10
        LOAD_MEMORY 1 10
        """
        machine_code, log = self.assembler.assemble(source_code)
        self.interpreter.execute(machine_code)
        self.assertEqual(self.interpreter.registers[1], 42)

    def test_store_to_memory(self):
        source_code = """
        LOAD_CONSTANT 42 10
        STORE_TO_MEMORY 10 20
        """
        machine_code, log = self.assembler.assemble(source_code)
        self.interpreter.execute(machine_code)
        self.assertEqual(self.interpreter.memory[20], 42)

    def test_sqrt(self):
        source_code = """
        LOAD_CONSTANT 16 10
        SQRT 10 20
        """
        machine_code, log = self.assembler.assemble(source_code)
        self.interpreter.execute(machine_code)
        self.assertEqual(self.interpreter.registers[10], 4)
        self.assertEqual(self.interpreter.memory[20], 4)

if __name__ == "__main__":
    unittest.main()
