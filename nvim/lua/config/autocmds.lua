-- Automatically cd into new working dir in the terminal across Tmux session
-- This autocommand relies on a Fish shell function: (https://github.com/uiriansan/wsl-dotfiles/blob/main/fish/functions/tmux_handle_nvim_working_dir.fish)

-- vim.api.nvim_create_autocmd("DirChanged", {
-- 	command = "silent !tmux_handle_nvim_working_dir <afile>",
-- })

-- Automatically load session on VimEnter and DirChanged
vim.api.nvim_create_autocmd({ "VimEnter", "DirChanged", }, {
	group = vim.api.nvim_create_augroup("Persistence", { clear = true }),
	callback = function()
		-- NOTE: Before restoring the session, check:
		-- 1. No arg passed when opening nvim, means no `nvim --some-arg ./some-path`
		-- 2. No pipe, e.g. `echo "Hello world" | nvim`
		if vim.fn.argc() == 0 and not vim.g.started_with_stdin then
			require("persistence").load()
		end
	end,
	-- HACK: need to enable `nested` otherwise the current buffer will not have a filetype(no syntax)
	nested = true,
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
