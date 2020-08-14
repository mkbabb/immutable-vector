import unittest
from typing import *

from immutable_vector import WIDTH, Node, Vector


class TestVector(unittest.TestCase):
    def append_pop(self, n: int) -> None:
        v0 = Vector[int]([i for i in range(n)])
        v1 = v0.copy()

        for i in range(n):
            v1 = v1.pop()
            s = v1.join()
            count = v1.reduce(lambda acc, curr_val, i: acc + 1, 0)
            self.assertEqual(count, n - (i + 1))

    def test_append_pop(self) -> None:
        self.append_pop(WIDTH ** 2)
        self.append_pop(WIDTH ** 2 + 1)
        self.append_pop(WIDTH ** 2 - 1)

        self.append_pop(0)
        self.append_pop(1)


if __name__ == "__main__":
    unittest.main()
