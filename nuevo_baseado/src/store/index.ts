import { configureStore } from '@reduxjs/toolkit'
import { persistStore, persistReducer } from 'redux-persist'
import storage from 'redux-persist/lib/storage'

import authReducer from './slices/authSlice'
import linksReducer from './slices/linksSlice'
import networkAnalysisReducer from './slices/networkAnalysisSlice'
import uiReducer from './slices/uiSlice'
import settingsReducer from './slices/settingsSlice'

const persistConfig = {
  key: 'fangio-telecom-root',
  storage,
  whitelist: ['auth', 'settings'],
}

const persistedAuthReducer = persistReducer(persistConfig, authReducer)
const persistedSettingsReducer = persistReducer(persistConfig, settingsReducer)

export const store = configureStore({
  reducer: {
    auth: persistedAuthReducer,
    links: linksReducer,
    networkAnalysis: networkAnalysisReducer,
    ui: uiReducer,
    settings: persistedSettingsReducer,
  },
  middleware: (getDefaultMiddleware) =>
    getDefaultMiddleware({
      serializableCheck: {
        ignoredActions: ['persist/PERSIST', 'persist/REHYDRATE'],
      },
    }),
  devTools: process.env.NODE_ENV !== 'production',
})

export const persistor = persistStore(store)

export type RootState = ReturnType<typeof store.getState>
export type AppDispatch = typeof store.dispatch
