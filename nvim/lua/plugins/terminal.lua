return {
	{
		'akinsho/toggleterm.nvim',
		version = "*",
		config = function()
			function _G.set_terminal_keymaps()
				local opts = { buffer = 0 }
				vim.keymap.set('t', '<esc>', [[<C-\><C-n>]], opts)
			end

			-- if you only want these mappings for toggle term use term://*toggleterm#* instead
			vim.cmd('autocmd! TermOpen term://*toggleterm#* lua set_terminal_keymaps()')

			require("toggleterm").setup({
				open_mapping = [[<leader>`]],
				shell = "fish",
				autochdir = true,
				start_in_insert = false,
				size = function(term)
					return vim.o.lines * 0.5
				end,
				shade_terminals = true,
				insert_mappings = false,
			})
		end
	},
}
