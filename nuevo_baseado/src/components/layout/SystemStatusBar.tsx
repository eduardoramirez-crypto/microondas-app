import React from 'react'

export const SystemStatusBar: React.FC = () => {
  return (
    <div className="flex items-center space-x-4 text-sm">
      <div className="flex items-center space-x-2">
        <div className="status-online"></div>
        <span className="text-gray-300">Sistema Operativo</span>
      </div>
      
      <div className="text-gray-400">|</div>
      
      <div className="text-gray-300">
        <span className="text-fangio-blue font-medium">v2.1.0</span>
      </div>
      
      <div className="text-gray-400">|</div>
      
      <div className="text-gray-300">
        Última actualización: <span className="text-fangio-blue">Hoy</span>
      </div>
    </div>
  )
}
