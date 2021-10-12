import { createAsyncThunk, createSlice } from '@reduxjs/toolkit'

import axios from 'axios'

const initialState = {
  labial: {
    errors: null,
    isLoading: false,
    assessment: null,
    data: { type: 'type 1', image: null }
  },
  lingual: {
    errors: null,
    isLoading: false,
    assessment: null,
    data: { type: 'type 1', image: null }
  },
  mesial: {
    errors: null,
    isLoading: false,
    assessment: null,
    data: { type: 'type 1', image: null }
  },
  destial: {
    errors: null,
    isLoading: false,
    assessment: null,
    data: { type: 'type 1', image: null }
  },
  top: {
    errors: null,
    isLoading: false,
    assessment: null,
    data: { type: 'type 1', image: null }
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
    formData.append('image_aspect', aspect[0].toUpperCase() + aspect.slice(1))
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
    } catch (err) {
      console.log('error happend while uploading the image', err)
      throw err
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
      state[aspect].errors = null
      state[aspect].assessment = null
    },

    setData: (state, action) => {
      const { aspect, name, value } = action.payload
      state[aspect].data[name] = value
    },

    deleteCurrentAssessment: (state, action) => {
      const aspect = action.payload
      state[aspect].isLoading = false
      state[aspect].errors = null
      state[aspect].assessment = null
    }
  },
  extraReducers: builder => {
    builder.addCase(uploadImage.fulfilled, (state, action) => {
      const { aspect, assessment } = action.payload
      state[aspect].isLoading = false
      state[aspect].errors = null
      state[aspect].assessment = assessment
    })
  }
})

export default engineSlice.reducer
export const actions = engineSlice.actions

// export default function (state = initialState, action) {
//   switch (action.type) {
//     case UPLOAD_LOADING:
//       return {
//         ...state,
//         isLoading: true,
//         errors: null,
//         assessment: null
//       }

//     case UPLOAD_SUCCESS:
//       console.log(JSON.stringify(action.payload))
//       return {
//         ...state,
//         assessment: action.payload,
//         isLoading: false,
//         errors: null
//       }

//     case DELETE_CURRENT:
//       if (action.payload) {
//         return {
//           ...state,
//           isLoading: false,
//           assessment: null,
//           errors: null
//         }
//       } else {
//         return {
//           ...state,
//           isLoading: false,
//           errors: null
//         }
//       }

//     default:
//       return state
//   }
// }
