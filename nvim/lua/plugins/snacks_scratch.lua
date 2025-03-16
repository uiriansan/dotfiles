return {
	"folke/snacks.nvim",
	---@type snacks.Config
	opts = {
		scratch = {
			enabled = true,
		},
	},
	keys = {
		{ "<leader>s", function() Snacks.scratch() end,        desc = "Toggle Scratch Buffer" },
		{ "<leader>S", function() Snacks.scratch.select() end, desc = "Select Scratch Buffer" },
	}
}
