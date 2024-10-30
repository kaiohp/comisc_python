import shutil
import tempfile
from pathlib import Path

from fake_file_system import FakeFileSystem
from sync import determine_actions, sync


def test_when_a_file_exists_in_the_source_but_not_the_destination():
    try:
        source = tempfile.mkdtemp()
        destination = tempfile.mkdtemp()

        content = 'I am a very useful file'
        file_path = Path(source) / 'my_file.txt'
        file_path.write_text(content)

        sync(source, destination)

        expected_path = Path(destination) / 'my_file.txt'

        assert expected_path.exists()
        assert expected_path.read_text() == content

    finally:
        shutil.rmtree(source)
        shutil.rmtree(destination)


def test_when_a_file_has_been_renamed_in_the_source():
    try:
        source = tempfile.mkdtemp()
        destination = tempfile.mkdtemp()

        content = 'I am a very useful file'

        file_on_source = Path(source) / 'my_file_final.txt'
        file_on_source.write_text(content)

        file_on_destination = Path(destination) / 'my_file.txt'
        file_on_destination.write_text(content)

        sync(source, destination)

        expected_path = Path(destination) / 'my_file_final.txt'

        assert expected_path.exists()
        assert expected_path.read_text() == content
        assert file_on_destination.exists() is False

    finally:
        shutil.rmtree(source)
        shutil.rmtree(destination)


def test_when_a_file_exists_in_the_source_but_not_the_destination_with_abstraction():
    source_hashes = {'hash': 'file.txt'}
    destinations_hashes = {}
    expected_actions = [('COPY', Path('/src/file.txt'), Path('/dst/file.txt'))]
    actions = determine_actions(
        source_hashes, destinations_hashes, '/src', '/dst'
    )

    assert list(actions) == expected_actions


def test_when_a_file_has_been_renamed_in_the_source_with_abstraction():
    source_hashes = {'hash': 'file.txt'}
    destinations_hashes = {'hash': 'file_1.txt'}
    expected_actions = [
        ('MOVE', Path('/dst/file_1.txt'), Path('/dst/file.txt'))
    ]
    actions = determine_actions(
        source_hashes, destinations_hashes, '/src', '/dst'
    )

    assert list(actions) == expected_actions


def test_when_a_file_exists_in_the_source_but_not_the_destination_with_fake_file_system():
    fake_path_hashes = {'/src': {'hash': 'file.txt'}, '/dst': {}}
    fake_file_system = FakeFileSystem(fake_path_hashes)

    sync('/src', '/dst', fake_file_system)

    expected_actions = [('COPY', Path('/src/file.txt'), Path('/dst/file.txt'))]

    assert fake_file_system.actions == expected_actions


def test_when_a_file_has_been_renamed_in_the_source_with_fake_file_system():
    fake_path_hashes = {
        '/src': {'hash': 'file.txt'},
        '/dst': {'hash': 'file_1.txt'},
    }
    fake_file_system = FakeFileSystem(fake_path_hashes)

    sync('/src', '/dst', fake_file_system)

    expected_actions = [
        ('MOVE', Path('/dst/file_1.txt'), Path('/dst/file.txt'))
    ]

    assert fake_file_system.actions == expected_actions
