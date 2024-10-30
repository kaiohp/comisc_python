import hashlib
import os
import shutil
from pathlib import Path


def hash_file(path: Path):
    BLOCKSIZE = 65536

    hasher = hashlib.sha1()
    with path.open('rb') as file:
        buf = file.read(BLOCKSIZE)
        while buf:
            hasher.update(buf)
            buf = file.read(BLOCKSIZE)
    return hasher.hexdigest()


def read_paths_and_hashes(path):
    hashes = {}
    for folder, _, files in os.walk(path):
        for file in files:
            file_path = Path(folder) / file
            file_hash = hash_file(file_path)
            hashes[file_hash] = file
    return hashes


def determine_actions(
    source_hashes: dict,
    destinations_hashes: dict,
    source: str,
    destination: str,
):
    for sha, filename in source_hashes.items():
        if sha not in destinations_hashes:
            source_path = Path(source) / filename
            destination_path = Path(destination) / filename

            yield 'COPY', source_path, destination_path

        elif destinations_hashes[sha] != filename:
            old_path = Path(destination) / destinations_hashes[sha]
            new_path = Path(destination) / filename

            yield 'MOVE', old_path, new_path

    for sha, filename in destinations_hashes.items():
        if sha not in source_hashes:
            path = Path(destination) / filename
            yield 'DELETE', path


class FileSystem:
    @classmethod
    def read(cls, root_path):
        return read_paths_and_hashes(root_path)

    @classmethod
    def copy(cls, source_path, destination_path):
        shutil.copy(source_path, destination_path)

    @classmethod
    def move(cls, old_path, new_path):
        shutil.move(old_path, new_path)

    @classmethod
    def delete(cls, file_path):
        os.remove(file_path)


def sync(source: str, destination: str, filesystem=FileSystem()):
    source_hashes = filesystem.read(source)
    destinations_hashes = filesystem.read(destination)

    actions = determine_actions(
        source_hashes, destinations_hashes, source, destination
    )

    for action in actions:
        match action:
            case ('COPY', src, dst):
                filesystem.copy(src, dst)
            case ('MOVE', old, new):
                filesystem.move(old, new)
            case ('DELETE', path):
                filesystem.delete(path)
