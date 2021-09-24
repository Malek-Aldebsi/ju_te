import { atom } from 'recoil'

export const engineState = atom({
  key: 'engineState',
  default: {
    errors: null,
    isLoading: false,
    assessment: null
  }
})
