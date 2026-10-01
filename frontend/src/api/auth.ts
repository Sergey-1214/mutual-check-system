const API_URL = '/api/v1/auth'

export type UserRole = 'student' | 'teacher'

export type CurrentUser = {
  id: number
  username: string
  email: string
  role: UserRole
}

type TokenResponse = {
  access_token: string
  token_type: string
  expires_in: number
}

export type RegisterData = {
  username: string
  email: string
  password: string
  role: UserRole
}

let accessToken: string | null = null
let restoreRequest: Promise<CurrentUser | null> | null = null

async function readResponse<T>(response: Response): Promise<T> {
  const data = await response.json().catch(() => null)

  if (!response.ok) {
    const detail = data?.detail
    const message = typeof detail === 'string'
      ? detail
      : Array.isArray(detail)
        ? detail[0]?.msg
        : null
    throw new Error(message || 'Не удалось выполнить запрос')
  }

  return data as T
}

async function loadUser(token: string) {
  const response = await fetch(`${API_URL}/me`, {
    credentials: 'include',
    headers: { Authorization: `Bearer ${token}` },
  })
  return readResponse<CurrentUser>(response)
}

async function acceptTokens(response: Response) {
  const tokens = await readResponse<TokenResponse>(response)
  accessToken = tokens.access_token
  return loadUser(tokens.access_token)
}

export async function login(email: string, password: string) {
  const response = await fetch(`${API_URL}/login`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ email, password }),
  })
  return acceptTokens(response)
}

export async function register(data: RegisterData) {
  const response = await fetch(`${API_URL}/register`, {
    method: 'POST',
    credentials: 'include',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  await readResponse<CurrentUser>(response)
  return login(data.email, data.password)
}

async function refreshSession() {
  const response = await fetch(`${API_URL}/refresh`, {
    method: 'POST',
    credentials: 'include',
  })

  if (response.status === 401) {
    accessToken = null
    return null
  }

  return acceptTokens(response)
}

export function restoreSession() {
  if (!restoreRequest) {
    restoreRequest = refreshSession().finally(() => {
      restoreRequest = null
    })
  }
  return restoreRequest
}

export async function logout() {
  try {
    await fetch(`${API_URL}/logout`, {
      method: 'POST',
      credentials: 'include',
    })
  } finally {
    accessToken = null
  }
}

export function getAccessToken() {
  return accessToken
}

export function pageForRole(role: UserRole) {
  return role === 'teacher' ? '/teacher/assignments' : '/assignments'
}
