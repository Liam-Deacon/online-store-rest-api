from typing import Union
from pathlib import Path

import json


class JsonSQLDataIngress:
    def __init__(self, filepath: Union[Path, str], tablename: str):
        self.tablename = tablename
        self.filepath = Path(filepath)
        if not self.filepath.exists():
            raise FileNotFoundError(f"JSON data file '{filepath}'"
                                    " does not exist")

