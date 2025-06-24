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
	{ "metalelf0/jellybeans-nvim" },
	{ "AlexvZyl/nordic.nvim" },
	{ "blazkowolf/gruber-darker.nvim" },
	{ "comfysage/evergarden",         opts = { variant = "hard" }, },
	{ "ramojus/mellifluous.nvim" },
	{ "neanias/everforest-nvim", },
	{ "sainnhe/gruvbox-material" },
	{
		"rebelot/kanagawa.nvim",
		priority = 1000,
		config = function()
			require("everforest").setup({
				background = "hard",
				colours_override = function(palette)
				end,
			})
		end,
	},
	{ "rose-pine/neovim" },
	{ "olimorris/onedarkpro.nvim" },
	{ "AlexvZyl/nordic.nvim" },
	{ "tiagovla/tokyodark.nvim" },
	{ "bluz71/vim-moonfly-colors" },
	{ "oxfist/night-owl.nvim" },
	{ "sho-87/kanagawa-paper.nvim" },
	{ "kvrohit/mellow.nvim", },
	{ "rktjmp/lush.nvim", },
	{
		"webhooked/kanso.nvim",
		lazy = false,
		priority = 1000,
		config = function()
			require("kanso").setup({
				theme = "zen",
			})
		end,
	},
}
