import { createSlice, PayloadAction } from '@reduxjs/toolkit'
import { AppSettings } from '@/types'

const initialState: AppSettings = {
  theme: 'dark',
  language: 'es',
  notifications: {
    email: true,
    push: true,
    sms: false,
  },
  display: {
    density: 'comfortable',
    fontSize: 'medium',
    showAnimations: true,
  },
}

const settingsSlice = createSlice({
  name: 'settings',
  initialState,
  reducers: {
    updateTheme: (state, action: PayloadAction<AppSettings['theme']>) => {
      state.theme = action.payload
    },
    updateLanguage: (state, action: PayloadAction<AppSettings['language']>) => {
      state.language = action.payload
    },
    updateNotificationSettings: (state, action: PayloadAction<Partial<AppSettings['notifications']>>) => {
      state.notifications = { ...state.notifications, ...action.payload }
    },
    updateDisplaySettings: (state, action: PayloadAction<Partial<AppSettings['display']>>) => {
      state.display = { ...state.display, ...action.payload }
    },
    resetSettings: () => initialState,
  },
})

export const {
  updateTheme,
  updateLanguage,
  updateNotificationSettings,
  updateDisplaySettings,
  resetSettings,
} = settingsSlice.actions

export default settingsSlice.reducer
