from os import path
from datetime import datetime
from ..getFilePath import getProgramFilePath


class ProgramFileRepository:
    def _generate_file_path(self, file):
        unique_filename = file.filename.replace("/", "_").replace(" ", "_")
        unique_filename = unique_filename + datetime.now().strftime("%d%m%Y_%H%M%S")
        return unique_filename

    def create(self, file) -> str:
        unique_filename = self._generate_file_path(unique_filename)

        file.save(path.join("static", "custom_programs", unique_filename))
        return unique_filename

    def update(self, file, old_unique_filename) -> str:
        source_file_path = getProgramFilePath(old_unique_filename)
        file.save(source_file_path)
        return source_file_path
