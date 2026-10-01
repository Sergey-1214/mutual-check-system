import type { ReactNode } from 'react'
import { Avatar, Box, Button, Typography } from '@mui/material'
import { Link, useLocation, useNavigate } from 'react-router-dom'
import { useAuth } from '../auth/AuthContext'

const links = [
  ['Главная', '/'],
  ['Мои работы', '/assignments'],
  ['Мои группы', '/groups'],
  ['Мои проверки', '/reviews'],
  ['Управление заданиями', '/teacher/assignments'],
  ['Управление группами', '/teacher/groups'],
]

function Layout({ children }: { children: ReactNode }) {
  const { pathname } = useLocation()
  const navigate = useNavigate()
  const { user, logout } = useAuth()
  const visibleLinks = user?.role === 'teacher'
    ? links.filter(([, path]) => path === '/' || path.startsWith('/teacher'))
    : links.filter(([, path]) => !path.startsWith('/teacher'))

  async function handleLogout() {
    await logout()
    navigate('/login', { replace: true })
  }

  return (
    <Box sx={{ minHeight: '100vh', color: 'text.primary' }}>
      <Box component="header" sx={{ position: 'relative', overflow: 'hidden', bgcolor: '#090D12', color: 'text.primary', borderBottom: '1px solid', borderColor: 'rgba(114,230,196,.18)' }}>
        <Box sx={{ position: 'absolute', width: 280, height: 280, borderRadius: '50%', background: 'radial-gradient(circle, rgba(114,230,196,.13), transparent 68%)', right: '6%', top: -190 }} />
        <Box sx={{ position: 'absolute', width: 180, height: 1, bgcolor: 'rgba(167,139,250,.45)', right: '2%', bottom: 12, transform: 'rotate(-12deg)' }} />
        <Box sx={{ position: 'relative', width: 'min(1100px, calc(100% - 32px))', mx: 'auto', py: 1.75, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1.25 }}>
            <Avatar variant="rounded" sx={{ width: 38, height: 38, bgcolor: 'primary.main', color: 'primary.contrastText', fontFamily: 'ui-monospace, monospace', fontWeight: 900, boxShadow: '0 0 24px rgba(114,230,196,.22)' }}>P</Avatar>
            <Box>
              <Typography variant="h6" sx={{ fontWeight: 800, lineHeight: 1.1 }}>PeerReview</Typography>
              <Typography variant="caption" sx={{ color: 'text.secondary', fontFamily: 'ui-monospace, monospace', letterSpacing: '.08em', textTransform: 'uppercase' }}>learn · review · grow</Typography>
            </Box>
          </Box>
          {user ? (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Box sx={{ textAlign: 'right', display: { xs: 'none', sm: 'block' } }}>
                <Typography variant="body2" sx={{ fontWeight: 750 }}>{user.username}</Typography>
                <Typography variant="caption" color="text.secondary">{user.role === 'teacher' ? 'Преподаватель' : 'Студент'}</Typography>
              </Box>
              <Avatar sx={{ width: 38, height: 38, bgcolor: 'rgba(167,139,250,.16)', color: 'secondary.light', border: '1px solid rgba(167,139,250,.35)', fontSize: 13, fontWeight: 800 }}>{user.username.trim().slice(0, 2).toUpperCase()}</Avatar>
              <Button onClick={handleLogout} size="small" color="inherit" sx={{ color: 'text.secondary' }}>Выйти</Button>
            </Box>
          ) : (
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button component={Link} to="/login" color="inherit">Войти</Button>
              <Button component={Link} to="/register" variant="contained">Регистрация</Button>
            </Box>
          )}
        </Box>
      </Box>

      {user && <Box component="nav" sx={{ bgcolor: 'rgba(13,17,23,.88)', borderBottom: '1px solid', borderColor: 'divider', backdropFilter: 'blur(14px)', position: 'sticky', top: 0, zIndex: 10 }}>
        <Box sx={{ width: 'min(1100px, calc(100% - 16px))', mx: 'auto', display: 'flex', gap: 0.75, py: 1, overflowX: 'auto' }}>
          {visibleLinks.map(([label, path]) => {
            const active = path === '/' ? pathname === '/' : pathname === path || pathname.startsWith(`${path}/`)
            return (
              <Button key={path} component={Link} to={path} variant={active ? 'contained' : 'text'} size="small" sx={{ whiteSpace: 'nowrap', color: active ? 'primary.contrastText' : 'text.secondary' }}>
                {label}
              </Button>
            )
          })}
        </Box>
      </Box>}

      <Box component="main" sx={{ width: 'min(1000px, calc(100% - 32px))', mx: 'auto', py: { xs: 3, md: 5 } }}>
        {children}
      </Box>
    </Box>
  )
}

export default Layout
