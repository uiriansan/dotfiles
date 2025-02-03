#!/bin/bash

#############################################################
#															#
#			https://github.com/uiriansan/hyprdots			#
#															#
#############################################################


# 1. Create directories
mkdir -p ~/.config ~/Pictures ~/Documents ~/Code ~/Sources
echo -e "\e[32m\e[1mUser directories created!\e[0m"

# 2. Upgrade system
sudo pacman --noconfirm -Syu
echo -e "\e[32m\e[1mSystem upgraded!\e[0m"

# 3. Copy everything into .config/
cp -r ./* ~/.config/
echo -e "\e[32m\e[1mConfig copied!\e[0m"

# 4. Install essentials
echo -e "\e[34m\e[1mInstalling essentials...\e[0m"

sudo pacman --noconfirm -S --needed grub bottom chafa clang cmake cronie eza fasm fastfetch feh fish fzf gdb git glfw htop libsixel lua luarocks man-db man-pages nasm qemu npm openssh python-pip python-pipx ripgrep wofi rust-analyzer rustup starship neovim tmux tree unzip xclip yazi nvidia-dkms nvidia-utils egl-wayland hyprland xdg-desktop-portal-hyprland kitty ghostty firefox spotify-launcher sddm qt5-declarative uwsm pipewire dunst qt5-wayland qt6-wayland hyprpolkitagent lxappearance nwg-look pulseaudio playerctl linux-headers

pipx ensurepath
pipx install img2art

echo -e "\e[32m\e[1mEssentials installed!\e[0m"

# 5. DRM kernel mode setting
echo -e "\e[34m\e[1mDRM kernel mode setting...\e[0m"

echo -e "\e[31m\e[1mEdit /etc/mkinitcpio.conf and add the following module names in the MODULE array:\nMODULES=(... nvidia nvidia_modeset nvidia_uvm nvidia_drm ...)\e[0m"

EDITOR=nvim sudoedit /etc/mkinitcpio.conf

read -p "Save the file and type 'yes' to continue: " DRM_CONF
while [[ $DRM_CONF != "yes" ]] ; do
	read -p "Save the file and type 'yes' to continue: " DRM_CONF
done

echo "options nvidia_drm modeset=1 fbdev=1" | sudo tee -a /etc/modprobe.d/nvidia.conf

sudo mkinitcpio -P

echo -e "\e[32m\e[1mDRM kernel mode setting finished!\e[0m"

# 6. Improve Nvidia\Wayland compatibility
echo -e "\e[34m\e[1mImproving Nvidia/Wayland compatibility...\e[0m"

sudo pacman --noconfirm -S libva-nvidia-driver

echo -e "\e[31m\e[1mEdit /etc/spotify-launcher.conf and uncomment this line:\nextra_arguments = ["--enable-features=UseOzonePlatform", "--ozone-platform=wayland"]\e[0m"

EDITOR=nvim sudoedit /etc/spotify-launcher.conf

read -p "Save the file and type 'yes' to continue: " SPOTIFY_CONF
while [[ $SPOTIFY_CONF != "yes" ]] ; do
	read -p "Save the file and type 'yes' to continue: " SPOTIFY_CONF
done

echo -e "\e[32m\e[1mNvidia/Wayland compatibility improved!\e[0m"

# 7. Setup SDDM
echo -e "\e[34m\e[1mConfiguring SDDM...\e[0m"

sudo systemctl enable sddm.service

# 8. Setup weather cron job
echo -e "\e[34m\e[1mConfiguring weather cron job...\e[0m"

sudo systemctl enable cronie.service
sudo systemctl start cronie.service

CRONJOB="*/30 * * * * ${HOME}/.config/scripts/consume_weather.sh >> ${HOME}/.config/scripts/weather_cron.log"
(crontab -l; echo "$cronjob") | crontab -

chmod +x ~/.config/scripts/consume_weather.sh
source $HOME/.config/scripts/consume_weather.sh

echo -e "\e[32m\e[1mWeather cron configured!\e[0m"

# 9. Setup pkglist.txt
echo -e "\e[34m\e[1mConfiguring pkglist.txt...\e[0m"

sudo cp ~/.config/savepkgs.hook /usr/share/libalpm/hooks/
chmod +x ~/.config/scripts/savepkgs.sh

read -p "Install pkglist.txt contents? (y/n): " PLIST_CONF
if [[ $PLIST_CONF =~ ^[Yy]$ ]] then
	sudo pacman --noconfirm -S --needed $(comm -12 <(pacman -Slq | sort) <(sort ~/.config/pkglist.txt))
else
	echo "You can install them later with\nsudo pacman -S --needed $(comm -12 <(pacman -Slq | sort) <(sort ~/.config/pkglist.txt))"
fi

echo -e "\e[32m\e[1mSetup completed!\e[0m"

echo -e "\e[31m\e[1mYou need to reboot your system.\e[0m"
read -p "Reboot now? (yes/no): " REBOOT_CONF
if [[ $REBOOT_CONF =~ ^[Yy]$ ]] then
	reboot
fi
