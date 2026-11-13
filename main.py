from frontend.app import App
from backend.database import Database
from backend.reader import FileType, YAMLReader


def clean_temp_files() -> None:
    import os
    from pathlib import Path
    temp_files = [
        Path(__file__).parent / "backend" / "template" / "output.html"
    ]
    for temp_file in temp_files:
        if temp_file.exists():
            os.remove(temp_file)


def get_file_type(properties: dict) -> FileType:
    reader_type = properties.get("reader_type", "yaml")
    file_type_members = FileType.__dict__["_member_map_"]
    supported_types = map(lambda x: x.lower(), file_type_members.keys())

    if reader_type.lower() not in supported_types:
        raise ValueError(f"Unsupported reader type: {reader_type}. Supported types are: {', '.join(supported_types)}")

    return FileType[reader_type.upper()]


def main() -> None:
    properties = YAMLReader("properties.yaml").read()

    is_test = properties.get("is_test", False)
    file_type = get_file_type(properties)

    db = Database(file_type)
    app = App(db, is_test=is_test)
    app.mainloop()


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        clean_temp_files()