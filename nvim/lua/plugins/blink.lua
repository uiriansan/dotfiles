return {
	{
		"saghen/blink.cmp",
		version = "1.*",
		dependencies = {
			"rafamadriz/friendly-snippets",
			{
				"folke/lazydev.nvim",
				ft = "lua", -- only load on lua files
				opts = {
					library = {
						-- See the configuration section for more details
						-- Load luvit types when the `vim.uv` word is found
						{ path = "${3rd}/luv/library", words = { "vim%.uv" } },
					},
				},
			},
		},
		---@module 'blink.cmp'
		---@type blink.cmp.Config
		opts = {
			keymap = {
				preset = "default",
			},
			signature = { enabled = true },
			appearance = {
				nerd_font_variant = "mono",
			},

			completion = {
				documentation = {
					auto_show = true,
				},
				list = {
					-- Maximum number of items to display
					max_items = 100,

					selection = {
						-- When `true`, will automatically select the first item in the completion list
						preselect = true,
						-- When `true`, inserts the completion item automatically when selecting it
						-- You may want to bind a key to the `cancel` command (default <C-e>) when using this option,
						-- which will both undo the selection and hide the completion menu
						auto_insert = false,
					},
					cycle = {
						from_bottom = true,
						from_top = true,
					},
				},
			},

			sources = {
				default = { "lsp", "path", "snippets", "buffer", "lazydev" },
				providers = {
					lazydev = {
						name = "LazyDev",
						module = "lazydev.integrations.blink",
						score_offset = 100, -- make lazydev completions top priority (see `:h blink.cmp`)
					},
				},
			},
		},
		opts_extend = { "sources.default" },
	},
}
