import React from 'react'
import { User } from '@/types'

interface UserMenuProps {
  user: User | null
  isOpen: boolean
  onToggle: () => void
  onLogout: () => void
}

export const UserMenu: React.FC<UserMenuProps> = ({
  user,
  isOpen,
  onToggle,
  onLogout,
}) => {
  return (
    <div className="relative">
      <button
        onClick={onToggle}
        className="flex items-center space-x-3 text-gray-300 hover:text-white transition-colors"
      >
        <div className="h-8 w-8 rounded-full bg-fangio-blue flex items-center justify-center">
          <span className="text-white text-sm font-medium">
            {user?.name?.charAt(0) || 'U'}
          </span>
        </div>
      </button>

      {isOpen && (
        <div className="absolute right-0 mt-2 w-48 bg-white/10 backdrop-blur-xl border border-white/20 rounded-lg shadow-lg">
          <div className="py-1">
            <button
              onClick={onLogout}
              className="block w-full text-left px-4 py-2 text-sm text-white hover:bg-white/10 transition-colors"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      )}
    </div>
  )
}
