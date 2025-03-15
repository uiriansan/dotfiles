# Run Fastfetch the first time the terminal on the second window gets focused. so it displays correctly
function wait_nf
	set WAITNF $(tmux showenv WAIT_FISH_NF | sed "s:^.*=::")
	if test $WAITNF = 1
		tmux send-keys -t dev:Fish.1 "nf" C-m
		tmux setenv -r WAIT_FISH_NF
		set -e WAITNF
	end
end
