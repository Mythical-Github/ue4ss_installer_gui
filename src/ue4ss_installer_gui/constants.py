from screeninfo import get_monitors

PRIMARY_MONITOR = get_monitors()[0]

SCREEN_WIDTH = PRIMARY_MONITOR.width
SCREEN_HEIGHT = PRIMARY_MONITOR.height

WINDOW_WIDTH = 600
WINDOW_HEIGHT = 800

X = int((SCREEN_WIDTH - WINDOW_WIDTH) / 2)
Y = int((SCREEN_HEIGHT - WINDOW_HEIGHT) / 2)

HEADER_HEIGHT = 40
SUBHEADER_HEIGHT = 30
FOOTER_HEIGHT = 28
DIVIDER_HEIGHT = 15
MARGIN = 40

UE4SS_REPO_URL = "https://github.com/UE4SS-RE/RE-UE4SS"

APP_TITLE = "UE4SS Installer"

# this is a list of base game dir names, for games that can contain more than one game installation
# if the game name is here, it will do additional scanning
MULTI_GAME_NAMES = ["Poppy Playtime"]

# this is a list of game titles, to prevent being populated in the menu, mostly for competitive games
INVALID_GAMES = ["place_holder_title_name"]

# a dict of sub paths to friendly display names, this will override normal display names, useful for games
# where the default name is messy, or indistinguishable
GAME_PATHS_TO_DISPLAY_NAMES = {
    r"Poppy Playtime\WindowsNoEditor": "Poppy Playtime - Chapter 1",
    "PlaytimeLauncher": "Poppy Playtime - Launcher",
    "TheKillingAntidotePlaytest": "The Killing Antidote Playtest",
    "TheKillingAntidote": "The Killing Antidote",
    "BronzebeardsTavern-Windows": "Bronzebeard's Tavern",
}
