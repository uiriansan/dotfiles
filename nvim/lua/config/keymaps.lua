-- Clear highlights on search when pressing <Esc> in normal mode
--  See `:help hlsearch`
vim.keymap.set("n", "<Esc>", "<cmd>nohlsearch<CR>")

-- Diagnostic keymaps
-- vim.keymap.set("n", "<leader>q", vim.diagnostic.setloclist, { desc = "Open diagnostic [Q]uickfix list" })

-- Exit terminal mode in the builtin terminal with a shortcut that is a bit easier
-- for people to discover. Otherwise, you normally need to press <C-\><C-n>, which
-- is not what someone will guess without a bit more experience.
--
-- NOTE: This won't work in all terminal emulators/tmux/etc. Try your own mapping
-- or just use <C-\><C-n> to exit terminal mode
vim.keymap.set("t", "<Esc><Esc>", "<C-\\><C-n>", { desc = "Exit terminal mode" })

-- Keybinds to make split navigation easier.
--  Use CTRL+<hjkl> to switch between windows
--
--  See `:help wincmd` for a list of all window commands
vim.keymap.set("n", "<M-h>", "<C-w><M-h>", { desc = "Move focus to the left window" })
vim.keymap.set("n", "<M-l>", "<C-w><M-l>", { desc = "Move focus to the right window" })
vim.keymap.set("n", "<M-j>", "<C-w><M-j>", { desc = "Move focus to the lower window" })
vim.keymap.set("n", "<M-k>", "<C-w><M-k>", { desc = "Move focus to the upper window" })
vim.keymap.set("n", "<M-Left>", "<C-w><M-h>", { desc = "Move focus to the left window" })
vim.keymap.set("n", "<M-Right>", "<C-w><M-l>", { desc = "Move focus to the right window" })
vim.keymap.set("n", "<M-Down>", "<C-w><M-j>", { desc = "Move focus to the lower window" })
vim.keymap.set("n", "<M-Up>", "<C-w><M-k>", { desc = "Move focus to the upper window" })

-- Splits
vim.keymap.set("n", "<M-h>", "<cmd>split<CR>", { desc = "Split window horizontally" })
vim.keymap.set("n", "<M-v>", "<cmd>vsplit<CR>", { desc = "Split window vertically" })
vim.keymap.set("n", "<M-w>", "<cmd>close<CR>", { desc = "Close split" })

-- cokeline.nvim
vim.keymap.set("n", "<C-q>", "<Plug>(cokeline-focus-prev)", { desc = "Previous buffer" })
vim.keymap.set("n", "<C-e>", "<Plug>(cokeline-focus-next)", { desc = "Next buffer" })
vim.keymap.set("n", "<C-w>", "<cmd>bn<bar>sp<bar>bp<bar>bd<CR>", { desc = "Close buffer" })
