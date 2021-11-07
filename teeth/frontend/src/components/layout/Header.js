import { HStack, Flex, Heading } from '@chakra-ui/layout'
import { Avatar } from '@chakra-ui/avatar'
import React from 'react'

export function Header (props) {
  return (
    <Flex
      align='center'
      wrap='wrap'
      padding={6}
      color='white'
      bg='blue.700'
      justify='space-between'
      as='nav'
      w='100%'
      shadow='md'
    >
      <HStack h='full' align='center' spacing={6} justify='left'>
        <Avatar src={'static/frontend/img/logo.jpg'} />
        <Heading size='lg' letterSpacing='tighter' as='h1'>
          Tooth Vision
        </Heading>
      </HStack>
    </Flex>
  )
}
