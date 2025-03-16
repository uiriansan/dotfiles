function tmux_start_dev
	if not set -q TMUX
		if not tmux has-session -t dev 2>/dev/null
			tmux new-session -d -s dev -n "Neovim"
			tmux send-keys -t dev:Neovim "nvim" C-m

			tmux new-window -t dev -n "Fish"

			tmux split-window -t dev:Fish -h
			tmux send-keys run_yazi C-m
			tmux split-window -t dev:Fish -v
			tmux send-keys "btm -b" C-m

			tmux resizep -t dev:Fish.2 -y "40%"

			tmux select-pane -t 2
			tmux select-pane -t 1
		
			# Run Fastfetch the first time the terminal on the second window gets focused.
			tmux setenv WAIT_FISH_NF 1

			# Link X11 server so that GUI applications work cross WSLg
			ln -s /mnt/wslg/.X11-unix/X0 /tmp/.X11-unix/X0
		end

		tmux attach-session -t dev:Neovim
	end
end

