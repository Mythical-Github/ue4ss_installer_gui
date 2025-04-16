from enum import Enum
from typing import List
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
    installed_files: List[Path] = field(default_factory=list)
    platform: GamePlatforms = GamePlatforms.OTHER
