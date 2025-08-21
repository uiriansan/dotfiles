return {
	---@type LazySpec
	{
		"mikavilpas/yazi.nvim",
		version = "*", -- use the latest stable version
		event = "VeryLazy",
		dependencies = {
			{ "nvim-lua/plenary.nvim", lazy = true },
		},
		keys = {
			{
				"<leader>e",
				"<cmd>Yazi<cr>",
				desc = "Resume the last yazi session",
				mode = { "n", "v" },
			},
		},
		---@type YaziConfig | {}
		opts = {
			-- if you want to open yazi instead of netrw, see below for more info

			enable_mouse_support = true,
			floating_window_scaling_factor = 1,
			yazi_floating_window_border = "none",
			keymaps = {
				show_help = "<f1>",
			},
			set_keymappings_function = function(yazi_buffer_id, config, context)
				vim.keymap.set({ 't' }, '<Esc>', function()
					context.api:emit_to_yazi { 'quit' }
				end, { buffer = yazi_buffer_id })

				vim.keymap.set({ 't' }, '<leader>e', function()
					context.api:emit_to_yazi { 'quit' }
				end, { buffer = yazi_buffer_id })
			end,
		},
		-- 👇 if you use `open_for_directories=true`, this is recommended
		init = function()
			-- mark netrw as loaded so it's not loaded at all.
			--
			-- More details: https://github.com/mikavilpas/yazi.nvim/issues/802
			vim.g.loaded_netrwPlugin = 1
		end,
	}
}
