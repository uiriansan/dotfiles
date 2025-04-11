MAIN_MONITOR_ID = 1
WORKSPACES_PER_MONITOR = 5

window_pattern_list = {
    "class:zen$": "Zen Browser",
    "title:nvim.*$": "Neovim",
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

# Google AI Studio API:
# https://aistudio.google.com/u/2/apikey?pli=1
GOOGLE_AI_STUDIO_API_FILE = ".gemini_key"
