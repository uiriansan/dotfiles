-- Autoformat
return {
	{
		"stevearc/conform.nvim",
		event = { "BufWritePre" },
		cmd = { "ConformInfo" },
		opts = {
			notify_on_error = true,
			format_on_save = function(bufnr)
				-- Disable "format_on_save lsp_fallback" for languages that don't
				-- have a well standardized coding style. You can add additional
				-- languages here or re-enable it for the disabled ones.
				local disable_filetypes = {}
				return {
					timeout_ms = 500,
					lsp_fallback = not disable_filetypes[vim.bo[bufnr].filetype],
				}
			end,
			formatters_by_ft = {
				lua = { "stylua" },
				python = { "isort", "black" },
				rust = { "rustfmt", lsp_format = "fallback" },
				javascript = { "prettierd", "prettier", stop_after_first = true },
				typescript = { 'prettier', name = 'dprint', timeout_ms = 500, lsp_format = 'fallback' },
				c = { "clang_format" },
				cpp = { "clang_format" },
				h = { "clang_format" },
				hpp = { "clang_format" },
				-- Conform can also run multiple formatters sequentially
				-- python = { "isort", "black" },
				--
				-- You can use 'stop_after_first' to run the first available formatter from the list
				-- javascript = { "prettierd", "prettier", stop_after_first = true },
			},
			formatters = {
				clang_format = {
					-- Create a link of ~/.config/nvim/.clang-format in $HOME so that clangd-formatter fallsback to it in case a project-level format file isn't provided
					prepend_args = { '--style=file', '--fallback-style=LLVM' },
				},
			},
		},
	},
}
