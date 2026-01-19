import React from 'react'

export const DashboardPage: React.FC = () => {
  return (
    <div className="space-y-6">
      <div className="text-center">
        <h1 className="text-3xl font-bold text-white">Dashboard</h1>
        <p className="text-gray-400">Vista general del sistema</p>
      </div>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <div className="card">
          <h3 className="text-lg font-semibold text-white">Enlaces Totales</h3>
          <p className="text-3xl font-bold text-fangio-blue">0</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-white">Enlaces Viables</h3>
          <p className="text-3xl font-bold text-secondary-500">0</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-white">Enlaces No Viables</h3>
          <p className="text-3xl font-bold text-red-500">0</p>
        </div>
        
        <div className="card">
          <h3 className="text-lg font-semibold text-white">Análisis Realizados</h3>
          <p className="text-3xl font-bold text-accent-500">0</p>
        </div>
      </div>
    </div>
  )
}
