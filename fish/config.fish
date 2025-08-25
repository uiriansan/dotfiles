if status is-interactive
	# Start TMux Session
end

function fish_greeting
	# starship
	starship init fish | source

	~/.config/fish/shell-facts/shell_facts
end

function countlines
	find . -name "*.$argv" | xargs wc -l
end

alias nf="fastfetch"
alias ff="fastfetch"
alias neofetch="fastfetch"

alias ls="lsd -A --hyperlink auto"
alias rg="rg --no-heading --hyperlink-format kitty"
alias wiki=wikiman

set --export VISUAL /usr/bin/zeditor
set --export EDITOR /usr/bin/nvim

fish_add_path /home/uirian/.local/bin/
fish_add_path /home/uirian/.spicetify

# bun
set --export BUN_INSTALL "$HOME/.bun"
set --export PATH $BUN_INSTALL/bin $PATH
set --export GIT_EDITOR nvim

set --export MANPAGER "less -R --use-color -Dd+r -Du+b"

# zoxide
zoxide init fish | source
