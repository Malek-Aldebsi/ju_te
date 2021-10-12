import React, { useRef } from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { uploadImage, actions, downloadReport } from '../../reducers/engine'
import { Box, Center, HStack, List } from '@chakra-ui/layout'
import { FormControl, FormLabel } from '@chakra-ui/form-control'
import { Select } from '@chakra-ui/select'
import { Input, InputGroup, InputRightElement } from '@chakra-ui/input'
import { Image } from '@chakra-ui/image'
import { Button } from '@chakra-ui/button'
import { Spinner } from '@chakra-ui/spinner'
import { UnorderedList, ListItem } from '@chakra-ui/layout'
import { Tabs, TabList, Tab, TabPanels, TabPanel } from '@chakra-ui/tabs'

export function Loading () {
  return (
    <Center w='100%' h='100%'>
      <Spinner size='xl' />
    </Center>
  )
}
