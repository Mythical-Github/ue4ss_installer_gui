from screeninfo import get_monitors

monitor = get_monitors()[0]

screen_width = monitor.width
screen_height = monitor.height

window_width = 600
window_height = 800

x = int((screen_width - window_width) / 2)
y = int((screen_height - window_height) / 2)

HEADER_HEIGHT = 40
SUBHEADER_HEIGHT = 30
FOOTER_HEIGHT = 28
DIVIDER_HEIGHT = 15
MARGIN = 40

UE4SS_REPO_URL = "https://github.com/UE4SS-RE/RE-UE4SS"
