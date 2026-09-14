#!/usr/bin/env python3
"""Tests for generate-tree.py. Run with: python3 -m unittest discover scripts"""

import importlib.util
import pathlib
import unittest


def _load():
    path = pathlib.Path(__file__).with_name("generate-tree.py")
    spec = importlib.util.spec_from_file_location("generate_tree", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gt = _load()


class BuildIndex(unittest.TestCase):

    def test_shape_is_branch_plus_tree(self):
        out = gt.build_index([("README.md", 10)], "main")
        self.assertEqual(out, {"branch": "main",
                               "tree": [{"path": "README.md", "size": 10}]})

    def test_entries_are_sorted_by_path(self):
        out = gt.build_index([("z.txt", 1), ("a/b.txt", 2), ("README.md", 3)], "main")
        self.assertEqual([e["path"] for e in out["tree"]],
                         ["README.md", "a/b.txt", "z.txt"])

    def test_the_output_file_excludes_itself(self):
        """Including it would change its own size on every run, so CI would
        commit a new tree.json forever."""
        out = gt.build_index([("tree.json", 999), ("README.md", 10)], "main")
        self.assertEqual([e["path"] for e in out["tree"]], ["README.md"])

    def test_sizes_are_preserved(self):
        out = gt.build_index([("big.bin", 1370864)], "main")
        self.assertEqual(out["tree"][0]["size"], 1370864)

    def test_empty_input(self):
        self.assertEqual(gt.build_index([], "main"), {"branch": "main", "tree": []})

    def test_branch_is_carried_through(self):
        self.assertEqual(gt.build_index([], "gh-pages")["branch"], "gh-pages")

    def test_is_deterministic(self):
        entries = [("b.txt", 1), ("a.txt", 2)]
        self.assertEqual(gt.build_index(entries, "main"), gt.build_index(entries, "main"))


class Serialisation(unittest.TestCase):

    def test_render_ends_with_one_newline(self):
        text = gt.render(gt.build_index([("a.txt", 1)], "main"))
        self.assertTrue(text.endswith("\n"))
        self.assertFalse(text.endswith("\n\n"))

    def test_render_is_stable_across_calls(self):
        index = gt.build_index([("a.txt", 1), ("b.txt", 2)], "main")
        self.assertEqual(gt.render(index), gt.render(index))

    def test_render_round_trips_as_json(self):
        import json
        index = gt.build_index([("a/b.txt", 7)], "main")
        self.assertEqual(json.loads(gt.render(index)), index)


if __name__ == "__main__":
    unittest.main()
