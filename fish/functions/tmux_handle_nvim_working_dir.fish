# FIXME: When Neovim working dir changes, send-keys through Tmux to update the terminal (if its pwd eq ~/) and yazi

# TODO: Implement fish_send_keys

function tmux_handle_nvim_working_dir
	set new_working_dir $argv
	set -l panes $(tmux list-panes -t dev:Fish -F '#{pane_id}' | sed 's/^%//')

	for i in $(seq $(count $panes))
		set pane_process $(tmux display -p -t dev:Fish.$i '#{pane_current_command}')

		switch $pane_process
			# Waiting for passthrough bug to be fixed!!! (https://github.com/sxyazi/yazi/issues/2171 & https://github.com/tmux/tmux/issues/4302)
			#case yazi
				#tmux send-keys -t dev:Fish.$i "q"
				#tmux send-keys -t dev:Fish.$i "yazi $new_working_dir" C-m
			case fish
				tmux send-keys -t dev:Fish.$i "cd $new_working_dir" C-m
		end
	end
end
#  ERROR: No idea what's happening
