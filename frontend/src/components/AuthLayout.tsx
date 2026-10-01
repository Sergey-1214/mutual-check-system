import type { ReactNode } from 'react'
import { Avatar, Box, Chip, Paper, Typography } from '@mui/material'
import { Link } from 'react-router-dom'

type AuthLayoutProps = {
  title: string
  subtitle: string
  children: ReactNode
}

function AuthLayout({ title, subtitle, children }: AuthLayoutProps) {
  return (
    <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center', px: 2, py: 5, position: 'relative', overflow: 'hidden' }}>
      <Box sx={{ position: 'absolute', width: 480, height: 480, borderRadius: '50%', background: 'radial-gradient(circle, rgba(114,230,196,.12), transparent 68%)', left: '-12%', top: '-24%' }} />
      <Box sx={{ position: 'absolute', width: 430, height: 430, borderRadius: '50%', background: 'radial-gradient(circle, rgba(167,139,250,.11), transparent 68%)', right: '-10%', bottom: '-25%' }} />

      <Box sx={{ width: 'min(440px, 100%)', position: 'relative' }}>
        <Box component={Link} to="/" sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1.25, mb: 3, color: 'text.primary', textDecoration: 'none' }}>
          <Avatar variant="rounded" sx={{ width: 42, height: 42, bgcolor: 'primary.main', color: 'primary.contrastText', fontFamily: 'ui-monospace, monospace', fontWeight: 900, boxShadow: '0 0 28px rgba(114,230,196,.2)' }}>P</Avatar>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 850, lineHeight: 1.05 }}>PeerReview</Typography>
            <Typography variant="caption" sx={{ color: 'text.secondary', fontFamily: 'ui-monospace, monospace', letterSpacing: '.08em', textTransform: 'uppercase' }}>learn · review · grow</Typography>
          </Box>
        </Box>

        <Paper elevation={0} sx={{ bgcolor: 'rgba(21,27,35,.94)', border: '1px solid', borderColor: 'divider', borderRadius: 4, p: { xs: 2.5, sm: 4 }, boxShadow: '0 28px 70px rgba(0,0,0,.32)', backdropFilter: 'blur(16px)' }}>
          <Chip label="Система взаимных проверок" size="small" sx={{ mb: 2, bgcolor: 'rgba(114,230,196,.1)', color: 'primary.light', border: '1px solid rgba(114,230,196,.2)' }} />
          <Typography variant="h4" component="h1" sx={{ fontWeight: 850, letterSpacing: '-0.035em' }}>{title}</Typography>
          <Typography color="text.secondary" sx={{ mt: 1, mb: 3 }}>{subtitle}</Typography>
          {children}
        </Paper>
      </Box>
    </Box>
  )
}

export default AuthLayout
