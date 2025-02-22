return {
	"folke/snacks.nvim",
	priority = 1000,
	lazy = false,
	---@type snacks.Config
	opts = {
		dashboard = {
			autokeys = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ",
			preset = {
				keys = {
					{
						{ key = "n", hidden = true, action = ":ene | startinsert" },
						{ key = "o", hidden = true, action = ":Oil --float" },
						{ key = "f", hidden = true, action = ":lua Snacks.dashboard.pick('files')" },
						{ key = "r", hidden = true, action = ":lua Snacks.dashboard.pick('oldfiles')" },
						{ key = "g", hidden = true, action = ":lua Snacks.dashboard.pick('live_grep')" },
						{ key = "s", hidden = true, section = "session" },
						{ key = "L", hidden = true, action = ":Lazy",                                  enabled = package.loaded.lazy ~= nil },
						{ key = "q", hidden = true, action = ":qa",                                    enabled = package.loaded.lazy ~= nil },
					},
				},
			},
			formats = {
				key = { "" },
				file = function(item)
					return {
						{ item.key,                           hl = "key" },
						{ " " },
						{ item.file:sub(2):match("^(.*[/])"), hl = "NonText" },
						{ item.file:match("([^/]+)$"),        hl = "Normal" },
					}
				end,
				icon = { "" },
			},
			sections = {
				-- hidden
				{ section = "keys" },
				-- not hidden
				{
					section = "terminal",
					cmd = "chafa ~/.config/fastfetch/lain.png --align center --format kitty",
					width = 15,
				},
				{
					{
						{ text = "" },
						{
							text = {
								{ "n ",           hl = "key" },
								{ "New file",     hl = "Normal" },
								{ "",             width = 10 },
								{ "r ",           hl = "key" },
								{ "Recent files", hl = "Normal" },
							},
						},
						{ text = "", padding = 1 },
						{
							text = {
								{ "o ",        hl = "key" },
								{ "Open file", hl = "Normal" },
								{ "",          width = 9 },
								{ "g ",        hl = "key" },
								{ "Grep text", hl = "Normal" },
							},
						},
						{ text = "", padding = 1 },
						{
							text = {
								{ "f ",              hl = "key" },
								{ "Find files",      hl = "Normal" },
								{ "",                width = 8 },
								{ "s ",              hl = "key" },
								{ "Restore session", hl = "Normal" },
							},
						},
					},
					{ text = "",            padding = 2 },
					{ title = "Projects",   padding = 1 },
					{ section = "projects", limit = 10, padding = 2 },
				},
			},
		},
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
		quickfile = { enabled = true },
		scroll = { enabled = true },
		words = { enabled = true },
		image = { enabeld = true },
		win = { enabled = true },
		rename = { enabled = true },
	},
	config = function(_, opts)
		require("snacks").setup(opts)
	end,
}
