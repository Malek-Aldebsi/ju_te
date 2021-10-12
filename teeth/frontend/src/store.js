import { configureStore } from '@reduxjs/toolkit'
import engineReducer from './reducers/engine'

// const store = createStore(
//   rootReducer,
//   initialState,
//   composeWithDevTools(applyMiddleware(...middleware))
// );

export const store = configureStore({
  reducer: { engine: engineReducer }
})
