import {
  UPLOAD_LOADING,
  UPLOAD_SUCCESS,
  DELETE_CURRENT,
} from "../actions/types";

const initialState = {
  errors: null,
  isLoading: false,
  assessment: null,
};

export default function (state = initialState, action) {
  switch (action.type) {
    case UPLOAD_LOADING:
      return {
        ...state,
        isLoading: true,
        errors: null,
        assessment: null,
      };

    case UPLOAD_SUCCESS:
      return {
        ...state,
        assessment: action.payload,
        isLoading: false,
        errors: null,
      };

    case DELETE_CURRENT:
      return {
        ...state,
        isLoading: false,
        assessment: null,
        errors: null,
      };

    default:
      return state;
  }
}
