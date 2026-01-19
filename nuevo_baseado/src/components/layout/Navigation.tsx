import React from 'react'
import { NavLink } from 'react-router-dom'
import { LucideIcon, BarChart3, Network, Activity, Settings } from 'lucide-react'

interface NavigationItem {
  id: string
  label: string
  path: string
  icon: string
  description: string
  badge?: string | number
}

interface NavigationProps {
  items: NavigationItem[]
}

const iconMap: Record<string, LucideIcon> = {
  BarChart3,
  Network,
  Activity,
  Settings,
}

export const Navigation: React.FC<NavigationProps> = ({ items }) => {
  return (
    <nav className="flex-1 space-y-1 px-3 py-4">
      {items.map((item) => {
        const Icon = iconMap[item.icon]
        return (
          <NavLink
            key={item.id}
            to={item.path}
            className={({ isActive }) =>
              `nav-item ${isActive ? 'nav-item-active' : 'nav-item-inactive'}`
            }
          >
            {Icon && <Icon className="h-5 w-5 mr-3" />}
            <div className="flex-1">
              <span className="text-sm font-medium">{item.label}</span>
              {item.badge && (
                <span className="ml-auto inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-fangio-blue/20 text-fangio-blue">
                  {item.badge}
                </span>
              )}
            </div>
          </NavLink>
        )
      })}
    </nav>
  )
}
