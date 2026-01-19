import React, { useState, useEffect } from 'react'
import { Outlet, useLocation } from 'react-router-dom'
import { motion, AnimatePresence } from 'framer-motion'
import { Menu, Settings, User, Bell } from 'lucide-react'

import { useAuth } from '@/hooks/useAuth'
import { Navigation } from './Navigation'
import { UserMenu } from './UserMenu'
import { SystemStatusBar } from './SystemStatusBar'
import { MobileNavigation } from './MobileNavigation'

export const Layout: React.FC = () => {
  const [sidebarOpen, setSidebarOpen] = useState(false)
  const [userMenuOpen, setUserMenuOpen] = useState(false)
  const location = useLocation()
  // const navigate = useNavigate()
  const { user, logout } = useAuth()

  // Close sidebar on route change
  useEffect(() => {
    setSidebarOpen(false)
  }, [location.pathname])

  const handleLogout = async () => {
    try {
      await logout()
    } catch (error) {
      console.error('Error during logout:', error)
    }
  }

  const navigationItems = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      path: '/dashboard',
      icon: 'BarChart3',
      description: 'Vista general del sistema',
    },
    {
      id: 'links',
      label: 'Enlaces PtP',
      path: '/links',
      icon: 'Network',
      description: 'Gestión de enlaces',
      badge: '12', // Dynamic count
    },
    {
      id: 'network-analysis',
      label: 'Análisis de Red',
      path: '/network-analysis',
      icon: 'Activity',
      description: 'Análisis y reportes',
    },
    {
      id: 'settings',
      label: 'Configuración',
      path: '/settings',
      icon: 'Settings',
      description: 'Ajustes del sistema',
    },
  ]

  return (
    <div className="min-h-screen bg-gradient-to-br from-fangio-dark via-gray-900 to-fangio-navy">
      {/* Mobile Navigation Overlay */}
      <AnimatePresence>
        {sidebarOpen && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="fixed inset-0 z-40 bg-black bg-opacity-50 lg:hidden"
            onClick={() => setSidebarOpen(false)}
          />
        )}
      </AnimatePresence>

      {/* Sidebar */}
      <motion.div
        initial={{ x: -100 }}
        animate={{ x: sidebarOpen ? 0 : -100 }}
        transition={{ type: 'spring', damping: 20 }}
        className={`fixed inset-y-0 left-0 z-50 w-64 bg-white/10 backdrop-blur-xl border-r border-white/20 lg:translate-x-0 lg:static lg:inset-0 ${
          sidebarOpen ? 'translate-x-0' : '-translate-x-full'
        }`}
      >
        <div className="flex h-full flex-col">
          {/* Logo */}
          <div className="flex h-16 shrink-0 items-center px-6">
            <div className="flex items-center space-x-3">
              <div className="h-8 w-8 rounded-lg bg-fangio-blue flex items-center justify-center">
                <span className="text-white font-bold text-lg">F</span>
              </div>
              <div>
                <h1 className="text-xl font-bold text-white">Fangio Telecom</h1>
                <p className="text-xs text-fangio-blue">Plataforma PtP</p>
              </div>
            </div>
          </div>

          {/* Navigation */}
          <Navigation items={navigationItems} />

          {/* User Section */}
          <div className="mt-auto p-6">
            <div className="rounded-lg bg-white/5 p-3">
              <div className="flex items-center space-x-3">
                <div className="h-8 w-8 rounded-full bg-fangio-blue flex items-center justify-center">
                  <User className="h-4 w-4 text-white" />
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-sm font-medium text-white truncate">
                    {user?.name || 'Usuario'}
                  </p>
                  <p className="text-xs text-gray-400 truncate">
                    {user?.role || 'Rol'}
                  </p>
                </div>
                <button
                  onClick={() => setUserMenuOpen(!userMenuOpen)}
                  className="text-gray-400 hover:text-white transition-colors"
                >
                  <Settings className="h-4 w-4" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </motion.div>

      {/* Main Content */}
      <div className="lg:pl-64">
        {/* Top Bar */}
        <div className="sticky top-0 z-30 bg-white/5 backdrop-blur-xl border-b border-white/20">
          <div className="flex h-16 items-center gap-x-4 px-4 sm:px-6 lg:px-8">
            {/* Mobile menu button */}
            <button
              type="button"
              className="-m-2.5 p-2.5 text-gray-400 lg:hidden"
              onClick={() => setSidebarOpen(true)}
            >
              <span className="sr-only">Abrir menú</span>
              <Menu className="h-6 w-6" />
            </button>

            {/* System Status Bar */}
            <div className="flex-1">
              <SystemStatusBar />
            </div>

            {/* Right side actions */}
            <div className="flex items-center gap-x-4">
              {/* Notifications */}
              <button className="p-2 text-gray-400 hover:text-white transition-colors">
                <Bell className="h-5 w-5" />
              </button>

              {/* User Menu */}
              <UserMenu
                user={user}
                isOpen={userMenuOpen}
                onToggle={() => setUserMenuOpen(!userMenuOpen)}
                onLogout={handleLogout}
              />
            </div>
          </div>
        </div>

        {/* Page Content */}
        <main className="py-6">
          <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
            <AnimatePresence mode="wait">
              <motion.div
                key={location.pathname}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                exit={{ opacity: 0, y: -20 }}
                transition={{ duration: 0.3 }}
              >
                <Outlet />
              </motion.div>
            </AnimatePresence>
          </div>
        </main>
      </div>

      {/* Mobile Navigation */}
      <MobileNavigation
        isOpen={sidebarOpen}
        onClose={() => setSidebarOpen(false)}
        navigationItems={navigationItems}
        user={user}
        onLogout={handleLogout}
      />
    </div>
  )
}
