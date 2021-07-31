import React, { Component, Fragment } from "react";
import { connect } from "react-redux";
import { upload, delete_current, download } from "../../actions/engine";

class Main extends Component {
  constructor(props) {
    super(props);
    this.fileInput = React.createRef();
  }

  state = {
    aspect: "Labial",
    type: "type 1",
  };

  componentDidUpdate() {
    //this.props.delete_current(false);
  }

  handleChange = (event) => {
    this.setState({ [event.target.name]: event.target.value });
  };

  handleSubmit = (event) => {
    event.preventDefault();
    const { aspect, type } = this.state;
    this.props.upload({
      aspect,
      type,
      image: this.fileInput.current.files[0],
    });
  };

  render() {
    let body = <div></div>;

    if (this.props.isLoading) {
      body = (
        <div className="card-body mt-5 text-center">
          <h6 className="h6">Loading</h6>
          <div className="spinner-border text-muted" role="status">
            <span className="visually-hidden">Loading...</span>
          </div>
        </div>
      );
    } else if (this.props.assessment) {
      const notes = this.props.assessment.notes.map((note, id) => (
        <li key={id} className="list-group-item">
          {note.note}
        </li>
      ));
      body = (
        <Fragment>
          <img
            className="img-fluid"
            src={this.props.assessment.processed_image}
            style={{ maxHeight: "400px" }}
          ></img>
          <div className="card-body">
            <ul className="list-group list-group-flush">{notes}</ul>
            <button
              type="button"
              className="btn btn-primary"
              onClick={() => this.props.delete_current(true)}
            >
              ReSubmit Another
            </button>

            <a
              className="btn btn-primary"
              href={`engine/api/assessments/${this.props.assessment.id}/report/`}
            >
              Save
            </a>
          </div>
        </Fragment>
      );
    } else {
      body = (
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
      );
    }

    return (
      <div className="container">
        <div className="row justify-content-center mt-5">
          <div className="col-xs-12 col-md-6">
            <div className="card h-100" style={{ maxHeight: "8rm" }}>
              <div className="card-header">
                <h4 className="h4">Tooth Picture</h4>
              </div>
              {body}
            </div>
          </div>
        </div>
      </div>
    );
  }
}

const mapStateToProps = (state) => ({
  isLoading: state.engine.isLoading,
  assessment: state.engine.assessment,
});

export default connect(mapStateToProps, { upload, delete_current, download })(
  Main
);
