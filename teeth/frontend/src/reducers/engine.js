import { UPLOAD_LOADING, UPLOAD_SUCCESS } from "../actions/types";

const initialState = {
  id: null,
  message: null,
  isLoading: false,
  processed_file_path: null,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case UPLOAD_LOADING:
      return { ...state, isLoading: true, id: null, message: null, file: null };

    case UPLOAD_SUCCESS:
      console.log(action.payload);
      return { ...state, ...action.payload, isLoading: false, id: null };
    default:
      return state;
  }
}
