import { User } from '@/types'

// Mock service - TODO: Implementar con API real
export const authService = {
  async login(credentials: { email: string; password: string }): Promise<{ data: User }> {
    // Simular delay de API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    // Mock user data
    const mockUser: User = {
      id: '1',
      email: credentials.email,
      name: 'Usuario Demo',
      role: 'engineer',
      lastLogin: new Date(),
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    
    return { data: mockUser }
  },

  async logout(): Promise<void> {
    // Simular delay de API
    await new Promise(resolve => setTimeout(resolve, 500))
    // TODO: Implementar logout real
  },

  async refresh(): Promise<{ data: User }> {
    // Simular delay de API
    await new Promise(resolve => setTimeout(resolve, 500))
    
    const mockUser: User = {
      id: '1',
      email: 'usuario@demo.com',
      name: 'Usuario Demo',
      role: 'engineer',
      lastLogin: new Date(),
      createdAt: new Date(),
      updatedAt: new Date(),
    }
    
    return { data: mockUser }
  },

  async updateProfile(userData: Partial<User>): Promise<{ data: User }> {
    // Simular delay de API
    await new Promise(resolve => setTimeout(resolve, 1000))
    
    const mockUser: User = {
      id: '1',
      email: 'usuario@demo.com',
      name: 'Usuario Demo',
      role: 'engineer',
      lastLogin: new Date(),
      createdAt: new Date(),
      updatedAt: new Date(),
      ...userData,
    }
    
    return { data: mockUser }
  },
}
