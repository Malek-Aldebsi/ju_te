import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

import axios from 'axios'

const initialState = {
  buccal: {
    error: null,
    isLoading: false,
    assessment: null,
    data: { type: 'permandipular', image: null }
  },
  lingual: {
    error: null,
    isLoading: false,
    assessment: null,
    data: { type: 'permandipular', image: null }
  },
  mesial: {
    error: null,
    isLoading: false,
    assessment: null,
    data: { type: 'permandipular', image: null }
  },
  distal: {
    error: null,
    isLoading: false,
    assessment: null,
    data: { type: 'permandipular', image: null }
  },
  top_view: {
    error: null,
    isLoading: false,
    assessment: null,
    data: { type: 'permandipular', image: null }
  }
}

function getCookie (name) {
  let cookieValue = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim()
      if (cookie.substring(0, name.length + 1) === name + '=') {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

export const uploadImage = createAsyncThunk(
  'engine/uploadImage',
  async (aspect, reduxAPI) => {
    const { type, image } = reduxAPI.getState().engine[aspect].data

    reduxAPI.dispatch(actions.uploadLoading(aspect))

    const formData = new FormData()
    formData.append('image_aspect', aspect)
    formData.append('image_type', type)
    formData.append('original_image', image)

    const config = {
      headers: {
        'Content-Type': 'multipart/form-data',
        'X-CSRFToken': getCookie('csrftoken')
      }
    }

    try {
      const resp = await axios.post('engine/api/assessments/', formData, config)
      const dataResp = await axios.get(
        `engine/api/assessments/${resp.data.id}/`
      )
      return { aspect, assessment: dataResp.data }
    } catch (error) {
      console.log(error)
      reduxAPI.rejectWithValue({ error, aspect })
      return { error, aspect }
    }
  }
)

export const engineSlice = createSlice({
  name: 'engine',
  initialState,
  reducers: {
    uploadLoading: (state, action) => {
      const aspect = action.payload
      state[aspect].isLoading = true
      state[aspect].error = null
      state[aspect].assessment = null
    },

    setData: (state, action) => {
      const { aspect, name, value } = action.payload
      state[aspect].data[name] = value
    },

    deleteCurrentAssessment: (state, action) => {
      const aspect = action.payload
      state[aspect].isLoading = false
      state[aspect].error = null
      state[aspect].assessment = null
    }
  },
  extraReducers: builder => {
    builder.addCase(uploadImage.fulfilled, (state, action) => {
      const { aspect, assessment } = action.payload
      state[aspect].isLoading = false
      state[aspect].error = null
      state[aspect].assessment = assessment
    })
    builder.addCase(uploadImage.rejected, (state, action) => {
      const { error, aspect } = action.payload
      state[aspect].error = error
    })
  }
})

export default engineSlice.reducer
export const actions = engineSlice.actions
