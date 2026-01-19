import React from 'react'
import { Link } from 'react-router-dom'

export const NotFoundPage: React.FC = () => {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-fangio-dark via-gray-900 to-fangio-navy">
      <div className="text-center">
        <h1 className="text-6xl font-bold text-fangio-blue">404</h1>
        <h2 className="text-2xl font-semibold text-white mt-4">Página no encontrada</h2>
        <p className="text-gray-400 mt-2">La página que buscas no existe</p>
        <Link to="/dashboard" className="btn-primary mt-6 inline-block">
          Volver al Dashboard
        </Link>
      </div>
    </div>
  )
}
