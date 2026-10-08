from hilbert_harness.observation.filesystem import (
    capture_filesystem_snapshot,
    compare_filesystem_snapshots,
)


def test_modified_file_produces_effect_observation(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("old content")

    before = capture_filesystem_snapshot(tmp_path)

    file_path.write_text("new content")

    after = capture_filesystem_snapshot(tmp_path)

    observations = compare_filesystem_snapshots(
        before,
        after,
        observed_at_step=2,
    )

    assert len(observations) == 1

    observation = observations[0]

    assert observation.operation == "file_write"
    assert observation.resource == "example.txt"
    assert observation.observed_at_step == 2

    assert observation.evidence["source"] == "filesystem_snapshot"
    assert (
        observation.evidence["before_sha256"]
        != observation.evidence["after_sha256"]
    )

def test_unchanged_file_produces_no_effect_observation(tmp_path):
    file_path = tmp_path / "example.txt"
    file_path.write_text("same content")

    before = capture_filesystem_snapshot(tmp_path)

    after = capture_filesystem_snapshot(tmp_path)

    observations = compare_filesystem_snapshots(
        before,
        after,
        observed_at_step=2,
    )

    assert observations == []

def test_created_file_produces_effect_observation(tmp_path):
    before = capture_filesystem_snapshot(tmp_path)

    file_path = tmp_path / "new_file.txt"
    file_path.write_text("new content")

    after = capture_filesystem_snapshot(tmp_path)

    observations = compare_filesystem_snapshots(
        before,
        after,
        observed_at_step=2,
    )

    assert len(observations) == 1

    observation = observations[0]

    assert observation.operation == "file_write"
    assert observation.resource == "new_file.txt"
    assert observation.observed_at_step == 2

    assert observation.evidence["source"] == "filesystem_snapshot"
    assert observation.evidence["before_sha256"] is None
    assert observation.evidence["after_sha256"] == after["new_file.txt"]


def test_deleted_file_produces_effect_observation(tmp_path):
    file_path = tmp_path / "obsolete.txt"
    file_path.write_text("old content")

    before = capture_filesystem_snapshot(tmp_path)

    file_path.unlink()

    after = capture_filesystem_snapshot(tmp_path)

    observations = compare_filesystem_snapshots(
        before,
        after,
        observed_at_step=2,
    )

    assert len(observations) == 1

    observation = observations[0]

    assert observation.operation == "file_delete"
    assert observation.resource == "obsolete.txt"
    assert observation.observed_at_step == 2

    assert observation.evidence["source"] == "filesystem_snapshot"
    assert observation.evidence["before_sha256"] == before["obsolete.txt"]
    assert observation.evidence["after_sha256"] is None