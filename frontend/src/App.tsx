import { BrowserRouter, Navigate, Route, Routes, useLocation } from 'react-router-dom'
import { Box, CircularProgress } from '@mui/material'
import Layout from './components/Layout'
import { pageForRole } from './api/auth'
import { AuthProvider, useAuth } from './auth/AuthContext'
import HomePage from './pages/HomePage'
import AssignmentsPage from './pages/AssignmentsPage'
import AssignmentPage from './pages/AssignmentPage'
import ReviewsPage from './pages/ReviewsPage'
import ReviewPage from './pages/ReviewPage'
import TeacherAssignmentsPage from './pages/TeacherAssignmentsPage'
import TeacherAssignmentPage from './pages/TeacherAssignmentPage'
import CreateAssignmentPage from './pages/CreateAssignmentPage'
import GroupsPage from './pages/GroupsPage'
import GroupPage from './pages/GroupPage'
import CreateGroupPage from './pages/CreateGroupPage'
import LoginPage from './pages/LoginPage'
import RegisterPage from './pages/RegisterPage'

function MainRoutes() {
  const { pathname } = useLocation()
  const { user, loading } = useAuth()

  if (loading) {
    return <Box sx={{ minHeight: '100vh', display: 'grid', placeItems: 'center' }}><CircularProgress /></Box>
  }
  if (!user && pathname !== '/') return <Navigate to="/login" replace />
  if (user?.role === 'student' && pathname.startsWith('/teacher')) {
    return <Navigate to="/assignments" replace />
  }
  if (user?.role === 'teacher' && ['/assignments', '/groups', '/reviews'].some((path) => pathname === path || pathname.startsWith(`${path}/`))) {
    return <Navigate to="/teacher/assignments" replace />
  }

  return (
    <Layout>
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/assignments" element={<AssignmentsPage />} />
        <Route path="/assignments/:id" element={<AssignmentPage />} />
        <Route path="/groups" element={<GroupsPage />} />
        <Route path="/groups/:id" element={<GroupPage />} />
        <Route path="/reviews" element={<ReviewsPage />} />
        <Route path="/reviews/:id" element={<ReviewPage />} />
        <Route path="/teacher/assignments" element={<TeacherAssignmentsPage />} />
        <Route path="/teacher/assignments/new" element={<CreateAssignmentPage />} />
        <Route path="/teacher/assignments/:id" element={<TeacherAssignmentPage />} />
        <Route path="/teacher/groups" element={<GroupsPage teacher />} />
        <Route path="/teacher/groups/new" element={<CreateGroupPage />} />
        <Route path="/teacher/groups/:id" element={<GroupPage teacher />} />
        <Route path="*" element={<Navigate to={user ? pageForRole(user.role) : '/'} replace />} />
      </Routes>
    </Layout>
  )
}

function App() {
  return (
    <AuthProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/login" element={<LoginPage />} />
          <Route path="/register" element={<RegisterPage />} />
          <Route path="*" element={<MainRoutes />} />
        </Routes>
      </BrowserRouter>
    </AuthProvider>
  )
}

export default App
