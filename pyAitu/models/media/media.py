from pyAitu.models.constants.file_type import FileType
from pyAitu.utils.strings import FILE_ID, FILE_TYPE, NAME


class Media:
    def __init__(self, file_id, name, file_type: FileType):
        self._file_id = file_id
        self._name = name
        self._file_type = file_type

    def to_dict(self):
        return {
            FILE_ID: self._file_id,
            NAME: self._name,
            FILE_TYPE: self._file_type
        }
