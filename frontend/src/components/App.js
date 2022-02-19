import React, { Component, Fragment } from 'react'
import { Header } from './layout/Header'
import { Main } from './page/Main'
import { Provider } from 'react-redux'
import { store } from '../store'
import { ChakraProvider } from '@chakra-ui/react'
import { theme } from '../theme'
import { Flex } from '@chakra-ui/layout'

class App extends Component {
  render () {
    return (
      <Provider store={store}>
        <ChakraProvider theme={theme}>
          <Flex w='100%' h='100%' flexDirection='column'>
            <Header />
            <Main />
          </Flex>
        </ChakraProvider>
      </Provider>
    )
  }
}

export default App
