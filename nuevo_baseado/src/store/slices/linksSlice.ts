import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit'
import { PtPLink } from '@/types'

interface LinksState {
  links: PtPLink[]
  isLoading: boolean
  error: string | null
  selectedLinks: string[]
}

const initialState: LinksState = {
  links: [],
  isLoading: false,
  error: null,
  selectedLinks: [],
}

export const fetchLinks = createAsyncThunk(
  'links/fetchLinks',
  async (_, { rejectWithValue }) => {
    try {
      // TODO: Implementar llamada a API
      return []
    } catch (error: any) {
      return rejectWithValue(error.message || 'Error al cargar enlaces')
    }
  }
)

export const addLink = createAsyncThunk(
  'links/addLink',
  async (link: Omit<PtPLink, 'id' | 'createdAt' | 'updatedAt'>, { rejectWithValue }) => {
    try {
      // TODO: Implementar llamada a API
      const newLink: PtPLink = {
        ...link,
        id: Date.now().toString(),
        createdAt: new Date(),
        updatedAt: new Date(),
      }
      return newLink
    } catch (error: any) {
      return rejectWithValue(error.message || 'Error al agregar enlace')
    }
  }
)

const linksSlice = createSlice({
  name: 'links',
  initialState,
  reducers: {
    setSelectedLinks: (state, action: PayloadAction<string[]>) => {
      state.selectedLinks = action.payload
    },
    toggleLinkSelection: (state, action: PayloadAction<string>) => {
      const linkId = action.payload
      if (state.selectedLinks.includes(linkId)) {
        state.selectedLinks = state.selectedLinks.filter(id => id !== linkId)
      } else {
        state.selectedLinks.push(linkId)
      }
    },
    clearSelection: (state) => {
      state.selectedLinks = []
    },
  },
  extraReducers: (builder) => {
    builder
      .addCase(fetchLinks.pending, (state) => {
        state.isLoading = true
        state.error = null
      })
      .addCase(fetchLinks.fulfilled, (state, action) => {
        state.isLoading = false
        state.links = action.payload
      })
      .addCase(fetchLinks.rejected, (state, action) => {
        state.isLoading = false
        state.error = action.payload as string
      })
      .addCase(addLink.fulfilled, (state, action) => {
        state.links.push(action.payload)
      })
  },
})

export const { setSelectedLinks, toggleLinkSelection, clearSelection } = linksSlice.actions
export default linksSlice.reducer
