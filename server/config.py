import toml
from pathlib import Path
from pydantic import BaseModel
from typing import Optional


class DB(BaseModel):
    host: str
    port: int
    user: str
    password: Optional[str]
    db: str


class Config(BaseModel):
    db: DB


def get_config():
    dirpath = Path("..")
    path = dirpath / "config.toml"
    if not path.is_file():
        path = dirpath / "config.default.toml"
    config = toml.load(path)
    return Config(db=config["db"])
