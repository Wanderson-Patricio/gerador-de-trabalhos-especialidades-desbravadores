from .reader import Reader,FileType, reader_by_file_type

import os
from pathlib import Path
from functools import wraps
from typing import Callable, Concatenate, ParamSpec, Protocol, TypeVar
import json
import yaml
from datetime import datetime


class _DataFileOwner(Protocol):
    @property
    def _data_file(self) -> str | Path: ...

    extension: str
    reader: Reader
    def get_latest_version_file(self) -> str: ...
    def get_latest_version(self) -> int: ...


_Service = TypeVar("_Service", bound=_DataFileOwner)
_Params = ParamSpec("_Params")


class Database:
    
    def __init__(self, reader_type: FileType, directory: str | Path | None = None) -> None:
        if directory is None:
            directory = Path(__file__).parent.parent / "data"
        self.directory = str(directory)
        self.extension: FileType = reader_type

    
    def get_latest_version_file(self) -> str:
        latest_version = self.get_latest_version()
        if latest_version == 0:
            latest_version = self.save_new_version()
        return os.path.join(self.directory, f"v{latest_version}", f"especialidades.{self.extension}")

    
    def get_latest_version(self) -> int:
        versions = [f for f in os.listdir(self.directory) if os.path.isdir(os.path.join(self.directory, f)) and f.startswith("v")]
        if not versions:
            return 0
        
        versions.sort(reverse=True)
        return int(versions[0].lstrip("v"))

    
    def get_version_file(self, version: int) -> str:
        filepath = os.path.join(self.directory, f"v{version}", f"especialidades.{self.extension}")
        if not os.path.isfile(filepath):
            raise FileNotFoundError(f"Version file for v{version} not found.")
        return filepath

    
    def save_new_version(self) -> int:
        latest_version = self.get_latest_version()
        new_version = latest_version + 1

        new_dir = os.path.join(self.directory, f"v{new_version}")
        os.makedirs(new_dir, exist_ok=True)
        new_file_path = os.path.join(new_dir, f"especialidades.{self.extension}")
        if new_version == 1:
            data = {"info": {}, "areas": [], "especialidades": []}
        else:
            reader = reader_by_file_type[self.extension]
            reader_instance = reader(self.get_version_file(latest_version))
            data = reader_instance.read()

        data["info"]["version"] = f"v{new_version}"
        data["info"]["created_at"] = datetime.now().isoformat()
        data["info"]["updated_at"] = datetime.now().isoformat()

        with open(new_file_path, "w", encoding="utf-8") as f:
            if self.extension == FileType.JSON:
                json.dump(data, f, ensure_ascii=False, indent=4)
            elif self.extension == FileType.YAML:
                yaml.safe_dump(data, f, allow_unicode=True)
        return new_version


    @staticmethod
    def update_date(
        func: Callable[Concatenate[_Service, _Params], bool],
    ) -> Callable[Concatenate[_Service, _Params], bool]:
        """Update the instance's data file timestamp after a successful operation."""
        @wraps(func)
        
        def wrapper(self: _Service, /, *args: _Params.args, **kwargs: _Params.kwargs) -> bool:
            result = func(self, *args, **kwargs)
            if result:
                reader_instance = reader_by_file_type[self.extension](self.get_latest_version_file()) # type: ignore
                data = reader_instance.read()

                data["info"]["updated_at"] = datetime.now().isoformat()
                with open(self.get_latest_version_file(), "w", encoding="utf-8") as f:
                    if self.extension == FileType.JSON:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                    elif self.extension == FileType.YAML:
                        yaml.safe_dump(data, f, allow_unicode=True)
            return result

        return wrapper