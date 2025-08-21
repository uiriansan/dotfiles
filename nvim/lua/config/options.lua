vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

-- Sync clipboard between OS and Neovim.
--  Schedule the setting after `UiEnter` because it can increase startup-time.
--  See `:help 'clipboard'`
vim.schedule(function()
	vim.opt.clipboard = "unnamedplus"
end)

vim.g.tpipeline_autoembed = 1
vim.g.tpipeline_fillcentre = 1
vim.g.tpipeline_restore = 1

-- disable netrw
vim.g.loaded_netrw = 1
vim.g.loaded_netrwPlugin = 1

vim.opt.termguicolors = true

vim.opt.tabstop = 4
vim.opt.shiftwidth = 4

-- Set to true if you have a Nerd Font installed and selected in the terminal
vim.g.have_nerd_font = true

-- Make line numbers default
vim.opt.number = true
vim.opt.relativenumber = true

-- Disable wrap
vim.opt.wrap = false

-- Enable mouse mode, can be useful for resizing splits for example!
vim.opt.mouse = "a"

-- Don't show the mode, since it's already in the status line
vim.opt.showmode = false

-- Sync clipboard between OS and Neovim.
--  Schedule the setting after `UiEnter` because it can increase startup-time.
--  See `:help 'clipboard'`
vim.schedule(function()
	vim.opt.clipboard = "unnamedplus"
end)

-- Enable break indent
vim.opt.breakindent = true

-- Save undo history
vim.opt.undofile = true

vim.opt.ignorecase = false
vim.opt.smartcase = false

vim.opt.signcolumn = "no" -- "yes" | "number"

-- Decrease update time
vim.opt.updatetime = 250

-- Decrease mapped sequence wait time
-- Displays which-key popup sooner
vim.opt.timeoutlen = 300

-- Configure how new splits should be opened
vim.opt.splitright = true
vim.opt.splitbelow = true

-- Sets how neovim will display certain whitespace characters in the editor.
--  See `:help 'list'`
--  and `:help 'listchars'`
vim.opt.list = true
vim.opt.listchars = { tab = "  ", trail = "·", nbsp = "␣" }

-- Remove "~" from line numbers after end of buffer
vim.opt.fillchars = { eob = " " }

-- Preview substitutions live, as you type!
vim.opt.inccommand = "split"

-- Show which line your cursor is on
vim.opt.cursorline = true

-- Minimal number of screen lines to keep above and below the cursor.
vim.opt.scrolloff = 5

-- remove cmdline when its not in use
vim.o.cmdheight = 0

-- Show diagnostics signs on the right
-- :h vim.diagnostic.config()
vim.diagnostic.config({
	virtual_text = {
		suffix = "",
		prefix = "",
		virt_text_pos = "right_align",
		format = function(diagnostic)
			if diagnostic.severity == vim.diagnostic.severity.ERROR then
				return ""
			elseif diagnostic.severity == vim.diagnostic.severity.WARN then
				return ""
			elseif diagnostic.severity == vim.diagnostic.severity.HINT then
				return ""
			elseif diagnostic.severity == vim.diagnostic.severity.INFO then
				return ""
			end

			return ""
		end,
	},
	-- virtual_text = false,
	signs = false,
	underline = false,
	float = {
		border = "rounded",
		source = true,
	},
	severity_sort = true,
	update_in_insert = true,
})

-- Hide status line
vim.opt.laststatus = 0

-- Disable swap files
vim.opt.swapfile = false

-- border for all floating windows
vim.o.winborder = "rounded"
