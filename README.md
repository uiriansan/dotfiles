Under development...\
Old version here: https://github.com/uiriansan/wsl-dotfiles-old
-- --
Neovim             |  Terminal
:-------------------------:|:-------------------------:
![Neovim preview](https://github.com/uiriansan/wsl-dotfiles/blob/main/nvim_preview.png)  |  ![Terminal preview](https://github.com/uiriansan/wsl-dotfiles/blob/main/fish_preview.png)

## Tools

- [**Windows Terminal**](https://github.com/microsoft/terminal)
- [**Arch Linux**](https://apps.microsoft.com/detail/9mznmnksm73x?hl=en-us)
- [**Tmux**](https://github.com/tmux/tmux/)
- [**Fish**](https://github.com/fish-shell/fish-shell) and [**Starship**](https://github.com/starship/starship)
- [**Neovim**](https://github.com/neovim/neovim)
- [**Yazi**](https://github.com/sxyazi/yazi)
- [**Bottom**](https://github.com/ClementTsang/bottom)
- [**Fastfetch**](https://github.com/fastfetch-cli/fastfetch)

## Keybindings

## Requirements
Pretty much everything in [pkglist.txt](https://github.com/uiriansan/wsl-dotfiles/blob/main/pkglist.txt).
To install on Arch, run `pacman -S --needed $(comm -12 <(pacman -Slq | sort) <(sort pkglist.txt))`

## Installation
`$ ./setup.sh`

## Special thanks
- [Asthestarsfalll/img2art](https://github.com/Asthestarsfalll/img2art) and [nxtkofi/LightningNvim](https://github.com/nxtkofi/LightningNvim?tab=readme-ov-file#dashboard-images): Neovim dashboard art;
