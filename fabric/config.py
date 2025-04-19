SHELL_NAME = "fabric-shell"

MAIN_MONITOR_ID = 1
WORKSPACES_PER_MONITOR = 5

BACKGROUND_COLOR = "#161617"
FOREGROUND_COLOR = "#FFFFFF"
ACCENT_COLOR = ""  # TODO:
BORDER_RADIUS = 10

window_pattern_list = {
    "class:zen$": "Zen Browser",
    "class:dev.zed.Zed$": "Zed Editor",
    "title:Yazi.*$": "Yazi",
    "title:nvim.*$": "Neovim",
    "class:kitty": "Kitty",
    "ititle:Spotify Premium$": "Spotify",
    "class:com.mitchellh.ghostty$": "Ghostty",
    "class:discord$": "Discord",
    "class:obsidian$": "Obsidian",
    # extract groups with $*. Won't match because the line above returns
    "title:(.*?) — Zen Browser$": "$1",
}

workspace_pattern_list = {
    "special:magic": " ",
    "special:browser": " ",
}

toolbar_plugin_order = [
    "media",
    "color_picker",
    "magnifier",
    "screenshot",
    "screen_record",
    "screen_filters",
    "volume",
    "internet_status",
]

########## HYPRSHADE SCREEN FILTERS (SHADERS) ###########
HYPRSHADE_SHADER_PATH = "~/.config/hypr/utils/blue-light-filter-with-brightness.glsl.mustache"
DEFAULT_BLUE_LIGHT_FILTER_VALUE: float = 6000.0 # 6000 Kelvin  | min: 2000, max: 25000
DEFAULT_BRIGHTNESS_VALUE: float = 0.8 # 80% | min: 0.5, max: 1.0

# Google AI Studio API:
# https://aistudio.google.com/u/2/apikey?pli=1
GOOGLE_AI_STUDIO_API_FILE = ".gemini_key"
