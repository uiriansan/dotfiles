local lsp_list = {
	"lua_ls",
	"clangd",
	"pyright",
	"rust-analyzer",
	"html",
	"cssls",
	"ts_ls",
	"jsonls",
	"svelte",
	"tailwindcss",
	"gopls",
}

return {
	"williamboman/mason.nvim",
	dependencies = {
		"williamboman/mason-lspconfig.nvim",
		{
			"neovim/nvim-lspconfig",
			config = function()
				vim.lsp.config("*", {})

				vim.lsp.enable(lsp_list)
			end,
		},
	},
	config = function()
		local mason = require("mason")
		local mason_lspconfig = require("mason-lspconfig")

		mason.setup({
			ui = {
				icons = {
					package_installed = "✓",
					package_pending = "➜",
					package_uninstalled = "✗",
				},
			},
		})

		mason_lspconfig.setup({
			ensure_installed = lsp_list,
			automatic_installation = true, -- install servers locally automatically
		})
	end,
}
