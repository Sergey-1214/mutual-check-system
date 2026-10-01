import { useState, type FormEvent } from 'react'
import { Alert, Box, Button, CircularProgress, Link as MuiLink, MenuItem, TextField, Typography } from '@mui/material'
import { Link, Navigate, useNavigate } from 'react-router-dom'
import { pageForRole, type UserRole } from '../api/auth'
import { useAuth } from '../auth/AuthContext'
import AuthLayout from '../components/AuthLayout'

function RegisterPage() {
  const navigate = useNavigate()
  const { user, loading, register } = useAuth()
  const [request, setRequest] = useState({ loading: false, error: '' })

  if (loading) {
    return <AuthLayout title="Регистрация" subtitle="Проверяем текущую сессию…"><Box sx={{ display: 'grid', placeItems: 'center', py: 4 }}><CircularProgress /></Box></AuthLayout>
  }
  if (user) return <Navigate to={pageForRole(user.role)} replace />

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault()
    const form = new FormData(event.currentTarget)
    setRequest({ loading: true, error: '' })

    try {
      const result = await register({
        username: String(form.get('username')),
        email: String(form.get('email')),
        password: String(form.get('password')),
        role: String(form.get('role')) as UserRole,
      })
      navigate(pageForRole(result.role), { replace: true })
    } catch (error) {
      setRequest({ loading: false, error: error instanceof Error ? error.message : 'Не удалось зарегистрироваться' })
    }
  }

  return (
    <AuthLayout title="Регистрация" subtitle="Создайте аккаунт студента или преподавателя.">
      <Box component="form" onSubmit={handleSubmit} sx={{ display: 'grid', gap: 2 }}>
        {request.error && <Alert severity="error">{request.error}</Alert>}
        <TextField name="username" label="Имя" autoComplete="name" required fullWidth slotProps={{ htmlInput: { minLength: 3, maxLength: 100 } }} />
        <TextField name="email" label="Электронная почта" type="email" autoComplete="email" required fullWidth />
        <TextField name="password" label="Пароль" type="password" autoComplete="new-password" helperText="Не менее 8 символов" required fullWidth slotProps={{ htmlInput: { minLength: 8, maxLength: 128 } }} />
        <TextField name="role" select label="Роль" defaultValue="student" helperText="Преподаватель создаёт группы и задания" required fullWidth>
          <MenuItem value="student">Студент</MenuItem>
          <MenuItem value="teacher">Преподаватель</MenuItem>
        </TextField>
        <Button type="submit" variant="contained" size="large" disabled={request.loading} sx={{ mt: 0.5 }}>
          {request.loading ? 'Создаём аккаунт…' : 'Создать аккаунт'}
        </Button>
        <Typography color="text.secondary" variant="body2" sx={{ textAlign: 'center' }}>
          Уже есть аккаунт?{' '}
          <MuiLink component={Link} to="/login" color="primary.main" underline="hover">Войти</MuiLink>
        </Typography>
      </Box>
    </AuthLayout>
  )
}

export default RegisterPage
