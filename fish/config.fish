if status is-interactive
	# Start TMux Session
end

function day_suffix
	switch $(date +%-d)
		case 1 21 31
			echo "st"
		case 2 22
			echo "nd"
		case 3 23
			echo "rd"
		case '*'
			echo "th"
	end
end

function fish_greeting
	# starship
	starship init fish | source

	set QUERY_RES (sqlite3 -json ~/.config/fish/facts/facts.db "SELECT text, year, pages FROM Facts WHERE type LIKE 'selected' AND day LIKE $(date +%-d) AND month LIKE $(date +%-m) ORDER BY RANDOM() LIMIT 1;" | jq 'first')

	set_color -b green -o black
	echo -n " $(date "+%B %-d$(day_suffix)") "
	set_color -b brblack -o white
	echo " in history: "
	set_color normal; echo

	set THUMB_URL (echo $QUERY_RES | jq -r '.pages | fromjson | .[0].thumb')
	if test -n $THUMB_URL
		echo -n (curl -s $THUMB_URL | chafa --size=30x10 --align="top,left")
	end

	echo -n 
	set_color normal;
	echo $QUERY_RES | jq -r '.text'
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
