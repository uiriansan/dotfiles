return {
	{
		"catppuccin/nvim",
		priority = 1000,
		config = function()
			require("catppuccin").setup({
				color_overrides = {
					mocha = {
						base = "#14161B",
					},
				},
			})
		end,
	},
	{ "vague2k/vague.nvim" },
	{ "neanias/everforest-nvim" },
	{ "rebelot/kanagawa.nvim" },
	{ "rose-pine/neovim" },
	{ "olimorris/onedarkpro.nvim" },
	{ "AlexvZyl/nordic.nvim" },
	{ "tiagovla/tokyodark.nvim" },
	{ "bluz71/vim-moonfly-colors" },
	{ "oxfist/night-owl.nvim" },
	{ "sho-87/kanagawa-paper.nvim" },
	{ "kvrohit/mellow.nvim" },
}
