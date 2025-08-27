-- https://github.com/nvim-lualine/lualine.nvim/blob/master/examples/evil_lualine.lua

local colors = require("kanso.colors").setup({ theme = "zen" }).palette
local custom_kanso = require("lualine.themes.kanso")

custom_kanso.normal.c.bg = colors.zenBg2

local mode_color = {
	["n"] = { bg = colors.red2, fg = colors.zenBg0 },
	["i"] = { bg = colors.green, fg = colors.zenBg0 },
	["v"] = { bg = colors.blue, fg = colors.zenBg0 },
	[""] = { bg = colors.blue, fg = colors.zenBg0 },
	["V"] = { bg = colors.blue, fg = colors.zenBg0 },
	["c"] = { bg = colors.pink, fg = colors.zenBg0 },
	["no"] = { bg = colors.red2, fg = colors.zenBg0 },
	["s"] = { bg = colors.pink, fg = colors.zenBg0 },
	["S"] = { bg = colors.pink, fg = colors.zenBg0 },
	["ic"] = { bg = colors.green, fg = colors.zenBg0 },
	["R"] = { bg = colors.aqua, fg = colors.zenBg0 },
	["Rv"] = { bg = colors.aqua, fg = colors.zenBg0 },
	["cv"] = { bg = colors.pink, fg = colors.zenBg0 },
	["ce"] = { bg = colors.pink, fg = colors.zenBg0 },
	["r"] = { bg = colors.aqua, fg = colors.zenBg0 },
	["rm"] = { bg = colors.aqua, fg = colors.zenBg0 },
	["r?"] = { bg = colors.aqua, fg = colors.zenBg0 },
	["!"] = { bg = colors.red2, fg = colors.zenBg0 },
	["t"] = { bg = colors.red2, fg = colors.zenBg0 },
}

local conditions = {
	buffer_not_empty = function()
		return vim.fn.empty(vim.fn.expand("%:t")) ~= 1
	end,
	hide_in_width = function()
		return vim.fn.winwidth(0) > 80
	end,
	check_git_workspace = function()
		local filepath = vim.fn.expand("%:p:h")
		local gitdir = vim.fn.finddir(".git", filepath .. ";")
		return gitdir and #gitdir > 0 and #gitdir < #filepath
	end,
}

local config = {
	options = {
		theme = custom_kanso,
		component_separators = "",
		section_separators = "",
		globalstatus = false,
		section = false,
		disabled_filetypes = {
			winbar = {
				"snacks_dashboard",
				"toggleterm",
			},
		},
	},
	winbar = {
		-- remove defaults
		lualine_a = {},
		lualine_b = {},
		lualine_y = {},
		lualine_z = {},
		-- these will be filled later
		lualine_c = {},
		lualine_x = {},
	},
	inactive_winbar = {
		-- remove defaults
		lualine_a = {},
		lualine_b = {},
		lualine_y = {},
		lualine_z = {},
		lualine_c = {},
		lualine_x = {},
	},
	sections = {},
	inactive_sections = {},
}

local function insert_left(component)
	table.insert(config.winbar.lualine_c, component)
end

local function insert_right(component)
	table.insert(config.winbar.lualine_x, component)
end

insert_left({
	"mode",
	fmt = function(res)
		return res:sub(1, 1)
	end,
	color = function()
		local mode = vim.fn.mode()
		return { bg = mode_color[mode].bg, fg = mode_color[mode].fg, }
	end,
	padding = { right = 1, left = 1 },
})

insert_left({
	function()
		local cwd = vim.fn.getcwd():match("[^/\\]+$")
		return (vim.b.branch_name ~= nil and vim.b.branch_name ~= "") and " " .. vim.b.branch_name or " " .. cwd
	end,
	color = { fg = colors.fg, gui = "bold" },
	on_click = function()
		require("snacks").lazygit()
	end,
	padding = { right = 0, left = 1 },
	draw_empty = false,
})

insert_left({
	function()
		local bufs = vim.api.nvim_list_bufs()
		local c = 0
		for i, b in ipairs(bufs) do
			if vim.bo[b].buflisted then
				c = c + 1
			end
		end

		return c > 1 and "[" .. c .. "]" or ""
	end,
	padding = { right = 0, left = 1 },
	draw_empty = false,
})

insert_left({
	function()
		local buf = vim.api.nvim_get_current_buf()
		local buf_name = vim.api.nvim_buf_get_name(buf)
		local filename = buf_name:match("[^/\\]+$")
		local buf_ro = vim.bo[buf].readonly
		local buf_mod = vim.bo[buf].modified

		local str = ""
		str = str .. (filename ~= "" and filename or "[No name]")
		if buf_ro then
			str = str .. " "
		elseif buf_mod then
			str = str .. " "
		end
		return str
	end,
	-- cond = conditions.neo_tree_closed,
	on_click = function()
		require("snacks").picker.buffers({
			on_show = function()
				vim.cmd.stopinsert()
			end,
			hidden = false,
			unloaded = true,
			current = true,
			sort_lastused = true,
			matcher = {
				sort_empty = false,
			},
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
	padding = { right = 0, left = 1 },
	color = { fg = colors.fg2 },
	draw_empty = false,
})

-- insert_left({
-- 	function()
-- 		return "%="
-- 	end,
-- })

insert_right({
	function()
		local errors = vim.diagnostic.get(nil, { severity = { min = vim.diagnostic.severity.ERROR } })
		local e_count = 0
		for _, error in ipairs(errors) do
			local buf = vim.api.nvim_buf_get_name(error.bufnr)
			local buf_dir = vim.fn.fnamemodify(buf, ":h")

			if buf_dir:sub(1, #vim.fn.getcwd()) == vim.fn.getcwd() then
				e_count = e_count + 1
			end
		end
		return (e_count and e_count > 0) and e_count or ""
	end,
	icon = "",
	update_in_insert = true,
	padding = { right = 1 },
	color = { fg = colors.red2 },
	draw_empty = false,
	on_click = function()
		require("snacks").picker.diagnostics()
	end,
})

insert_right({
	function()
		local warns = vim.diagnostic.get(nil,
			{ severity = { min = vim.diagnostic.severity.WARN, max = vim.diagnostic.severity.WARN } })
		local w_count = 0
		for _, warn in ipairs(warns) do
			local buf = vim.api.nvim_buf_get_name(warn.bufnr)
			local buf_dir = vim.fn.fnamemodify(buf, ":h")

			if buf_dir:sub(1, #vim.fn.getcwd()) == vim.fn.getcwd() then
				w_count = w_count + 1
			end
		end
		return (w_count and w_count > 0) and w_count or ""
	end,
	icon = "",
	update_in_insert = true,
	padding = { right = 1 },
	color = { fg = colors.yellow },
	draw_empty = false,
	on_click = function()
		require("snacks").picker.diagnostics()
	end,
})

insert_right({
	function()
		local clients = vim.lsp.get_clients({ bufnr = 0 })
		if next(clients) ~= nil then
			for i, client in ipairs(clients) do
				if client.name ~= nil and client.name ~= "" then
					return client.name
				end
			end
		end
		return ""
	end,
	color = { fg = colors.gray },
	padding = { right = 1, left = 0 },
	draw_empty = false,
})

insert_right({
	function()
		local isVisualMode = vim.fn.mode():find("[Vv]")
		if not isVisualMode then
			return ""
		end
		local starts = vim.fn.line("v")
		local ends = vim.fn.line(".")
		local lines = starts <= ends and ends - starts + 1 or starts - ends + 1
		return "L:" .. tostring(lines) .. " C:" .. tostring(vim.fn.wordcount().visual_chars)
	end,
	icon = "",
	padding = { right = 1, left = 0 },
	draw_empty = false,
	color = { fg = mode_color["v"].bg },
})

insert_right({
	"searchcount",
	icon = "",
	padding = { right = 1, left = 0 },
	draw_empty = false,
	color = { fg = mode_color["c"].bg },
})

insert_right({
	function()
		local cur = vim.fn.line(".")
		local tot = vim.fn.line("$")
		return require("lualine.utils.utils").stl_escape(string.format("%d%%", cur / tot * 100))
	end,
	padding = { right = 1, left = 0 },
	draw_empty = false,
})

return {
	{
		"nvim-lualine/lualine.nvim",
		dependencies = {
			"nvim-tree/nvim-web-devicons",
		},
		config = function()
			require("lualine").setup(config)
		end,
	},
}
