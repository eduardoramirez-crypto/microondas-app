import React from 'react'
import { User } from '@/types'

interface MobileNavigationProps {
  isOpen: boolean
  onClose: () => void
  navigationItems: any[]
  user: User | null
  onLogout: () => void
}

export const MobileNavigation: React.FC<MobileNavigationProps> = ({
  isOpen,
  onClose,
  // navigationItems,
  // user,
  onLogout,
}) => {
  if (!isOpen) return null

  return (
    <div className="fixed inset-0 z-50 lg:hidden">
      <div className="fixed inset-0 bg-black bg-opacity-50" onClick={onClose} />
      
      <div className="fixed inset-y-0 left-0 w-64 bg-white/10 backdrop-blur-xl border-r border-white/20">
        <div className="flex h-full flex-col">
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
          
          <div className="flex-1 px-3 py-4">
            <p className="text-gray-400 text-sm px-3 py-2">Navegación móvil</p>
          </div>
          
          <div className="p-6">
            <button
              onClick={onLogout}
              className="w-full btn-outline"
            >
              Cerrar Sesión
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
