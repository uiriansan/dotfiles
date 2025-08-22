return {
	"folke/snacks.nvim",
	priority = 1000,
	lazy = false,
	dependencies = {
		{
			"folke/todo-comments.nvim",
			config = function()
				require("todo-comments").setup({})
			end,
		},
	},
	---@type snacks.Config
	opts = {
		-- your configuration comes here
		-- or leave it empty to use the default settings
		-- refer to the configuration section below
		bigfile = { enabled = true },
		dashboard = { enabled = true },
		explorer = { enabled = false },
		indent = { enabled = true },
		input = { enabled = true },
		image = { enabled = true },
		lazygit = {
			enabled = true,
			configure = true,
		},
		picker = {
			enabled = true,
			layout = {
				preset = "ivy_split",
			},
			layouts = {
				ivy_split = {
					layout = {
						box = "vertical",
						backdrop = false,
						width = 0,
						height = 0.5,
						position = "bottom",
						border = "top",
						title = " {title} {live} {flags}",
						title_pos = "left",
						{ win = "input", height = 1, border = "bottom" },
						{
							box = "horizontal",
							{ win = "list",    border = "none" },
							{ win = "preview", title = "{preview}", width = 0.6, border = "left" },
						},
					},
				},
			},
			matcher = {
				filename_bonus = true, -- give bonus for matching file names (last part of the path)
				cwd_bonus = false, -- give bonus for matching files in the cwd
				frecency = true,
			},
			previewers = {
				diff = {
					builtin = true, -- use Neovim for previewing diffs (true) or use an external tool (false)
					cmd = { "delta" }, -- example to show a diff with delta
				},
				git = {
					builtin = true, -- use Neovim for previewing git output (true) or use git (false)
					args = {}, -- additional arguments passed to the git command. Useful to set pager options usin `-c ...`
				},
				file = {
					max_size = 1024 * 1024, -- 1MB
					max_line_length = 500, -- max line length
					ft = nil, ---@type string? filetype for highlighting. Use `nil` for auto detect
				},
			},
			win = {
				input = {
					keys = {
						["<Esc>"] = { "close", mode = { "n", "i" } },
					},
				},
			},
		},
		notifier = { enabled = true },
		quickfile = { enabled = true },
		scope = { enabled = true },
		scroll = { enabled = true },
		statuscolumn = { enabled = true },
		words = { enabled = true },
		terminal = {
			enabled = true,
			shell = "fish",
			start_insert = false,
			win = {
				{
					bo = {
						filetype = "snacks_terminal",
					},
					wo = {},
					keys = {
						q = "hide",
						["<leader>`"] = "hide",
						gf = function(self)
							local f = vim.fn.findfile(vim.fn.expand("<cfile>"), "**")
							if f == "" then
								Snacks.notify.warn("No file under cursor")
							else
								self:hide()
								vim.schedule(function()
									vim.cmd("e " .. f)
								end)
							end
						end,
						term_normal = {
							"<esc>",
							function(self)
								if vim.fn.mode() == "i" then

								end
								self.esc_timer = self.esc_timer or (vim.uv or vim.loop).new_timer()
								if self.esc_timer:is_active() then
									self.esc_timer:stop()
									vim.cmd("stopinsert")
								else
									self.esc_timer:start(200, 0, function() end)
									Snacks.terminal.hide()
									return "<esc>"
								end
							end,
							mode = "t",
							expr = true,
							desc = "Double escape to normal mode",
						},
					},
				}
			}
		}
	},
	keys = {
		{
			"<leader><space>",
			function()
				Snacks.picker.buffers({
					on_show = function()
						vim.cmd.stopinsert()
					end,
					hidden = false,
					unloaded = true,
					current = true,
					sort_lastused = true,
					win = {
						input = {
							keys = {
								["<c-x>"] = { "bufdelete", mode = { "n", "i" } },
							},
						},
						list = { keys = { ["dd"] = { "bufdelete", mode = { "n" } } } },
					},
				})
			end,
			desc = "Navigate opened buffers",
		},
		{
			"<leader>f",
			function()
				Snacks.picker.files({
					show_empty = true,
					supports_live = true,
				})
			end,
			desc = "Find files",
		},
		{
			"<leader>r",
			function()
				Snacks.picker.recent({})
			end,
			desc = "Browse recent files",
		},
		{
			"<leader>p",
			function()
				Snacks.picker.projects({})
			end,
			desc = "Browse recent projects",
		},
		{
			"<leader>s",
			function()
				Snacks.picker.grep({})
			end,
			desc = "Grep",
		},
		{
			"<leader>S",
			function()
				Snacks.picker.grep_word({})
			end,
			desc = "Grep selection or word",
			mode = { "n", "v" },
		},
		{
			"<leader>gL",
			function()
				Snacks.picker.git_log({
					finder = "git_log",
					format = "git_log",
					preview = "git_show",
					confirm = "git_checkout",
				})
			end,
			desc = "Browse Git logs",
		},
		{
			"<leader>;",
			function()
				Snacks.picker.diagnostics()
			end,
			desc = "Open diagnostics",
		},

		{
			"<leader>?",
			function()
				Snacks.picker.keymaps({
					layout = "vertical",
				})
			end,
			desc = "Show keymaps",
		},
		{
			"<leader>m",
			function()
				Snacks.picker.man({})
			end,
			desc = "Browse ManPages",
		},
		{
			"<leader>y",
			function()
				Snacks.picker.cliphist()
			end,
			desc = "Browse clipboard history",
		},
		{
			"<leader>t",
			function()
				Snacks.picker.todo_comments({
					keywords = { "TODO", "WARNING", "WARN", "BUG", "NOTE", "INFO", "FIX", "FIXME", "ERROR" },
					no_status = true,
				})
				vim.schedule(function()
					local input = require("snacks.picker.core.input")
					local statuscolumn = input.statuscolumn
					input.statuscolumn = function(self)
						if self.picker.opts.no_status == true then
							return " "
						else
							return statuscolumn(self)
						end
					end
				end)
			end,
			desc = "Browse TODOs",
		},
		-- {
		-- 	"<leader>`",
		-- 	function()
		-- 		Snacks.terminal.toggle()
		-- 	end,
		-- 	desc = "Toggle terminal"
		-- }
	},
}
