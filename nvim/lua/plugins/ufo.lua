return {
	"kevinhwang91/nvim-ufo",
	dependencies = { 'kevinhwang91/promise-async' },

	config = function()
		require("ufo").setup({
			open_fold_hl_timeout = 0,
			enable_get_fold_virt_text = true,
			provider_selector = function(_, filetype)
				return { 'treesitter', 'indent' }
			end,
			fold_virt_text_handler = function(virtText, lnum, endLnum, width, truncate, ctx)
				-- include the bottom line in folded text for additional context
				local suffix = (' 󰁂 %s '):format(endLnum - lnum)
				local sufWidth = vim.fn.strdisplaywidth(suffix)
				local targetWidth = width - sufWidth
				local curWidth = 0
				table.insert(virtText, { suffix, 'Folded' })
				local endVirtText = ctx.get_fold_virt_text(endLnum)
				for i, chunk in ipairs(endVirtText) do
					local chunkText = chunk[1]
					local hlGroup = chunk[2]
					if i == 1 then
						chunkText = chunkText:gsub("^%s+", "")
					end
					local chunkWidth = vim.fn.strdisplaywidth(chunkText)
					if targetWidth > curWidth + chunkWidth then
						table.insert(virtText, { chunkText, hlGroup })
					else
						chunkText = truncate(chunkText, targetWidth - curWidth)
						table.insert(virtText, { chunkText, hlGroup })
						chunkWidth = vim.fn.strdisplaywidth(chunkText)
						-- str width returned from truncate() may less than 2nd argument, need padding
						if curWidth + chunkWidth < targetWidth then
							suffix = suffix .. (' '):rep(targetWidth - curWidth - chunkWidth)
						end
						break
					end
					curWidth = curWidth + chunkWidth
				end
				return virtText
			end,
		})

		vim.o.foldcolumn = '1' -- '0' is not bad
		vim.o.foldlevel = 99 -- Using ufo provider need a large value, feel free to decrease the value
		vim.o.foldlevelstart = 99
		vim.o.foldenable = true

		-- Using ufo provider need remap `zR` and `zM`. If Neovim is 0.6.1, remap yourself
		vim.keymap.set('n', 'zR', require('ufo').openAllFolds)
		vim.keymap.set('n', 'zM', require('ufo').closeAllFolds)
	end,
}
