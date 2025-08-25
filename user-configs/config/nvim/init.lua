-- Neovim
-- Options
vim.opt.number = true
vim.opt.relativenumber = true
vim.opt.wrap = true
vim.opt.linebreak = true
vim.opt.cursorline = true
vim.opt.cursorcolumn = true

-- Blinking Cursor
vim.opt.guicursor = "n-v-c-i:ver25-blinkon1"

-- Netrw
vim.keymap.set('n', '<C-e>', ':Lexplore<CR>', { noremap = true, silent = true })
vim.g.netrw_winsize = 10
vim.g.netrw_banner = 0


-- Settings
vim.opt.expandtab = true
vim.opt.shiftwidth = 4
vim.opt.tabstop = 4
vim.opt.smartindent = true
vim.opt.scrolloff = 10

-- Search
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- StatusLine
vim.opt.laststatus = 2
vim.cmd([[
    highlight StatusLine guibg=NONE guifg=NONE ctermbg=NONE ctermfg=NONE
    highlight StatusLineNC guibg=NONE guifg=NONE ctermbg=NONE ctermfg=NONE
]])

-- Force black background for all colorschemes
vim.api.nvim_create_autocmd("ColorScheme", {
  pattern = "*",
  callback = function()
    vim.api.nvim_set_hl(0, "Normal", { bg = "#000000" })
    vim.api.nvim_set_hl(0, "NormalFloat", { bg = "#000000" })
    vim.api.nvim_set_hl(0, "NormalNC", { bg = "#000000" })
  end,
})

-- Also set it immediately for the current session
vim.api.nvim_set_hl(0, "Normal", { bg = "#000000" })
vim.api.nvim_set_hl(0, "NormalFloat", { bg = "#000000" })
vim.api.nvim_set_hl(0, "NormalNC", { bg = "#000000" })
