# Save packages list
pacman -Qqe > pkglist.txt

# Copy Windows Terminal settings.json
sudo cp /mnt/c/Users/uiria/AppData/Local/Packages/Microsoft.WindowsTerminal_8wekyb3d8bbwe/LocalState/* ./windows_terminal/
