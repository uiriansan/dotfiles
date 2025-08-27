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
				desc = "LSP",
				mode = "n",
			},
			{
				"<leader>T",
				"",
				desc = "Trouble",
				mode = "n",
			},

			-- Window maps
			{
				"g<Right>",
				"",
				desc = "Move focus to the right",
				mode = "n",
			},
			{
				"g<Down>",
				"",
				desc = "Move focus down",
				mode = "n",
			},
			{
				"g<Left>",
				"",
				desc = "Move focus to the left",
				mode = "n",
			},
			{
				"g<Up>",
				"",
				desc = "Move focus up",
				mode = "n",
			},
		},
	}
}
