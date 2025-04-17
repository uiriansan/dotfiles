MAIN_MONITOR_ID = 1
WORKSPACES_PER_MONITOR = 5

BACKGROUND_COLOR = "#161617"
FOREGROUND_COLOR = "#FFFFFF"
ACCENT_COLOR = ""  # TODO:
BORDER_RADIUS = 10

window_pattern_list = {
    "class:zen$": "Zen Browser",
    "class:dev.zed.Zed$": "Zed Editor",
    "title:nvim.*$": "Neovim",
    "class:Emacs": "Emacs",
    "title:Yazi.*$": "Yazi",
    "class:com.mitchellh.ghostty$": "Ghostty",
    "ititle:Spotify Premium$": "Spotify",
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
    "brightness",
    "volume",
    "internet_status",
]

# Google AI Studio API:
# https://aistudio.google.com/u/2/apikey?pli=1
GOOGLE_AI_STUDIO_API_FILE = ".gemini_key"
