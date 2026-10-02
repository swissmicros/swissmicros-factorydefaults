#!/usr/bin/env python3
"""Tests for generate-manifest.py. Run with: python3 -m unittest discover scripts"""

import importlib.util
import pathlib
import tempfile
import unittest


def _load():
    path = pathlib.Path(__file__).with_name("generate-manifest.py")
    spec = importlib.util.spec_from_file_location("generate_manifest", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


gm = _load()


def _repo(files):
    """A temporary repo root holding empty files at the given relative paths."""
    tmp = tempfile.TemporaryDirectory()
    root = pathlib.Path(tmp.name)
    for rel in files:
        p = root / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_bytes(b"")
    return tmp


class BuildManifest(unittest.TestCase):

    def _pioneer(self, files):
        with _repo(files) as root:
            return {m["name"]: m for m in gm.build_manifest(root)["pioneer"]}

    def test_qspi_models_are_flagged(self):
        models = self._pioneer([
            "Pioneer_Models/DM32/a.bin",
            "Pioneer_Models/DM42/a.bin",
            "Pioneer_Models/DM42n/a.bin",
        ])
        for name in ("DM32", "DM42", "DM42n"):
            self.assertIs(models[name]["qspi"], True, name)

    def test_other_models_carry_an_explicit_false(self):
        """Every model states the flag, so a reader never has to guess what a
        missing key means."""
        models = self._pioneer([
            "Pioneer_Models/DM41X/a.bin",
            "Pioneer_Models/DM41Xn/a.bin",
            "Pioneer_Models/R47/a.bin",
        ])
        for name in ("DM41X", "DM41Xn", "R47"):
            self.assertIs(models[name]["qspi"], False, name)

    def test_loose_qspi_image_is_not_a_model(self):
        models = self._pioneer([
            "Pioneer_Models/DM42/a.bin",
            "Pioneer_Models/DM42_qspi_3.x.bin",
        ])
        self.assertEqual(list(models), ["DM42"])

    def test_model_entry_keeps_name_and_files(self):
        models = self._pioneer(["Pioneer_Models/DM42/a.bin"])
        self.assertEqual(models["DM42"]["files"], ["Pioneer_Models/DM42/a.bin"])


class CommittedManifest(unittest.TestCase):

    def test_every_pioneer_model_in_models_json_has_a_boolean_qspi_flag(self):
        import json
        path = pathlib.Path(__file__).resolve().parent.parent / "models.json"
        manifest = json.loads(path.read_text())
        for model in manifest["pioneer"]:
            self.assertIsInstance(model.get("qspi"), bool, model["name"])


if __name__ == "__main__":
    unittest.main()
