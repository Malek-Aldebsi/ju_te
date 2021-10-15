import React from 'react'
import { Center } from '@chakra-ui/layout'
import { Spinner } from '@chakra-ui/spinner'

export function Loading () {
  return (
    <Center w='100%' h='400px'>
      <Spinner color='blue.500' size='xl' />
    </Center>
  )
}
