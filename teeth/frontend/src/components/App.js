import React, { Component, Fragment } from 'react'
import Header from './layout/Header'
import { Main } from './page/Main'
import { Provider } from 'react-redux'
import { store } from '../store'
import { ChakraProvider } from '@chakra-ui/react'
import { theme } from '../theme'

class App extends Component {
  render () {
    return (
      <Provider store={store}>
        <ChakraProvider theme={theme}>
          <Fragment>
            <Header />
            <Main />
          </Fragment>
        </ChakraProvider>
      </Provider>
    )
  }
}

export default App
