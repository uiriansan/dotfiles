-- Automatically cd into new working dir in the terminal across Tmux session
-- This autocommand relies on a Fish shell function: (https://github.com/uiriansan/wsl-dotfiles/blob/main/fish/functions/tmux_handle_nvim_working_dir.fish)

vim.api.nvim_create_autocmd("DirChanged", {
	command = "silent !tmux_handle_nvim_working_dir <afile>",
})

-- Highlight when yanking (copying) text
--  Try it with `yap` in normal mode
--  See `:help vim.highlight.on_yank()`
vim.api.nvim_create_autocmd("TextYankPost", {
	desc = "Highlight when yanking (copying) text",
	group = vim.api.nvim_create_augroup("kickstart-highlight-yank", { clear = true }),
	callback = function()
		vim.highlight.on_yank()
	end,
})

-- Let LSP know when a file has been renamed with Oil
vim.api.nvim_create_autocmd("User", {
	pattern = "OilActionsPost",
	callback = function(event)
		if event.data.actions.type == "move" then
			Snacks.rename.on_rename_file(event.data.actions.src_url, event.data.actions.dest_url)
		end
	end,
})
