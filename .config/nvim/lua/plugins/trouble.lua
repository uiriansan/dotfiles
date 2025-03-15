return {
	"folke/trouble.nvim",
	opts = {
		auto_close = false,
		auto_open = false,
		auto_preview = true,
		auto_refresh = true,
		auto_jump = false,
		focus = true,
		restore = true,
		follow = true,
		indent_guides = true,
		max_items = 200,
		multiline = false,
		pinned = false,
		warn_no_results = false,
		open_no_results = true,
		win = {
			title = "Trouble",
			size = 12,
		},
		modes = {
			diagnostics = {
				sort = { "severity", "filename", "pos", "message" },
				format =
				"{severity_icon}{severity}: {message:md} {item.source} {code} {hl:TroubleDiagnosticsPos}{pos}",
			}
		},
		keys = {
			["?"] = "help",
			r = "refresh",
			R = "toggle_refresh",
			q = "close",
			o = "jump_close",
			["<esc>"] = "cancel",
			["<cr>"] = "jump",
			["<2-leftmouse>"] = "jump",
			["<c-s>"] = "jump_split",
			["<c-v>"] = "jump_vsplit",
			j = "next",
			["}"] = "next",
			["]]"] = "next",
			k = "prev",
			["{"] = "prev",
			["[["] = "prev",
			dd = "delete",
			d = { action = "delete", mode = "v" },
			i = "inspect",
			p = "preview",
			P = "toggle_preview",
			zo = "fold_open",
			zO = "fold_open_recursive",
			zc = "fold_close",
			zC = "fold_close_recursive",
			za = "fold_toggle",
			zA = "fold_toggle_recursive",
			zm = "fold_more",
			zM = "fold_close_all",
			zr = "fold_reduce",
			zR = "fold_open_all",
			zx = "fold_update",
			zX = "fold_update_all",
			zn = "fold_disable",
			zN = "fold_enable",
			zi = "fold_toggle_enable",
			gb = { -- example of a custom action that toggles the active view filter
				action = function(view)
					view:filter({ buf = 0 }, { toggle = true })
				end,
				desc = "Toggle Current Buffer Filter",
			},
			s = { -- example of a custom action that toggles the severity
				action = function(view)
					local f = view:get_filter("severity")
					local severity = ((f and f.filter.severity or 0) + 1) % 5
					view:filter({ severity = severity }, {
						id = "severity",
						template = "{hl:Title}Filter:{hl} {severity}",
						del = severity == 0,
					})
				end,
				desc = "Toggle Severity Filter",
			},
		},
	},
	cmd = "Trouble",
	keys = {
		{
			"<leader>t",
			"<cmd>Trouble diagnostics toggle<cr>",
			desc = "Toggle Trouble",
		},
		{
			"<leader>Tb",
			"<cmd>Trouble diagnostics toggle filter.buf=0<cr>",
			desc = "Buffer Diagnostics (Trouble)",
		},
		{
			"<leader>Ts",
			"<cmd>Trouble symbols toggle focus=true win.position=left win.size=35<cr>",
			desc = "Buffer symbols",
		},
		{
			"<leader>Tl",
			"<cmd>Trouble lsp toggle focus=false win.position=right<cr>",
			desc = "LSP Definitions / references / ... (Trouble)",
		},
		{
			"<leader>TL",
			"<cmd>Trouble loclist toggle<cr>",
			desc = "Location List (Trouble)",
		},
		{
			"<leader>Tq",
			"<cmd>Trouble qflist toggle<cr>",
			desc = "Quickfix List (Trouble)",
		},
	},
}
