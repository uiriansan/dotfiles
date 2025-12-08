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
				cwd_bonus = true, -- give bonus for matching files in the cwd
				frecency = true,
				sort_empty = true,
				history_bonus = true,
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
	},
	keys = {
		{
			"<leader><space>",
			function()
				Snacks.picker.smart({
					-- on_show = function()
					-- 	vim.cmd.stopinsert()
					-- end,
					multi = {
						{
							source = "buffers",
							current = false,
						},
					},
					matcher = {
						sort_empty = false,
					},
					win = {
						input = {
							keys = {
								["<c-x>"] = { "bufdelete", mode = { "n", "i" } },
							},
						},
					},
				})
			end,
			desc = "Navigate opened buffers",
			mode = "n",
		},
		{
			"<leader>f",
			function()
				Snacks.picker.files({
					show_empty = true,
					hidden = true,
					supports_live = true,
					ignored = true,
				})
			end,
			desc = "Find files",
			mode = "n",
		},
		{
			"<leader>r",
			function()
				Snacks.picker.recent({})
			end,
			desc = "Browse recent files",
			mode = "n",
		},
		{
			"<leader>p",
			function()
				Snacks.picker.projects({})
			end,
			desc = "Browse recent projects",
			mode = "n",
		},
		{
			"<leader>s",
			function()
				Snacks.picker.grep({})
			end,
			desc = "Grep",
			mode = "n",
		},
		{
			"<leader>S",
			function()
				Snacks.picker.grep_word({})
			end,
			desc = "Grep selection or word",
			mode = { "n", "v" },
			mode = "n",
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
			mode = "n",
		},
		{
			"<leader><Tab>",
			function()
				Snacks.picker.diagnostics()
			end,
			desc = "Open diagnostics",
			mode = "n",
		},

		{
			"<leader>?",
			function()
				Snacks.picker.keymaps({
					layout = "select",
				})
			end,
			desc = "Show keymaps",
			mode = "n",
		},
		{
			"<leader>m",
			function()
				Snacks.picker.man({})
			end,
			desc = "Browse ManPages",
			mode = "n",
		},
		{
			"\"",
			function()
				Snacks.picker.cliphist({
					layout = "select"
				})
			end,
			desc = "Browse clipboard history",
			mode = "n",
		},
		{
			"<leader>t",
			function()
				Snacks.picker.todo_comments({
					keywords = { "TODO", "WARNING", "WARN", "BUG", "NOTE", "INFO", "FIX", "FIXME", "ERROR" },
					no_status = true,
				})
				-- vim.schedule(function()
				-- 	local input = require("snacks.picker.core.input")
				-- 	local statuscolumn = input.statuscolumn
				-- 	input.statuscolumn = function(self)
				-- 		if self.picker.opts.no_status == true then
				-- 			return " "
				-- 		else
				-- 			return statuscolumn(self)
				-- 		end
				-- 	end
				-- end)
			end,
			desc = "Browse TODOs",
			mode = "n",
		},
	},
}
