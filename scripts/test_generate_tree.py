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


class Dates(unittest.TestCase):

    LOG = ("\x001700000000\n\nb/new.bin\na.txt\n"
           "\x001600000000\n\nb/new.bin\nb/c/old.bin\n")

    def test_parse_log_keeps_the_newest_commit_per_file(self):
        """git log lists newest first; a file's first sighting is its last change."""
        self.assertEqual(gt.parse_log(self.LOG),
                         {"b/new.bin": 1700000000, "a.txt": 1700000000,
                          "b/c/old.bin": 1600000000})

    def test_format_date_is_zurich_local_time(self):
        self.assertEqual(gt.format_date(1700000000), "2023-11-14 23:13")

    def test_files_carry_their_date(self):
        out = gt.build_index([("a.txt", 1)], "main", {"a.txt": 1700000000})
        self.assertEqual(out["tree"], [{"path": "a.txt", "size": 1, "date": "2023-11-14 23:13"}])

    def test_file_without_a_date_has_no_date_key(self):
        out = gt.build_index([("a.txt", 1)], "main", {})
        self.assertEqual(out["tree"], [{"path": "a.txt", "size": 1}])

    def test_folders_take_their_newest_file_date(self):
        out = gt.build_index([("b/new.bin", 1), ("b/c/old.bin", 2)], "main",
                             {"b/new.bin": 1700000000, "b/c/old.bin": 1600000000})
        self.assertEqual(out["folders"], {"b": {"date": "2023-11-14 23:13"},
                                          "b/c": {"date": "2020-09-13 14:26"}})

    def test_without_dates_there_is_no_folders_key(self):
        self.assertNotIn("folders", gt.build_index([("a.txt", 1)], "main"))


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
