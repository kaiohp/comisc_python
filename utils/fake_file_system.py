from pathlib import Path


class FakeFileSystem:
    def __init__(self, path_hashes):
        self.path_hashes = path_hashes
        self.actions = []

    def read(self, path):
        return self.path_hashes[path]

    def copy(self, source_path, destination_path):
        self.actions.append(
            ('COPY', Path(source_path), Path(destination_path))
        )

    def move(self, old_path, new_path):
        self.actions.append(('MOVE', Path(old_path), Path(new_path)))

    def delete(self, file_path):
        self.actions.append(('DELETE', Path(file_path)))
