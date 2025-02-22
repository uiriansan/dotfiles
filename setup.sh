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
# mkdir -p ~/.config ~/Pictures ~/Documents ~/Code ~/Sources
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
# sudo pacman --noconfirm -S --needed grub ntfs-3g bottom chafa jq clang cmake cronie eza fasm fastfetch feh fish fzf gdb git glfw htop libsixel fd lua luarocks lazygit man-db man-pages nasm qemu-desktop npm openssh python-pip python-pipx ripgrep rust-analyzer rustup starship neovim tmux tree unzip xclip yazi nvidia-dkms nvidia-utils egl-wayland hyprland xdg-desktop-portal-hyprland hyprpaper kitty ghostty firefox spotify-launcher sddm qt5-declarative uwsm pipewire dunst qt5-wayland qt6-wayland qt5-svg qt5-quickcontrols2 hyprpolkitagent lxappearance nwg-look pulseaudio playerctl qt5-graphicaleffects wl-clipboard fzy imagemagick sbctl bluez-utils linux-headers
#
# # fabric 
# sudo pacman -S gtk3 cairo gtk-layer-shell libgirepository gobject-introspection gobject-introspection-runtime python python-pip python-gobject python-cairo python-loguru pkgconf
#
# yay -S python-fabric-git
#
# yay -S rose-pine-hyprcursor
# yay -S hyprshot
#
# pipx ensurepath
# pipx install img2art
#
# # Install Rust
# rustup default stable
#
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
# # sudo pacman -S ttf-jetbrains-mono-nerd
# # sudo pacman -S adobe-source-han-sans-cn-fonts adobe-source-han-sans-jp-fonts adobe-source-han-sans-kr-fonts adobe-source-han-sans-otc-fonts adobe-source-han-sans-tw-fonts adobe-source-han-serif-cn-fonts adobe-source-han-serif-jp-fonts adobe-source-han-serif-kr-fonts adobe-source-han-serif-otc-fonts adobe-source-han-serif-tw-fonts
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
