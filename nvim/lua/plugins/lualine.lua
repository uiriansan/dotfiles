-- https://github.com/nvim-lualine/lualine.nvim/blob/master/examples/evil_lualine.lua

local colors = require("catppuccin.palettes").get_palette("mocha")
local mode_color = {
	n = colors.red,
	i = colors.green,
	v = colors.blue,
	[""] = colors.blue,
	V = colors.blue,
	c = colors.magenta,
	no = colors.red,
	s = colors.pink,
	S = colors.pink,
	ic = colors.yellow,
	R = colors.violet,
	Rv = colors.violet,
	cv = colors.red,
	ce = colors.red,
	r = colors.cyan,
	rm = colors.cyan,
	["r?"] = colors.cyan,
	["!"] = colors.red,
	t = colors.red,
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
	neo_tree_opened = function()
		return vim.g["neo_tree_opened"]
	end,
	neo_tree_closed = function()
		return not vim.g["neo_tree_opened"]
	end,
}

local config = {
	options = {
		component_separators = "",
		section_separators = "",
		globalstatus = true,
		theme = {
			normal = { c = { fg = colors.text, bg = "#0a0a0d" } }, -- colors.mantle
			inactive = { c = { fg = colors.text, bg = "#0a0a0d" } },
		},
	},
	sections = {
		-- remove defaults
		lualine_a = {},
		lualine_b = {},
		lualine_y = {},
		lualine_z = {},
		-- these will be filled later
		lualine_c = {},
		lualine_x = {},
	},
	inactive_sections = {
		-- remove defaults
		lualine_a = {},
		lualine_b = {},
		lualine_y = {},
		lualine_z = {},
		lualine_c = {},
		lualine_x = {},
	},
}

local function insert_left(component)
	table.insert(config.sections.lualine_c, component)
end

local function insert_right(component)
	table.insert(config.sections.lualine_x, component)
end

insert_left({
	"mode",
	fmt = function(res)
		return res:sub(1, 1)
	end,
	color = function()
		return { bg = mode_color[vim.fn.mode()], fg = colors.surface0 }
	end,
	padding = { right = 1, left = 1 },
})

insert_left({
	"branch",
	icon = "",
	color = { fg = colors.fg, bg = colors.bg, gui = "bold" },
	on_click = function()
		vim.cmd([[ Neotree git_status position=left ]])
	end,
})

insert_left({
	"diagnostics",
	sources = { "nvim_diagnostic" },
	section = { "error", "warn", "info" },
	symbols = { error = " ", warn = " ", info = " " },
	diagnostics_color = {
		color_error = { fg = colors.red },
		color_warn = { fg = colors.yellow },
		color_info = { fg = colors.cyan },
	},
	always_visible = false,
	on_click = function()
		vim.cmd([[ Trouble diagnostics toggle ]])
	end,
})

insert_left({
	"filename",
	file_status = true,
	symbols = {
		modified = "",
		readonly = "",
	},
	cond = conditions.neo_tree_closed,
	on_click = function()
		vim.cmd([[ Neotree ]])
	end,
})

-- insert_left({
-- 	function()
-- 		return "%="
-- 	end,
-- })

insert_right({
	function()
		local color = colors.text
		local msg = ""
		local buf_ft = vim.api.nvim_buf_get_option(0, "filetype")
		local buf_fn = vim.api.nvim_buf_get_name(0)
		local _, c = require("nvim-web-devicons").get_icon_color(buf_fn, buf_ft)
		color = c
		vim.cmd("hi! lualine_lsp_name guifg=" .. color .. " guibg=#000000")

		local clients = vim.lsp.get_active_clients()
		if next(clients) == nil then
			return msg
		end
		for _, client in ipairs(clients) do
			local filetypes = client.config.filetypes
			if filetypes and vim.fn.index(filetypes, buf_ft) ~= -1 then
				return client.name
			end
		end
		return msg
	end,
	color = "lualine_lsp_name",
})

insert_right({
	"o:encoding",
	fmt = string.upper,
	cond = conditions.hide_in_width,
})

insert_right({
	"filesize",
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
	icon = "󰒉",
	color = { fg = mode_color["v"] },
	cond = conditions.neo_tree_closed,
})

insert_right({
	"searchcount",
	icon = "",
	cond = conditions.neo_tree_closed,
})

insert_right({
	"location",
	color = { fg = colors.text },
	cond = conditions.buffer_not_empty and conditions.neo_tree_closed,
})

-- insert_right({
-- 	function()
-- 		local time = os.date("*t")
-- 		return "󰃮 "
-- 			.. string.format("%02d", time.day)
-- 			.. "/"
-- 			.. string.format("%02d", time.month)
-- 			.. "/"
-- 			.. time.year
-- 	end,
-- 	color = { fg = colors.text, gui = "bold" },
-- })

insert_right({
	function()
		local time = os.date("*t")
		return string.format("%02d", time.hour) .. ":" .. string.format("%02d", time.min)
	end,
	color = { fg = colors.green, gui = "bold" },
})

return {
	{
		"nvim-lualine/lualine.nvim",
		dependencies = {
			"nvim-tree/nvim-web-devicons",
		},
		config = config,
	},
}
