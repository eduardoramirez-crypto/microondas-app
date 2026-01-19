import { useSelector, useDispatch } from 'react-redux'
import { useNavigate } from 'react-router-dom'
import { toast } from 'sonner'

import { RootState, AppDispatch } from '@/store'
import {
  loginUser,
  logoutUser,
  refreshUser,
  updateProfile,
  clearError,
} from '@/store/slices/authSlice'
import { User } from '@/types'

export const useAuth = () => {
  const dispatch = useDispatch<AppDispatch>()
  const navigate = useNavigate()

  const { user, isAuthenticated, isLoading, error } = useSelector(
    (state: RootState) => state.auth
  )

  const login = async (credentials: { email: string; password: string }) => {
    try {
      const result = await dispatch(loginUser(credentials)).unwrap()
      toast.success('Sesión iniciada correctamente')
      navigate('/dashboard')
      return result
    } catch (error) {
      toast.error(error as string)
      throw error
    }
  }

  const logout = async () => {
    try {
      await dispatch(logoutUser()).unwrap()
      toast.success('Sesión cerrada correctamente')
      navigate('/login')
    } catch (error) {
      toast.error('Error al cerrar sesión')
      // Force logout even if API fails
      dispatch(clearError())
      navigate('/login')
    }
  }

  const refresh = async () => {
    try {
      const result = await dispatch(refreshUser()).unwrap()
      return result
    } catch (error) {
      toast.error('Sesión expirada, por favor inicie sesión nuevamente')
      dispatch(clearError())
      navigate('/login')
      throw error
    }
  }

  const updateUserProfile = async (userData: Partial<User>) => {
    try {
      const result = await dispatch(updateProfile(userData)).unwrap()
      toast.success('Perfil actualizado correctamente')
      return result
    } catch (error) {
      toast.error(error as string)
      throw error
    }
  }

  const clearAuthError = () => {
    dispatch(clearError())
  }

  return {
    // State
    user,
    isAuthenticated,
    isLoading,
    error,

    // Actions
    login,
    logout,
    refresh,
    updateUserProfile,
    clearAuthError,

    // Computed
    isAdmin: user?.role === 'admin',
    isEngineer: user?.role === 'engineer',
    isViewer: user?.role === 'viewer',
  }
}
