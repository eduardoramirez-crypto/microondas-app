// User and Authentication Types
export interface User {
  id: string
  email: string
  name: string
  role: UserRole
  avatar?: string
  lastLogin: Date
  createdAt: Date
  updatedAt: Date
}

export type UserRole = 'admin' | 'engineer' | 'viewer'

export interface AuthState {
  user: User | null
  isAuthenticated: boolean
  isLoading: boolean
  error: string | null
}

// Link Types
export interface PtPLink {
  id: string
  siteA: Site
  siteB: Site
  distance: number
  frequency: number
  feasibility: FeasibilityStatus
  technicalAnalysis: TechnicalAnalysis
  status: LinkStatus
  createdAt: Date
  updatedAt: Date
  createdBy: string
}

export interface Site {
  id: string
  name: string
  coordinates: Coordinates
  height: number
  ranHeight: number
  transportType: TransportType
  leaseType: LeaseType
  towerType: TowerType
  operationalStatus: OperationalStatus
  state: SiteState
}

export interface Coordinates {
  latitude: number
  longitude: number
  latitudeRad: number
  longitudeRad: number
}

export interface TechnicalAnalysis {
  earthCurvature: number
  fresnelZoneRadius: number
  requiredClearance: number
  availableClearance: number
  annualAvailability: number
  fadeMargin: number
  rainAttenuation: number
  atmosphericAbsorption: number
}

export type FeasibilityStatus = 'feasible' | 'not_feasible' | 'conditional'
export type LinkStatus = 'active' | 'inactive' | 'maintenance' | 'planned'
export type TransportType = 'fiber' | 'microwave' | 'satellite' | 'copper'
export type LeaseType = 'owned' | 'leased' | 'shared' | 'colocation'
export type TowerType = 'self_supporting' | 'guyed' | 'monopole' | 'lattice'
export type OperationalStatus = 'on_air' | 'off_air' | 'testing' | 'commissioning'
export type SiteState = 'active' | 'inactive' | 'maintenance' | 'decommissioned'

// Network Analysis Types
export interface NetworkAnalysis {
  id: string
  name: string
  description: string
  links: string[]
  analysisType: AnalysisType
  parameters: AnalysisParameters
  results: AnalysisResults
  createdAt: Date
  createdBy: string
}

export type AnalysisType = 'same_transport' | 'frequency_planning' | 'capacity_analysis' | 'redundancy'
export interface AnalysisParameters {
  maxDistance: number
  minFrequency: number
  maxFrequency: number
  minHeight: number
  transportTypes: TransportType[]
}
export interface AnalysisResults {
  totalLinks: number
  feasibleLinks: number
  nonFeasibleLinks: number
  recommendations: string[]
  charts: ChartData[]
}

// Chart and Visualization Types
export interface ChartData {
  id: string
  type: ChartType
  title: string
  data: any
  options: any
}

export type ChartType = 'bar' | 'line' | 'pie' | 'scatter' | 'heatmap'

// Form and Input Types
export interface LinkFormData {
  siteA: Partial<Site>
  siteB: Partial<Site>
  technicalParameters: Partial<TechnicalAnalysis>
}

export interface ValidationError {
  field: string
  message: string
}

// API Response Types
export interface ApiResponse<T> {
  success: boolean
  data: T
  message: string
  errors?: ValidationError[]
}

export interface PaginatedResponse<T> {
  data: T[]
  pagination: {
    page: number
    limit: number
    total: number
    totalPages: number
  }
}

// File Upload Types
export interface FileUpload {
  id: string
  name: string
  size: number
  type: string
  uploadedAt: Date
  status: UploadStatus
  progress: number
  error?: string
}

export type UploadStatus = 'uploading' | 'completed' | 'failed' | 'processing'

// Settings and Configuration Types
export interface AppSettings {
  theme: Theme
  language: Language
  notifications: NotificationSettings
  display: DisplaySettings
}

export type Theme = 'light' | 'dark' | 'system'
export type Language = 'es' | 'en'
export interface NotificationSettings {
  email: boolean
  push: boolean
  sms: boolean
}
export interface DisplaySettings {
  density: 'compact' | 'comfortable' | 'spacious'
  fontSize: 'small' | 'medium' | 'large'
  showAnimations: boolean
}

// Navigation Types
export interface NavigationItem {
  id: string
  label: string
  path: string
  icon: string
  children?: NavigationItem[]
  badge?: string | number
  disabled?: boolean
}

// Error Types
export interface AppError {
  code: string
  message: string
  details?: any
  timestamp: Date
  userId?: string
}

// Performance and Monitoring Types
export interface PerformanceMetrics {
  pageLoadTime: number
  apiResponseTime: number
  memoryUsage: number
  cpuUsage: number
  timestamp: Date
}

// Export and Import Types
export interface ExportOptions {
  format: ExportFormat
  includeCharts: boolean
  includeAnalysis: boolean
  dateRange?: {
    start: Date
    end: Date
  }
}

export type ExportFormat = 'excel' | 'csv' | 'pdf' | 'json'
