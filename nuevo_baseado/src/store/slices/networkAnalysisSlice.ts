import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { NetworkAnalysis } from '@/types'

interface NetworkAnalysisState {
  analyses: NetworkAnalysis[]
  currentAnalysis: NetworkAnalysis | null
  isLoading: boolean
  error: string | null
}

const initialState: NetworkAnalysisState = {
  analyses: [],
  currentAnalysis: null,
  isLoading: false,
  error: null,
}

export const createAnalysis = createAsyncThunk(
  'networkAnalysis/createAnalysis',
  async (analysis: Omit<NetworkAnalysis, 'id' | 'createdAt'>, { rejectWithValue }) => {
    try {
      // TODO: Implementar llamada a API
      const newAnalysis: NetworkAnalysis = {
        ...analysis,
        id: Date.now().toString(),
        createdAt: new Date(),
      }
      return newAnalysis
    } catch (error: any) {
      return rejectWithValue(error.message || 'Error al crear análisis')
    }
  }
)

const networkAnalysisSlice = createSlice({
  name: 'networkAnalysis',
  initialState,
  reducers: {
    setCurrentAnalysis: (state, action: PayloadAction<NetworkAnalysis | null>) => {
      state.currentAnalysis = action.payload
    },
    clearError: (state) => {
      state.error = null
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(createAnalysis.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(createAnalysis.fulfilled, (state, action) => {
        state.isLoading = false
        state.analyses.push(action.payload)
        state.currentAnalysis = action.payload
      })
      .addCase(createAnalysis.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
  },
})

export const { setCurrentAnalysis, clearError } = networkAnalysisSlice.actions
export default networkAnalysisSlice.reducer
