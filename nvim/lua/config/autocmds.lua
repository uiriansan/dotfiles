-- Automatically cd into new working dir in the terminal across Tmux session
-- This autocommand relies on a Fish shell function: (https://github.com/uiriansan/wsl-dotfiles/blob/main/fish/functions/tmux_handle_nvim_working_dir.fish)

vim.api.nvim_create_autocmd("DirChanged", {
	command = "silent !tmux_handle_nvim_working_dir <afile>",
})

local function augroup(name)
	return vim.api.nvim_create_augroup("lazyvim_" .. name, { clear = true })
end

vim.api.nvim_create_autocmd("VimEnter", {
	group = augroup("autoupdate"),
	callback = function()
		require("lazy").update({
			show = false,
		})
	end,
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

-- Share clipboard with Windows
vim.opt.clipboard = "unnamedplus"
if vim.fn.has("wsl") == 1 then
	vim.api.nvim_create_autocmd("TextYankPost", {

		group = vim.api.nvim_create_augroup("Yank", { clear = true }),

		callback = function()
			vim.fn.system("clip.exe", vim.fn.getreg('"'))
		end,
	})
end
