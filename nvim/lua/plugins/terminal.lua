return {
	{
		'akinsho/toggleterm.nvim',
		version = "*",
		opts = {
			open_mapping = [[<leader>`]],
			shell = "fish",
			autochdir = true,
			start_in_insert = true,
			size = function(term)
				return vim.o.lines * 0.5
			end,
		},
	},
}
