import axios from "axios";
import { DELETE_CURRENT, UPLOAD_LOADING, UPLOAD_SUCCESS } from "./types";

export const upload =
  ({ aspect, type, image }) =>
  (dispatch) => {
    //waiting for response
    dispatch({ type: UPLOAD_LOADING });

    var formData = new FormData();
    formData.append("image_aspect", aspect);
    formData.append("image_type", type);
    formData.append("original_image", image);

    const config = {
      headers: {
        "Content-Type": "multipart/form-data",
        "X-CSRFToken": getCookie("csrftoken"),
      },
    };
    axios
      .post("engine/api/assessments/", formData, config)
      .then((res) => {
        dispatch({ type: UPLOAD_SUCCESS, payload: res.data });
      })
      .catch((err) => console.log(err));
  };

export const delete_current = () => (dispatch, getState) => {
  const id = getState().engine.assessment.id;

  const config = {
    headers: {
      // "X-CSRFToken": getCookie("csrftoken"),
    },
  };

  axios
    .delete(`engine/api/assessments/${id}/`, null, config)
    .then((res) => dispatch({ type: DELETE_CURRENT }))
    .catch((err) => console.log(err));
};

function getCookie(name) {
  let cookieValue = null;
  if (document.cookie && document.cookie !== "") {
    const cookies = document.cookie.split(";");
    for (let i = 0; i < cookies.length; i++) {
      const cookie = cookies[i].trim();
      // Does this cookie string begin with the name we want?
      if (cookie.substring(0, name.length + 1) === name + "=") {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
        break;
      }
    }
  }
  return cookieValue;
}
