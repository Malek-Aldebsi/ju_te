import axios from "axios";
import { UPLOAD_LOADING, UPLOAD_SUCCESS } from "./types";

export const upload =
  ({ aspect, type, file }) =>
  (dispatch) => {
    //waiting for response
    dispatch({ type: UPLOAD_LOADING });

    var formData = new FormData();
    formData.append("aspect", aspect);
    formData.append("type", type);
    formData.append("file", file);

    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    };
    axios.post("engine/upload/", formData, config).then((res) => {
      dispatch({ type: UPLOAD_SUCCESS, payload: res.data });
    });
  };
