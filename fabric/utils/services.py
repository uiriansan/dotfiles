from fabric.hyprland.service import Hyprland

connection: Hyprland | None = None

def get_hyprland_connection() -> Hyprland:
    global connection
    if not connection:
        connection = Hyprland()

    return connection
