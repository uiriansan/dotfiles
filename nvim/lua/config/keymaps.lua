local map = vim.keymap.set

-- Disable arrows in every mode
map("n", "<Up>", ":echoe 'Get off my lawn!'<CR>")
map("n", "<Down>", ":echoe 'Get off my lawn!'<CR>")
map("n", "<Left>", ":echoe 'Get off my lawn!'<CR>")
map("n", "<Right>", ":echoe 'Get off my lawn!'<CR>")
map("i", "<Up>", "<C-o>:echoe 'Get off my lawn!'<CR>")
map("i", "<Down>", "<C-o>:echoe 'Get off my lawn!'<CR>")
map("i", "<Left>", "<C-o>:echoe 'Get off my lawn!'<CR>")
map("i", "<Right>", "<C-o>:echoe 'Get off my lawn!'<CR>")
map("v", "<Up>", ":<C-u>echoe 'Get off my lawn!'<CR>")
map("v", "<Down>", ":<C-u>echoe 'Get off my lawn!'<CR>")
map("v", "<Left>", ":<C-u>echoe 'Get off my lawn!'<CR>")
map("v", "<Right>", ":<C-u>echoe 'Get off my lawn!'<CR>")

-- Disable command history
map("n", "q:", "<nop>", { desc = "Disable command history" })

map("n", "<leader>L", "<cmd>Lazy<CR>", { desc = "Open Lazy" })
map("n", "<leader>M", "<cmd>Mason<CR>", { desc = "Open Mason" })

vim.api.nvim_create_autocmd("LspAttach", {
	group = vim.api.nvim_create_augroup("UserLspConfig", {}),
	callback = function(ev)
		-- Buffer local mappings.
		-- See `:help vim.lsp.*` for documentation on any of the below functions
		local opts = { buffer = ev.buf, silent = true }

		-- set keybinds
		opts.desc = "Show LSP references"
		map("n", "gr", function() Snacks.picker.lsp_references() end, opts) -- show definition, references

		opts.desc = "Go to declaration"
		map("n", "gD", vim.lsp.buf.declaration, opts) -- go to declaration

		opts.desc = "Show LSP definitions"
		map("n", "gd", function() Snacks.picker.lsp_definitions() end, opts) -- show lsp definitions

		opts.desc = "Show LSP implementations"
		map("n", "gi", function() Snacks.picker.lsp_implementations() end, opts) -- show lsp implementations

		opts.desc = "Show LSP type definitions"
		map("n", "gt", function() Snacks.picker.lsp_type_definitions() end, opts) -- show lsp type definitions

		opts.desc = "See available code actions"
		map({ "n", "v" }, "<C-space>", vim.lsp.buf.code_action, opts) -- see available code actions, in visual mode will apply to selection

		opts.desc = "Smart rename"
		map("n", "<leader>lr", vim.lsp.buf.rename, opts) -- smart rename

		opts.desc = "Show line diagnostics"
		map("n", "<Tab>", vim.diagnostic.open_float, opts) -- show diagnostics for line

		opts.desc = "Go to previous diagnostic"
		map("n", "[d", vim.diagnostic.goto_prev, opts) -- jump to previous diagnostic in buffer

		opts.desc = "Go to next diagnostic"
		map("n", "]d", vim.diagnostic.goto_next, opts) -- jump to next diagnostic in buffer

		opts.desc = "Show documentation for what is under cursor"
		map("n", "K", vim.lsp.buf.hover, opts) -- show documentation for what is under cursor

		opts.desc = "Show LSP symbols"
		map("n", "<leader>o", function() Snacks.picker.lsp_symbols() end, opts)
	end,
})

-- Clear search highlight with Escape
map('n', '<Esc>', function() vim.cmd('noh') end, { desc = "Clear search highlight with Escape " })
map("n", "<leader>n", ":ene<CR>", { desc = "Create new file" })
