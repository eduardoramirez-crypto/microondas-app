# 🚀 Fangio Telecom - Plataforma PtP Profesional

> Plataforma empresarial para la gestión y análisis de enlaces Point-to-Point (PtP) con capacidades avanzadas de planificación de radioenlaces.

[![React](https://img.shields.io/badge/React-18.2.0-blue.svg)](https://reactjs.org/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.2.2-blue.svg)](https://www.typescriptlang.org/)
[![Vite](https://img.shields.io/badge/Vite-5.0.0-purple.svg)](https://vitejs.dev/)
[![Tailwind CSS](https://img.shields.io/badge/Tailwind-3.3.6-38B2AC.svg)](https://tailwindcss.com/)
[![Redux Toolkit](https://img.shields.io/badge/Redux%20Toolkit-1.9.7-purple.svg)](https://redux-toolkit.js.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## ✨ Características Principales

- 🔐 **Autenticación Profesional** - Sistema de login seguro con JWT
- 📊 **Dashboard Interactivo** - Métricas en tiempo real y visualizaciones
- 🔗 **Gestión de Enlaces PtP** - CRUD completo con validaciones
- 📡 **Análisis de Red** - Algoritmos avanzados de factibilidad
- 🗺️ **Visualización de Mapas** - Integración con Leaflet para análisis geográfico
- 📈 **Reportes y Exportación** - Múltiples formatos (Excel, PDF, CSV)
- 🎨 **UI/UX Moderna** - Diseño responsive con Tailwind CSS y Framer Motion
- 🔧 **Configuración Avanzada** - Personalización del sistema
- 📱 **Responsive Design** - Optimizado para todos los dispositivos
- 🚀 **Performance Optimizado** - Lazy loading y code splitting

## 🛠️ Stack Tecnológico

### Frontend
- **React 18** - Biblioteca de interfaz de usuario
- **TypeScript** - Tipado estático para mayor robustez
- **Vite** - Build tool ultra-rápido
- **Tailwind CSS** - Framework CSS utility-first
- **Framer Motion** - Animaciones fluidas y profesionales

### State Management
- **Redux Toolkit** - Gestión de estado global
- **Redux Persist** - Persistencia de datos
- **React Query** - Gestión de estado del servidor

### Routing & Navigation
- **React Router v6** - Enrutamiento declarativo
- **Protected Routes** - Sistema de autenticación

### UI Components
- **Lucide React** - Iconografía moderna
- **Sonner** - Notificaciones elegantes
- **Recharts** - Gráficos interactivos
- **React Leaflet** - Mapas interactivos

### Development Tools
- **ESLint** - Linting de código
- **Prettier** - Formateo automático
- **Husky** - Git hooks
- **Vitest** - Testing framework

## 🚀 Instalación y Configuración

### Prerrequisitos
- **Node.js** >= 18.0.0
- **npm** >= 9.0.0
- **Git**

### Instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/fangio-telecom/ptp-platform.git
   cd ptp-platform
   ```

2. **Instalar dependencias**
   ```bash
   npm install
   ```

3. **Configurar variables de entorno**
   ```bash
   cp .env.example .env.local
   # Editar .env.local con tus configuraciones
   ```

4. **Ejecutar en modo desarrollo**
   ```bash
   npm run dev
   ```

5. **Abrir en el navegador**
   ```
   http://localhost:3000
   ```

### Scripts Disponibles

```bash
# Desarrollo
npm run dev          # Servidor de desarrollo
npm run build        # Build de producción
npm run preview      # Preview del build

# Calidad de código
npm run lint         # Ejecutar ESLint
npm run lint:fix     # Corregir errores automáticamente
npm run format       # Formatear con Prettier
npm run type-check   # Verificar tipos TypeScript

# Testing
npm run test         # Ejecutar tests
npm run test:ui      # Interfaz de testing
npm run test:coverage # Reporte de cobertura
```

## 📁 Estructura del Proyecto

```
src/
├── components/          # Componentes reutilizables
│   ├── auth/           # Componentes de autenticación
│   ├── layout/         # Componentes de layout
│   ├── forms/          # Formularios
│   ├── tables/         # Tablas de datos
│   └── ui/             # Componentes de UI básicos
├── hooks/              # Hooks personalizados
├── pages/              # Páginas de la aplicación
├── services/           # Servicios de API
├── store/              # Store de Redux
│   └── slices/         # Slices de Redux
├── types/              # Definiciones de tipos TypeScript
├── utils/              # Utilidades y helpers
├── styles/             # Estilos globales
└── App.tsx             # Componente principal
```

## 🔧 Configuración

### Variables de Entorno

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:8000/api
VITE_API_TIMEOUT=10000

# Authentication
VITE_JWT_SECRET=your-jwt-secret
VITE_REFRESH_TOKEN_EXPIRY=7d

# Application
VITE_APP_NAME=Fangio Telecom PtP
VITE_APP_VERSION=2.1.0
VITE_APP_ENVIRONMENT=development

# External Services
VITE_MAPBOX_TOKEN=your-mapbox-token
VITE_GOOGLE_ANALYTICS_ID=your-ga-id
```

### Configuración de Tailwind

El proyecto incluye una configuración personalizada de Tailwind CSS con:

- Paleta de colores personalizada para Fangio Telecom
- Componentes predefinidos (botones, cards, inputs)
- Animaciones y transiciones personalizadas
- Soporte para glassmorphism y efectos modernos

## 📊 Características Técnicas

### Performance
- **Code Splitting** automático por rutas
- **Lazy Loading** de componentes
- **Memoización** con React.memo y useMemo
- **Bundle Analysis** integrado

### Seguridad
- **JWT Authentication** con refresh tokens
- **Protected Routes** basadas en roles
- **Input Validation** con Zod
- **XSS Protection** integrada

### Testing
- **Unit Tests** con Vitest
- **Component Testing** con React Testing Library
- **E2E Tests** con Playwright (opcional)
- **Coverage Reports** automáticos

### CI/CD
- **GitHub Actions** para automatización
- **Linting** y **Type Checking** automáticos
- **Build** y **Deploy** automatizados
- **Quality Gates** integrados

## 🎨 Diseño y UX

### Principios de Diseño
- **Glassmorphism** para efectos modernos
- **Micro-interacciones** para mejor engagement
- **Responsive Design** mobile-first
- **Accessibility** (WCAG 2.1 AA)

### Sistema de Colores
- **Primary**: Azul Fangio (#00e6ff)
- **Secondary**: Verde éxito (#10b981)
- **Accent**: Naranja (#f59e42)
- **Neutral**: Escala de grises profesional

### Tipografía
- **Inter** para texto de interfaz
- **JetBrains Mono** para código
- **Sistema de escalas** consistente

## 📱 Responsive Design

El proyecto está optimizado para todos los dispositivos:

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px
- **Large Desktop**: > 1440px

## 🔌 API Integration

### Endpoints Principales

```typescript
// Authentication
POST /api/auth/login
POST /api/auth/logout
POST /api/auth/refresh
GET  /api/auth/profile

// Links Management
GET    /api/links
POST   /api/links
PUT    /api/links/:id
DELETE /api/links/:id

// Network Analysis
POST /api/analysis/same-transport
POST /api/analysis/frequency-planning
GET  /api/analysis/:id/report
```

### Interceptors

- **Request Interceptors**: Añadir tokens de autenticación
- **Response Interceptors**: Manejo de errores global
- **Error Handling**: Retry automático para errores 5xx

## 🚀 Deployment

### Build de Producción

```bash
npm run build
```

### Servidores Soportados

- **Vercel** (recomendado)
- **Netlify**
- **AWS S3 + CloudFront**
- **Docker** (incluido)

### Docker

```bash
# Build de la imagen
docker build -t fangio-ptp .

# Ejecutar contenedor
docker run -p 3000:3000 fangio-ptp
```

## 🤝 Contribución

### Guía de Contribución

1. **Fork** el proyecto
2. **Crear** una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. **Commit** tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. **Push** a la rama (`git push origin feature/AmazingFeature`)
5. **Abrir** un Pull Request

### Estándares de Código

- **TypeScript** estricto
- **ESLint** + **Prettier** para consistencia
- **Conventional Commits** para mensajes
- **Testing** obligatorio para nuevas features

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

## 🆘 Soporte

### Documentación
- [Guía de Usuario](docs/user-guide.md)
- [API Reference](docs/api-reference.md)
- [Component Library](docs/components.md)

### Contacto
- **Email**: soporte@fangio.com.mx
- **Website**: [https://fangio.com.mx](https://fangio.com.mx)
- **Issues**: [GitHub Issues](https://github.com/fangio-telecom/ptp-platform/issues)

### Comunidad
- **Discord**: [Fangio Telecom Community](https://discord.gg/fangio)
- **Blog**: [Blog Técnico](https://blog.fangio.com.mx)

## 🙏 Agradecimientos

- **React Team** por el framework increíble
- **Vite Team** por el build tool ultra-rápido
- **Tailwind CSS** por el sistema de diseño
- **Comunidad Open Source** por las librerías

---

**Desarrollado con ❤️ por el equipo de Fangio Telecom**

*Transformando la conectividad, un enlace a la vez.* 