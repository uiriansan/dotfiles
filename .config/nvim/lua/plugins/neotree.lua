-- Neo-tree is a Neovim plugin to browse the file system
-- https://github.com/nvim-neo-tree/neo-tree.nvim

return {
	{
		"nvim-neo-tree/neo-tree.nvim",
		version = "*",
		dependencies = {
			"nvim-lua/plenary.nvim",
			"nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
			"MunifTanjim/nui.nvim",
			"mrbjarksen/neo-tree-diagnostics.nvim",
		},
		cmd = "Neotree",
		keys = {
			{ "<leader>e", ":Neotree reveal<CR>", desc = "File explorer" },
		},
		config = function()
			require("neo-tree").setup({
				show_path = "none",
				close_if_last_window = true,
				auto_clean_after_session_restore = true,
				enable_diagnostics = false,
				enable_git_status = false,
				open_files_do_not_replace_types = { "terminal", "trouble", "qf" }, -- when opening files, do not use windows containing these filetypes or buftypes
				sources = {
					"filesystem",
					"diagnostics",
					"git_status",
				},
				source_selector = {
					winbar = true,
					statusline = false, -- toggle to show selector on statusline
					content_layout = "center",
					tabs_layout = "equal",
					sources = {
						{ source = "filesystem", display_name = "" .. "" },
					},
				},
				default_component_configs = {
					container = {
						enable_character_fade = true,
					},
					indent = {
						indent_size = 2,
						padding = 1,
						with_markers = false,
						indent_marker = "▏",
						last_indent_marker = "▏",
						highlight = "NeoTreeIndentMarker",
						with_expanders = true,
						expander_collapsed = "",
						expander_expanded = "",
						expander_highlight = "NeoTreeExpander",
					},
					icon = {
						folder_closed = "",
						folder_open = "",
						folder_empty = "󰜌",
						-- The next two settings are only a fallback, if you use nvim-web-devicons and configure default icons there
						-- then these will never be used.
						default = "*",
						highlight = "NeoTreeFileIcon",
					},
					modified = {
						symbol = "",
						highlight = "NeoTreeModified",
					},
					name = {
						trailing_slash = false,
						use_git_status_colors = true,
						highlight = "NeoTreeFileName",
					},
				},
				window = {
					position = "left",
					width = 35,
					mapping_options = {
						noremap = true,
						nowait = true,
					},
					mappings = {
						["/"] = "fuzzy_sorter",
						["<space>"] = { "toggle_node", nowait = false },
						["<space>"] = { "open", nowait = false },
					},
				},
				filesystem = {
					bind_to_cwd = true,
					follow_current_file = {
						enabled = true,
					},
					hijack_netrw_behavior = "open_default",
					use_libuv_file_watcher = true,
					filtered_items = {
						visible = false,
						show_hidden_count = true,
						hide_dotfiles = false,
						hide_gitignored = false,
						hide_by_name = {
							-- 'node_modules'
						},
						hide_by_pattern = {
							-- '*.env'
						},
						never_show = {
							-- '.DS_Store'
						},
					},
					window = {
						mappings = {
							["<leader>e"] = "close_window",
						},
					},
				},
				buffers = {
					follow_current_file = {
						enabled = true,
					},        -- This will find and focus the file in the active buffer every
					-- time the current file is changed while the tree is open.
					group_empty_dirs = true, -- when true, empty folders will be grouped together
					show_unloaded = true,
					window = {
						mappings = {
							["bd"] = "buffer_delete",
							["<bs>"] = "navigate_up",
							["."] = "set_root",
						},
					},
				},
				diagnostics = {
					auto_preview = {   -- May also be set to `true` or `false`
						enabled = false, -- Whether to automatically enable preview mode
						preview_config = {}, -- Config table to pass to auto preview (for example `{ use_float = true }`)
						event = "neo_tree_buffer_enter", -- The event to enable auto preview upon (for example `"neo_tree_window_after_open"`)
					},
					bind_to_cwd = true,
					diag_sort_function = "severity", -- "severity" means diagnostic items are sorted by severity in addition to their positions.
					-- "position" means diagnostic items are sorted strictly by their positions.
					-- May also be a function.
					follow_current_file = { -- May also be set to `true` or `false`
						enabled = true, -- This will find and focus the file in the active buffer every time
						always_focus_file = false, -- Focus the followed file, even when focus is currently on a diagnostic item belonging to that file
						expand_followed = true, -- Ensure the node of the followed file is expanded
						leave_dirs_open = false, -- `false` closes auto expanded dirs, such as with `:Neotree reveal`
						leave_files_open = false, -- `false` closes auto expanded files, such as with `:Neotree reveal`
					},
					group_dirs_and_files = true, -- when true, empty folders and files will be grouped together
					group_empty_dirs = true, -- when true, empty directories will be grouped together
					show_unloaded = true, -- show diagnostics from unloaded buffers
					refresh = {
						delay = 100,    -- Time (in ms) to wait before updating diagnostics. Might resolve some issues with Neovim hanging.
						event = "vim_diagnostic_changed", -- Event to use for updating diagnostics (for example `"neo_tree_buffer_enter"`)
						-- Set to `false` or `"none"` to disable automatic refreshing
						max_items = 10000, -- The maximum number of diagnostic items to attempt processing
						-- Set to `false` for no maximum
					},
					window = {
						position = "left",
						width = 40,
						mapping_options = {
							noremap = true,
							nowait = true,
						},
					},
				},
				git_status = {
					window = {
						position = "left",
						width = 40,
						mapping_options = {
							noremap = true,
							nowait = true,
						},
					},
				},
				event_handlers = {
					{
						event = "file_open_requested",
						handler = function()
							require("neo-tree.command").execute({ action = "close" })
						end,
					},
					{
						event = "neo_tree_buffer_enter",
						handler = function()
							vim.g["neo_tree_opened"] = true
							local hl = vim.api.nvim_get_hl_by_name("Cursor", true)
							hl.blend = 100
							vim.api.nvim_set_hl(0, "Cursor", hl)
							vim.opt.guicursor:append("a:Cursor/lCursor")
						end,
					},
					{
						event = "neo_tree_buffer_leave",
						handler = function()
							vim.g["neo_tree_opened"] = false
							local hl = vim.api.nvim_get_hl_by_name("Cursor", true)
							hl.blend = 0
							vim.api.nvim_set_hl(0, "Cursor", hl)
							vim.opt.guicursor:remove("a:Cursor/lCursor")
						end,
					},
				},
			})
		end,
	},
}
