from enum import Enum
from typing import List, Type, Any
from pathlib import Path
from dataclasses import dataclass, field


class GamePlatforms(Enum):
    STEAM = "Steam"
    EPIC = "Epic"
    OTHER = "Other"


@dataclass
class GameInfo:
    install_dir: Path
    game_title: str
    ue4ss_version: str
    last_installed_version: str
    platform: GamePlatforms
    using_developer_version: bool
    show_pre_releases: bool
    using_portable_version: bool
    using_keep_mods_and_settings: bool
    installed_files: List[Path] = field(default_factory=list)


def get_enum_from_val(enum_cls: Type[Enum], value: Any) -> Enum:
    for entry in enum_cls:
        if entry.value == value:
            return entry
    raise ValueError(f"{value} is not a valid value for {enum_cls.__name__}")


def get_enum_strings_from_enum(enum_cls: Type[Enum]) -> list[str]:
    return [entry.value for entry in enum_cls]
