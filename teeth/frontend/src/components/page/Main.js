import React, { Component } from "react";
import { connect } from "react-redux";
import { upload } from "../../actions/engine";

class Main extends Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();
  }

  state = {
    aspect: "Labial",
    type: "type 1",
  };

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { aspect, type } = this.state;
    this.props.upload({
      aspect,
      type,
      file: this.fileInput.current.files[0],
    });
  };

  render() {
    let body = <div></div>;

    if (this.props.processed_file_path) {
      body = (
        <div className="row justify-content-center mt-2">
          <div className=" col-xs-12 col-sm-8 col-md-6 text-center">
            <img
              className="img-fluid img-thumbnail"
              src={this.props.processed_file_path}
              style={{ maxHeight: "400px" }}
            ></img>
          </div>
        </div>
      );
    }

    return (
      <div className="container">
        <div className="row justify-content-md-center mt-5">
          <div className="col-xs-12 col-md-6">
            <div className="card">
              <div className="card-header">
                <h4 className="h4">Tooth Picture</h4>
              </div>
              <div className="card-body">
                <form
                  className="row justify-content-center"
                  encType="multipart/form-data"
                  onSubmit={this.handleSubmit}
                >
                  <div className="mb-3 col-xs-12 col-md-6">
                    <label className="form-label" htmlFor="type">
                      Photo Type
                    </label>
                    <select
                      className="form-select"
                      name="type"
                      value={this.state.type}
                      onChange={this.handleChange}
                    >
                      <option value="type 1">type 1</option>
                      <option value="Others">Others</option>
                    </select>
                  </div>

                  <div className="w-100" />

                  <div className="mb-3 col-xs-12 col-md-6">
                    <label className="form-label" htmlFor="aspect">
                      Photo Aspect
                    </label>

                    <select
                      className="form-select"
                      name="aspect"
                      value={this.state.aspect}
                      onChange={this.handleChange}
                      required
                    >
                      <option value="Labial">Labial</option>
                      <option value="Lingual">Lingual</option>
                      <option value="Mesial">Mesial</option>
                      <option value="Destial">Destial</option>
                      <option value="top view">top view</option>
                    </select>
                  </div>

                  <div className="w-100" />

                  <div className="mb-3 col-xs-12 col-md-6">
                    <label htmlFor="file" className="form-label">
                      Tooth Photo
                    </label>
                    <input
                      className="form-control"
                      type="file"
                      name="file"
                      ref={this.fileInput}
                      required
                    />
                  </div>

                  <div className="w-100"></div>

                  <button
                    type="submit"
                    className="btn btn-primary btn-block mb-4 col-xs-8 col-sm-6 col-md-2"
                  >
                    Submit
                  </button>
                </form>
              </div>
            </div>
          </div>
        </div>
        {body}
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isLoading: state.engine.isLoading,
  processed_file_path: state.engine.processed_file_path,
});

export default connect(mapStateToProps, { upload })(Main);
