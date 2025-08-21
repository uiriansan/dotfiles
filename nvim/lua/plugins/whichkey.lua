return {
	{
		"folke/which-key.nvim",
		event = "VeryLazy",
		opts = {
			preset = "helix",
			presets = {
				operators = true,
				motions = true,
			},
			win = {
				width = 50,
				padding = { 1, 2 },
				-- border = "none",
				title = false,
			},
			show_keys = false,
			show_help = false,
		},
		keys = {
			{
				"<leader>c",
				"",
				desc = "LSP"
			},
			{
				"<leader>T",
				"",
				desc = "Trouble"
			},

			-- Window maps
			{
				"g<Right>",
				"",
				desc = "Move focus to the right",
			},
			{
				"g<Down>",
				"",
				desc = "Move focus down",
			},
			{
				"g<Left>",
				"",
				desc = "Move focus to the left",
			},
			{
				"g<Up>",
				"",
				desc = "Move focus up",
			},
		},
	}
}
