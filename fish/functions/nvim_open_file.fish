# This function is used to open files in the existing Neovim instance across Tmux instead of create another one

function nvim_open_file
	set file_path $(path resolve $argv)

	# if server file existis and Neovim is running, remote attach to it
	if test -e ~/.cache/nvim/server.pipe && pgrep -f /usr/bin/nvim > /dev/null
		# if path is provided and a directory, change nvim's working dir
		if test -d $file_path && count $argv > /dev/null
			set nvim_command "<C-\><C-N>:cd $file_path<CR>"
			/usr/bin/nvim --server ~/.cache/nvim/server.pipe --remote-send $nvim_command
		else if test -e $file_path
			set nvim_command "<C-\><C-N>:e $file_path<CR>"
			/usr/bin/nvim --server ~/.cache/nvim/server.pipe --remote-send $nvim_command
		#else if test -n string match "<C-*" $argv

		else
			/usr/bin/nvim $argv
		end
	else
		# Delete Neovim's server.pipe in case it exists (e.g. the session was killed with nvim running)
		rm -f ~/.cache/nvim/server.pipe
		
		# Create new server
	 	/usr/bin/nvim --listen ~/.cache/nvim/server.pipe $file_path
	end
end
