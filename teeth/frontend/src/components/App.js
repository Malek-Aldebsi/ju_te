import React, { Component, Fragment } from "react";
import Header from "./layout/Header";
import Main from "./page/Main";
import { Provider } from "react-redux";
import store from "../store";

class App extends Component {
  render() {
    return (
      <Provider store={store}>
        <Fragment>
          <Header />
          <Main />
        </Fragment>
      </Provider>
    );
  }
}

export default App;
