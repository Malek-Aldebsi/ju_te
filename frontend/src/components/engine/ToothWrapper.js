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
import { Result } from './Result'
import { Loading } from './Loading'
import { Form } from './Form'
import { Error } from './Error'

export function ToothWrapper ({ aspect, title }) {
  const isLoading = useSelector(({ engine }) => engine[aspect].isLoading)
  const assessment = useSelector(({ engine }) => engine[aspect].assessment)
  const error = useSelector(({ engine }) => engine[aspect].error)

  console.log('error of wrapper', error)
  if (error) {
    return <Error message={error?.message} status={error.status} />
  } else if (isLoading) {
    return <Loading />
  } else if (assessment) {
    return <Result aspect={aspect} />
  }

  return (
    <Box
      flex
      flexDirection='column'
      h={['100%', '524px', '400px']}
      px={[0, 3, 6]}
      py={[0, 4, 6]}
    >
      <Center w='100%' mb={12} fontSize='xl'>
        {title}
      </Center>
      <Form aspect={aspect} title={title} />
    </Box>
  )
}
