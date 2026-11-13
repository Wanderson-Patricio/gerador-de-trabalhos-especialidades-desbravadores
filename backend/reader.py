from enum import StrEnum
import json
import yaml
from pathlib import Path
from typing import Literal, Union
from abc import ABC, abstractmethod

class Reader(ABC):
    def __init__(self, file_path: Union[str, Path]) -> None:
        self.file_path: Union[str, Path] = file_path
        self.extension = Path(file_path).suffix

    @abstractmethod
    def read(self) -> dict:
        pass

    @abstractmethod
    def append(self, key: str, data: dict) -> None:
        pass

    @abstractmethod
    def update(self, key: str, data: dict, **identifiers) -> None:
        pass

    @abstractmethod
    def remove(self, key: str, **identifiers) -> None:
        pass



class JSONReader(Reader):
    def read(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as self.file:
            return json.load(self.file)

    def append(self, key: str, data: dict) -> None:
        current_data = self.read()
        data_list = current_data.get(key, [])
        data_list.append(data)
        current_data[key] = data_list
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)


    def update(self, key: str, data: dict, **identifiers) -> None:
        current_data = self.read()
        data_list = current_data.get(key, [])
        for i, item in enumerate(data_list):
            if all(item.get(k) == v for k, v in identifiers.items()):
                data_list[i] = data
                break
        current_data[key] = data_list
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)


    def remove(self, key: str, **identifiers) -> None:
        current_data = self.read()
        data_list = current_data.get(key, [])
        for i, item in enumerate(data_list):
            if all(item.get(k) == v for k, v in identifiers.items()):
                del data_list[i]
                break
        current_data[key] = data_list
        with open(self.file_path, 'w', encoding='utf-8') as f:
            json.dump(current_data, f, ensure_ascii=False, indent=4)


class YAMLReader(Reader):
    def read(self) -> dict:
        with open(self.file_path, 'r', encoding='utf-8') as self.file:
            return yaml.safe_load(self.file)

    def append(self, key: str, data: dict) -> None:
        current_data = self.read() or {}
        data_list = current_data.get(key, [])
        data_list.append(data)
        current_data[key] = data_list
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(current_data, f, allow_unicode=True)

    def update(self, key: str, data: dict, **identifiers) -> None:
        current_data = self.read() or {}
        data_list = current_data.get(key, [])
        for i, item in enumerate(data_list):
            if all(item.get(k) == v for k, v in identifiers.items()):
                data_list[i] = data
                break
        current_data[key] = data_list
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(current_data, f, allow_unicode=True)

    def remove(self, key: str, **identifiers) -> None:
        current_data = self.read() or {}
        data_list = current_data.get(key, [])
        for i, item in enumerate(data_list):
            if all(item.get(k) == v for k, v in identifiers.items()):
                del data_list[i]
                break
        current_data[key] = data_list
        with open(self.file_path, 'w', encoding='utf-8') as f:
            yaml.safe_dump(current_data, f, allow_unicode=True)





class FileType(StrEnum):
    JSON = "json"
    YAML = "yaml"

reader_by_file_type = {
    FileType.JSON: JSONReader,
    FileType.YAML: YAMLReader
}