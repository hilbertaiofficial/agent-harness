from pathlib import Path

from hilbert_harness.taxonomy import load_taxonomy


def test_haf_taxonomy_loads():
    taxonomy = load_taxonomy(Path(__file__).parents[1] / "taxonomy" / "haf-v0.1.json")

    assert taxonomy["version"] == "0.1"
    assert len(taxonomy["categories"]) == 11
    assert taxonomy["categories"][0]["id"] == "HAF-01"

