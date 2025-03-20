if status is-interactive
	# Start TMux Session
end

function fish_greeting
	# starship
	starship init fish | source

	sleep 0.1 # Gotta sleep here, otherwise fastfetch logo won't display properly
	
	nf #Run Fastfetch
end

function search_man_pages
	 apropos $argv | fzf -q $argv | awk '{print $1}' | xargs man
end

function open_manpage_in_nvim
	set manvim_tmp /tmp/$argv
	man $argv > $manvim_tmp
end

alias nf="fastfetch"
alias ff="fastfetch"
alias neofetch="fastfetch"

alias ls="lsd -A"

alias vim=nvim_open_file
alias v=nvim_open_file
alias vi=nvim_open_file
alias neovim=nvim_open_file
alias nvim=nvim_open_file

alias mansearch=search_man_pages

set -U EDITOR /usr/bin/nvim

fish_add_path /home/uirian/.local/bin/
fish_add_path /home/uirian/.spicetify

# bun
set --export BUN_INSTALL "$HOME/.bun"
set --export PATH $BUN_INSTALL/bin $PATH

# zoxide
zoxide init fish | source
