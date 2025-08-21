return {
	"folke/snacks.nvim",
	priority = 1000,
	lazy = false,
	dependencies = {
		"folke/todo-comments.nvim",
		config = function()
			require("todo-comments").setup({})
		end,
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
						height = 0.4,
						position = "bottom",
						border = "top",
						title = " {title} {live} {flags}",
						title_pos = "left",
						{ win = "input", height = 1, border = "bottom" },
						{
							box = "horizontal",
							{ win = "list", border = "none" },
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
			"<leader>g",
			function()
				Snacks.picker.grep({})
			end,
			desc = "Grep",
		},
		{
			"<leader>G",
			function()
				Snacks.picker.grep_word({})
			end,
			desc = "Grep selection or word",
			mode = { "n", "v" },
		},
		{
			"<leader>gl",
			function()
				Snacks.picker.git_log({
					finder = "git_log",
					format = "git_log",
					preview = "git_show",
					confirm = "git_checkout",
					layout = "vertical",
				})
			end,
			desc = "Git log",
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
			"<leader>td",
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
	},
}
