from immutable_vector import Vector, WIDTH, Node
from typing import *


import unittest


class TestVector(unittest.TestCase):
    def test_append_case_1(self) -> None:
        v0 = Vector[int]([i for i in range(WIDTH)])
        v1 = v0.append(WIDTH)

        self.assertTrue(v1.length == WIDTH + 1)
        # self.assertTrue(isinstance(v1.root.children[0], Node))
        # self.assertTrue(v1.root.children[1][0] == WIDTH)

    def test_append_case_2(self) -> None:
        v0 = Vector[int]([i for i in range(WIDTH * WIDTH)])
        v1 = v0.append(WIDTH * WIDTH + 1)

        self.assertTrue(v1.length == WIDTH * WIDTH + 1)
        # self.assertTrue(isinstance(v1.root.children[0][0], Node))

    def test_append_case_3(self) -> None:
        v0 = Vector[int]([])
        v1 = v0.copy()

        v1.mutate()
        for i in range(WIDTH):
            v1.append(i)
            self.assertFalse(v0.root == v1.root)
            self.assertTrue(v1.root.children[i] == i)

        self.assertTrue(v1.length == WIDTH)


if __name__ == "__main__":
    # unittest.main()
    n = WIDTH ** 2
    v0 = Vector[int]([i for i in range(n)])
    v1 = v0.copy()

    for i in range(n):
        v1 = v1.pop()

