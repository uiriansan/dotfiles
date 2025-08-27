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

-- turn Snacks off while the cmp menu is open, turn it back on afterward
local group = vim.api.nvim_create_augroup("BlinkCmpSnacksToggle", { clear = true })

vim.api.nvim_create_autocmd("User", {
	group = group,
	pattern = "BlinkCmpMenuOpen",
	callback = function() vim.g.snacks_animate = false end,
})

vim.api.nvim_create_autocmd("User", {
	group = group,
	pattern = "BlinkCmpMenuClose",
	callback = function() vim.g.snacks_animate = true end,
})

-- Explicitly start TS highlighting in markdown buffers
vim.api.nvim_create_autocmd("FileType", {
	pattern = { "markdown" },
	callback = function()
		vim.treesitter.start(0, "markdown")
	end,
})

-- Set Git branch name:
local function branch_name()
	local branch = vim.fn.system("git branch --show-current 2> /dev/null | tr -d '\n'")
	if branch ~= "" then
		return branch
	else
		return ""
	end
end


vim.api.nvim_create_autocmd({ "FileType", "BufEnter", "FocusGained" }, {
	callback = function()
		vim.b.branch_name = branch_name()
	end
})
