return {
	"folke/snacks.nvim",
	dependencies = {
		"lewis6991/gitsigns.nvim",
	},
	priority = 1000,
	lazy = false,
	---@type snacks.Config
	opts = {
		bigfile = { enabled = true },
		explorer = { enabled = false },
		indent = { enabled = true },
		input = { enabled = true },
		image = { enabled = true },
		lazygit = {
			enabled = true,
			configure = true,
			win = {
				style = {
					width = 0,
					height = 0,
				},
			},
		},
		gitbrowse = {
			enabled = true,
			notify  = true,
		},
		notifier = { enabled = true },
		quickfile = { enabled = true },
		scope = { enabled = true },
		scroll = { enabled = true },
		statuscolumn = {
			enabled = true,
			left = { "mark", "sign" }, -- priority of signs on the left (high to low)
			right = { "git" }, -- priority of signs on the right (high to low)
			folds = {
				open = false, -- show open fold icons
				git_hl = false, -- use Git Signs hl for fold icons
			},
			git = {
				-- patterns to match Git signs
				patterns = { "GitSign", "MiniDiffSign" },
			},
			refresh = 50, -- refresh at most every 50ms
		},
		words = { enabled = true },
	},
	keys = {
		{
			"<leader>gl",
			function()
				require("snacks").lazygit()
			end,
			desc = "Open LazyGit",
			mode = "n",
		},
		{
			"<leader>go",
			function()
				require("snacks").gitbrowse()
			end,
			desc = "Open repo in browser",
			mode = "n",
		}
	}
}
