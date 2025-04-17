# #!/bin/bash
#
# #############################################################
# #															#
# #			https://github.com/uiriansan/hyprdots			#
# #															#
# #############################################################
#
#
# # 1. Create directories
# mkdir -p ~/.config ~/Pictures/Screenshots ~/Documents ~/Code ~/Sources
# echo -e "\e[32m\e[1mUser directories created!\e[0m"
#
# # 2. Upgrade system
# sudo pacman --noconfirm -Syu
# echo -e "\e[32m\e[1mSystem upgraded!\e[0m"
#
# # 3. Copy everything into .config/
# cp -r . ~/.config ####### FIX THIS PATH!!!
# echo -e "\e[32m\e[1mConfig copied!\e[0m"
#
# # 4. Install essentials
# echo -e "\e[34m\e[1mInstalling essentials...\e[0m"
#
# sudo pacman --noconfirm -S --needed grub ntfs-3g bottom cpio gtk-engine-murrine meson pkg-config obsidian chafa jq clang cmake cronie eza fasm fastfetch feh fish fzf gdb git glfw htop libsixel fd bat wget lua luarocks dart-sass cava zed wf-recorder hypridle slurp lazygit man-db man-pages nasm qemu-desktop npm inkscape blender openssh python-pip python-pipx ripgrep rust-analyzer rustup starship neovim tmux tree xdg-desktop-portal-gtk xdg-desktop-portal-hyprland hyprpolkitagent weston hyprwayland-scanner unzip xclip yazi nvidia-dkms nvidia-utils egl-wayland hyprland xdg-desktop-portal-hyprland hyprpaper kitty ghostty firefox spotify-launcher sddm qt5-declarative uwsm pipewire wireplumber qt5-wayland qt6-wayland qt5-svg qt5-quickcontrols2 hyprpolkitagent lxappearance nwg-look pulseaudio playerctl qt5-graphicaleffects wl-clipboard fzy imagemagick zoxide sbctl xdg-desktop-portal-wlr bluez-utils linux-headers
#
# # Fabric
# sudo pacman -S --noconfirm --needed pipewire playerctl dart-sass power-profiles-daemon networkmanager brightnessctl pkgconf wf-recorder kitty python pacman-contrib gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python-pip python-gobject python-psutil python-dbus python-cairo python-loguru python-setproctitle
#
# yay -S --needed gray-git python-fabric gnome-bluetooth-3.0 python-rlottie-python python-pytomlpp slurp imagemagick tesseract tesseract-data-eng
#
# We may need to source the virtual environment for the Frabric config:
# cd ~/.config/fabric/
# source venv/bin/activate.fish # Since this script uses Bash, this might be a problem
# pip install -r 'requirements.txt'
# -----------------------------------------------------
#
# Hyprland plugins:
# hyprpm update
# hyprpm add https://github.com/Duckonaut/split-monitor-workspaces
# hyprpm add https://github.com/pyt0xic/hyprfocus
#
# hyprpm enable split-monitor-workspaces hyprfocus
# hyprpm reload
#
# git clone https://github.com/coffeeispower/woomer.git ~/Sources/woomer/
# cd ~/Sources/woomer/
# cargo b
#
# yay -S rose-pine-hyprcursor
# yay -S hyprshot
# yay -S hyprshade-git
# yay -S hyprsunset
# yay -S hyprswitch
# yay -S hyprmag-git
#
# GTK Cursor:
# wget -O ~/Downloads/BreezeXDark.tar.xz "https://github.com/ful1e5/BreezeX_Cursor/releases/latest/download/BreezeX-Dark.tar.xz" | tar -xvf BreezeX-Dark.tar.xz
# sudo tar -xvf ~/Downloads/BreezeXDark.tar.xz -C /usr/share/icons/
#
# pipx ensurepath
# pipx install img2art
#
# # Install Rust
# rustup default stable
#
# echo -e "\e[32m\e[1mEssentials installed!\e[0m"
#
# # 5. DRM kernel mode setting
# echo -e "\e[34m\e[1mDRM kernel mode setting...\e[0m"
#
# echo -e "\e[31m\e[1mEdit /etc/mkinitcpio.conf and add the following module names in the MODULE array:\nMODULES=(... nvidia nvidia_modeset nvidia_uvm nvidia_drm ...)\e[0m"
#
# EDITOR=nvim sudoedit /etc/mkinitcpio.conf
#
# read -p "Save the file and type 'yes' to continue: " DRM_CONF
# while [[ $DRM_CONF != "yes" ]] ; do
# 	read -p "Save the file and type 'yes' to continue: " DRM_CONF
# done
#
# echo "options nvidia_drm modeset=1 fbdev=1" | sudo tee -a /etc/modprobe.d/nvidia.conf
#
# sudo mkinitcpio -P
#
# echo -e "\e[32m\e[1mDRM kernel mode setting finished!\e[0m"
#
# # 6. Improve Nvidia\Wayland compatibility
# echo -e "\e[34m\e[1mImproving Nvidia/Wayland compatibility...\e[0m"
#
# # sudo pacman --noconfirm -S libva-nvidia-driver
#
# echo -e "\e[31m\e[1mEdit /etc/spotify-launcher.conf and uncomment this line:\nextra_arguments = ["--enable-features=UseOzonePlatform", "--ozone-platform=wayland"]\e[0m"
#
# EDITOR=nvim sudoedit /etc/spotify-launcher.conf
#
# read -p "Save the file and type 'yes' to continue: " SPOTIFY_CONF
# while [[ $SPOTIFY_CONF != "yes" ]] ; do
# 	read -p "Save the file and type 'yes' to continue: " SPOTIFY_CONF
# done
#
# echo -e "\e[32m\e[1mNvidia/Wayland compatibility improved!\e[0m"
#
# # 7. Setup SDDM
# echo -e "\e[34m\e[1mConfiguring SDDM...\e[0m"
#
# sudo systemctl enable sddm.service
#
# # 8. Setup weather cron job
# echo -e "\e[34m\e[1mConfiguring weather cron job...\e[0m"
#
# sudo systemctl enable cronie.service
# sudo systemctl start cronie.service
#
# CRONJOB="*/30 * * * * ${HOME}/.config/scripts/consume_weather.sh >> ${HOME}/.config/scripts/weather_cron.log"
# (crontab -l; echo "$CRONJOB") | crontab -
#
# chmod +x ~/.config/scripts/consume_weather.sh
# source $HOME/.config/scripts/consume_weather.sh
#
# echo -e "\e[32m\e[1mWeather cron configured!\e[0m"
#
# # 9. Setup pkglist.txt
# echo -e "\e[34m\e[1mConfiguring pkglist.txt...\e[0m"
#
# sudo cp ~/.config/savepkgs.hook /usr/share/libalpm/hooks/
# chmod +x ~/.config/savepkgs.sh
#
# read -p "Install pkglist.txt contents? (y/n): " PLIST_CONF
# if [[ $PLIST_CONF =~ ^[Yy]$ ]] then
# 	sudo pacman --noconfirm -S --needed $(comm -12 <(pacman -Slq | sort) <(sort ~/.config/pkglist.txt))
# else
# 	echo "You can install them later with\nsudo pacman -S --needed $(comm -12 <(pacman -Slq | sort) <(sort ~/.config/pkglist.txt))"
# fi
#
# echo -e "\e[32m\e[1mSetup completed!\e[0m"
#
# # sudo pacman -S ttf-jetbrains-mono-nerd ttf-ubuntu-mono-nerd ttf-ubuntu-nerd
# # sudo pacman -S adobe-source-han-sans-cn-fonts adobe-source-han-sans-jp-fonts adobe-source-han-sans-kr-fonts adobe-source-han-sans-otc-fonts adobe-source-han-sans-tw-fonts adobe-source-han-serif-cn-fonts adobe-source-han-serif-jp-fonts adobe-source-han-serif-kr-fonts adobe-source-han-serif-otc-fonts adobe-source-han-serif-tw-fonts noto-fonts noto-fonts-cjk noto-fonts-emoji inter-font
#
# ssh-keygen -t ed25519 -C "uiriansan@gmail.com"
#
# git config --global user.email "uiriansan@gmail.com"
# git config --global user.name "uiriansan"
# git config --global init.defaultBranch main
# # Update config repo to use ssh
# git remote set-url origin git@github.com:uiriansan/hyprdots.git
#
# sudo cp -r ~/.config/sddm/themes/deepin/ /usr/share/sddm/themes/
# sudo sed -i "s/^Current=.*/Current=deepin/g" /usr/lib/sddm/sddm.conf.d/default.conf
# # SDDM user avatar (gotta be .png)
# # Convert with $ magick convert <image.jpg> <image.png>
# # Print its size with $ magick /usr/share/sddm/faces/uirian.face.icon -print "Size: %wx%h\n" /dev/null
# # Cut square with $ magick .config/sddm/uirian.png -gravity center -extent "%[fx:h<w?h:w]x%[fx:h<w?h:w]" .config/sddm/uirian.png
# #
# # qt5-svg qt5-quickcontrols2
# sudo cp <image> /usr/share/sddm/faces/username.face.icon
#
# sudo pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si
#
# yay -S zen-browser-bin
#
# # Anyrun
# yay -S anyrun-git
# yay -S walker-bin
# yay -S units
#
# curl -fsSL https://raw.githubusercontent.com/spicetify/cli/main/install.sh | sh
#
#
# # Grub
# sudo cp -r ~/.config/grub/themes/lain/ /boot/grub/themes/
#
# # https://unix.stackexchange.com/a/33005
#
# sudo sed -i 's/^#GRUB_THEME=.*/GRUB_THEME="\/boot\/grub\/themes\/lain\/theme.txt"/g' /etc/default/grub
#
# # Removing the partition names from os-prober entries
# sudo sed -i 's/onstr="$(gettext_printf "(on %s)" "${DEVICE}")"/onstr=""/g' /etc/grub.d/30_os-prober
#
# # Use short name ("Windows" instead of "Windows Boot Manager")
# sudo sed -i 's/LONGNAME="`echo ${OS} | cut -d \':\' -f 2 | tr \'^\' \' \'`"/LONGNAME="`echo ${OS} | cut -d \':\' -f 3 | tr \'^\' \' \'`"/g' /etc/grub.d/30_os-prober
#
# # Move os-prober entries before Linux
# sudo mv /etc/grub.d/30_os-prober /etc/grub.d/05_os-prober
#
# # Add icon to "Advanced options"
# # Change "Advanced options for OS" to "OS Options"
# sudo sed -i 's/gettext_printf "Advanced options for %s" "\${OS}" | grub_quote)\' /gettext_printf "Options for %s" "\${OS}" | cut -d \' \' -f1,2,3 | grub_quote)\' --class advanced_options /g' /etc/grub.d/10_linux
#
# # Add icon to "UEFI Firmware Settings"
# sudo sed -i 's/menuentry \'$LABEL\' \\\$menuentry_id_option/menuentry \'$LABEL\' --class uefi_firmware_settings \\\$menuentry_id_option/g' /etc/grub.d/30_uefi-firmware
#
# sudo grub-mkconfig -o /boot/grub/grub.cfg
# # /etc/grub.d/


# Unzip ~/config/gtk/Kanagawa....zip
# Move the extracted files to the following paths:

    # For GTK3: ~/.themes In this path you must move the entire theme folder.
    # For GTK4: ~/.config/gtk-4.0 The files to move to this path can be found inside the theme directory in the gtk-4.0 folder, copy only the assets, gtk.css and gtk-dark.css files or create a symlinks.

#

# Applying the themes
    #
    # For GTK3, apply themes from Gnome Tweaks.
    # For GTK4 applications it is only necessary to have moved the assets, gtk.css and gtk-dark.css files to the ~/.config/gtk-4.0 path, and if you notice that the theme has not been applied, just close and reopen the application.
    #
# https://github.com/Fausto-Korpsvart/Kanagawa-GKT-Theme?tab=readme-ov-file
