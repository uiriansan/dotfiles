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
			vim.cmd([[ colorscheme catppuccin-mocha ]])
		end,
	},
	-- {
	-- 	"vague2k/vague.nvim",
	-- 	config = function()
	-- 		require("vague").setup({
	-- 			-- optional configuration here
	-- 		})
	-- 		vim.cmd([[ colorscheme vague ]])
	-- 	end,
	-- },
}
