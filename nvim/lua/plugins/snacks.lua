return {
	"folke/snacks.nvim",
	priority = 1000,
	lazy = false,
	---@type snacks.Config
	opts = {
		bigfile = { enabled = true },
		indent = {
			enabled = true,
			indent = {
				only_scope = true,
				hl = "EndOfBuffer"
			},
			scope = {
				enabled = true,
				priority = 200,
				char = "│",
				underline = false,
				only_current = false,
				hl = "FoldColumn",
			},
			chunk = {
				enabled = false,
			},
			animate = {
				enabled = false,
			},
		},
		input = { enabled = true },
		notifier = {
			enabled = true,
			top_down = true,
		},
		statuscolumn = { enabled = true },
		quickfile = { enabled = true },
		scroll = { enabled = true },
		words = { enabled = true },
		image = { enabeld = true },
		win = { enabled = true },
		rename = { enabled = true },
	},
}
