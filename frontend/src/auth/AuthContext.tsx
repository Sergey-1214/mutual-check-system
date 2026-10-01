import { createContext, useContext, useEffect, useState, type ReactNode } from 'react'
import {
  login as loginRequest,
  logout as logoutRequest,
  register as registerRequest,
  restoreSession,
  type CurrentUser,
  type RegisterData,
} from '../api/auth'

type AuthContextValue = {
  user: CurrentUser | null
  loading: boolean
  login: (email: string, password: string) => Promise<CurrentUser>
  register: (data: RegisterData) => Promise<CurrentUser>
  logout: () => Promise<void>
}

const AuthContext = createContext<AuthContextValue | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [state, setState] = useState<{ user: CurrentUser | null; loading: boolean }>({
    user: null,
    loading: true,
  })

  useEffect(() => {
    restoreSession()
      .then((user) => setState({ user, loading: false }))
      .catch(() => setState({ user: null, loading: false }))
  }, [])

  async function login(email: string, password: string) {
    const user = await loginRequest(email, password)
    setState({ user, loading: false })
    return user
  }

  async function register(data: RegisterData) {
    const user = await registerRequest(data)
    setState({ user, loading: false })
    return user
  }

  async function logout() {
    await logoutRequest()
    setState({ user: null, loading: false })
  }

  return (
    <AuthContext.Provider value={{ ...state, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  )
}

// oxlint-disable-next-line react/only-export-components
// oxlint-disable-next-line react/only-export-components
export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) throw new Error('useAuth должен использоваться внутри AuthProvider')
  return context
}
