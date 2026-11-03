import unittest

from library.union_find import UnionFind


class UnionFindTests(unittest.TestCase):
    def test_union_and_connectivity(self):
        uf = UnionFind(5)

        self.assertTrue(uf.union(0, 1))
        self.assertTrue(uf.union(1, 2))
        self.assertTrue(uf.same(0, 2))
        self.assertFalse(uf.same(0, 3))
        self.assertFalse(uf.union(0, 2))

    def test_component_size_after_unions(self):
        uf = UnionFind(4)
        uf.union(0, 1)
        uf.union(2, 3)
        uf.union(1, 3)

        self.assertEqual(uf.size(0), 4)
        self.assertEqual(uf.size(2), 4)
        self.assertEqual(uf.size(1), 4)

    def test_singleton_size(self):
        self.assertEqual(UnionFind(1).size(0), 1)


if __name__ == "__main__":
    unittest.main()
