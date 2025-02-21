if status is-interactive
	# Start TMux Session
end

function fish_greeting
	nf # Run Fastfetch
end

alias nf="fastfetch"
alias ff="fastfetch"
alias neofetch="fastfetch"

alias ls="ls -l"

alias vim=nvim_open_file
alias v=nvim_open_file
alias vi=nvim_open_file
alias neovim=nvim_open_file
alias nvim=nvim_open_file

set -U EDITOR /usr/bin/nvim

fish_add_path /home/uirian/.local/bin/
fish_add_path /home/uirian/.spicetify

# bun
set --export BUN_INSTALL "$HOME/.bun"
set --export PATH $BUN_INSTALL/bin $PATH

# starship
starship init fish | source
