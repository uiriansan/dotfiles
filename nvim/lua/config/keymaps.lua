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
