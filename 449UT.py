import unittest

def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

class TestMathFunctions(unittest.TestCase):
    def test_add_positive(self):
        self.assertEqual(add(2, 3), 5)

    def test_add_negative(self):
        self.assertEqual(add(-2, -3), -5)

    def test_subtract(self):
        self.assertEqual(subtract(10, 5), 5)

if __name__ == '__main__':
    unittest.main()

