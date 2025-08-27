return {
	'vyfor/cord.nvim',
	build = ':Cord update',
	opts = function()
		local git_branch = vim.fn.system('git branch --show-current'):gsub('\n', '')

		return {
			timestamp = {
				enabled = false,
			},
			idle = {
				smart_idle = true,
				ignore_focus = false,
			},
			variables = {
				git_status = function()
					return ' [' .. 'git:' .. git_branch .. ']'
				end,
				lsps = function()
					local clients = vim.lsp.get_clients()
					if next(clients) ~= nil then
						local str = ""
						for i, client in ipairs(clients) do
							if i >= 3 then
								break
							end

							str = str .. " | " .. client.name
						end
						return str
					end
					return ""
				end,
				lines = function()
					return ' (' .. vim.api.nvim_buf_line_count(0) .. ' lines)'
				end,
			},
			text = {
				editing = function(opt)
					return string.format("Editing %s %s", opt.filename, opt.lines())
				end,
				workspace = function(opt)
					return string.format('%s%s', opt.workspace, opt.git_status())
				end,
				terminal = "Compiling project..."
			},
			hooks = {
				workspace_change = function()
					git_branch = vim.fn.system('git branch --show-current'):gsub('\n', '')
				end,
				post_activity = function(_, activity)
					local version = vim.version()
					activity.assets.small_text = string.format('Neovim %s.%s.%s', version.major, version.minor, version
						.patch)
				end,
			},
			buttons = {
				{
					label = function(opt)
						return opt.repo_url and 'View Repository' or 'Website'
					end,
					url = function(opt)
						return opt.repo_url or 'https://github.com/uiriansan'
					end
				}
			},
		}
	end,
}
