import { useState, type FormEvent } from 'react'
import { Alert, Box, Button, CircularProgress, Link as MuiLink, TextField, Typography } from '@mui/material'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { pageForRole } from '../api/auth'
import { useAuth } from '../auth/AuthContext'
import AuthLayout from '../components/AuthLayout'

function LoginPage() {
  const navigate = useNavigate()
  const { user, loading, login } = useAuth()
  const [request, setRequest] = useState({ loading: false, error: '' })

  if (loading) {
    return <AuthLayout title="Вход" subtitle="Проверяем текущую сессию…"><Box sx={{ display: 'grid', placeItems: 'center', py: 4 }}><CircularProgress /></Box></AuthLayout>
  }
  if (user) return <Navigate to={pageForRole(user.role)} replace />

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    setRequest({ loading: true, error: '' })

    try {
      const result = await login(String(form.get('email')), String(form.get('password')))
      navigate(pageForRole(result.role), { replace: true })
    } catch (error) {
      setRequest({ loading: false, error: error instanceof Error ? error.message : 'Не удалось войти' })
    }
  }

  return (
    <AuthLayout title="Вход" subtitle="Войдите, чтобы перейти к заданиям и проверкам.">
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'grid', gap: 2 }}>
        {request.error && <Alert severity="error">{request.error}</Alert>}
        <TextField name="email" label="Электронная почта" type="email" autoComplete="email" required fullWidth />
        <TextField name="password" label="Пароль" type="password" autoComplete="current-password" required fullWidth />
        <Button type="submit" variant="contained" size="large" disabled={request.loading} sx={{ mt: 0.5 }}>
          {request.loading ? 'Входим…' : 'Войти'}
        </Button>
        <Typography color="text.secondary" variant="body2" sx={{ textAlign: 'center' }}>
          Ещё нет аккаунта?{' '}
          <MuiLink component={Link} to="/register" color="primary.main" underline="hover">Зарегистрироваться</MuiLink>
        </Typography>
      </Box>
    </AuthLayout>
  )
}

export default LoginPage
