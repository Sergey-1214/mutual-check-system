import { createTheme } from '@mui/material/styles'

const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#72E6C4',
      dark: '#48B99A',
      light: '#A2F1DA',
      contrastText: '#07120F',
    },
    secondary: {
      main: '#A78BFA',
      dark: '#8065D8',
      light: '#C5B5FF',
      contrastText: '#100D18',
    },
    success: {
      main: '#57D3A0',
      dark: '#36A97B',
      light: '#8BE4BF',
    },
    warning: {
      main: '#F3B35E',
      dark: '#CA8738',
      light: '#FFD08D',
    },
    error: { main: '#FF7A8A' },
    background: {
      default: '#0D1117',
      paper: '#151B23',
    },
    text: {
      primary: '#EDF6F3',
      secondary: '#9DAEA9',
    },
    divider: '#29343D',
  },
  shape: {
    borderRadius: 14,
  },
  typography: {
    fontFamily: 'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    h1: { fontWeight: 800, letterSpacing: '-0.04em' },
    h2: { fontWeight: 800, letterSpacing: '-0.035em' },
    h3: { fontWeight: 800, letterSpacing: '-0.03em' },
    h4: { fontWeight: 800, letterSpacing: '-0.025em' },
    button: { textTransform: 'none', fontWeight: 750 },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 999,
          paddingInline: 18,
          boxShadow: 'none',
        },
        contained: {
          boxShadow: '0 8px 24px rgba(15, 88, 71, .25)',
          '&:hover': { boxShadow: '0 10px 30px rgba(57, 177, 145, .28)' },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { borderRadius: 999, fontWeight: 700 },
      },
    },
    MuiTextField: {
      defaultProps: { variant: 'outlined' },
    },
    MuiOutlinedInput: {
      styleOverrides: {
        root: {
          backgroundColor: '#10161D',
          '& fieldset': { borderColor: '#34424D' },
          '&:hover fieldset': { borderColor: '#52636F' },
        },
      },
    },
    MuiLinearProgress: {
      styleOverrides: {
        root: { backgroundColor: '#26343A' },
      },
    },
    MuiCssBaseline: {
      styleOverrides: {
        body: { colorScheme: 'dark' },
      },
    },
  },
})

export default theme
