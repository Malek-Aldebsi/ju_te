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

const typeOptions = [
  {
    label: 'type 1',
    value: 'type 1'
  },
  {
    label: 'Others',
    value: 'Others'
  }
]

export function Form ({ aspect, title }) {
  const photoRef = useRef()
  const dispatch = useDispatch()
  const aspectData = useSelector(({ engine }) => engine[aspect].data)

  const submit = e => {
    e.preventDefault()

    dispatch(uploadImage(aspect))
  }

  return (
    <>
      <FormControl isRequired mb={3}>
        <FormLabel htmlFor='type'>Image Type</FormLabel>
        <Select
          value={aspectData.type}
          onChange={e =>
            dispatch(
              actions.setData({ aspect, name: 'type', value: e.target.value })
            )
          }
        >
          {typeOptions.map((item, idx) => (
            <option key={idx} value={item.value}>
              {item.label}
            </option>
          ))}
        </Select>
      </FormControl>

      <FormControl isRequired mb={3}>
        <FormLabel htmlFor='image'>Upload Image</FormLabel>
        <Input
          type='file'
          display='none'
          name='image'
          onChange={e =>
            dispatch(
              actions.setData({
                aspect,
                name: 'image',
                value: e.currentTarget.files[0]
              })
            )
          }
          ref={photoRef}
        />
        <InputGroup>
          <Input
            isReadOnly
            value={aspectData?.image?.name || 'No file uploaded'}
          />

          <InputRightElement w='30%'>
            <Button
              w='100%'
              colorScheme='blue'
              onClick={() => photoRef.current.click()}
            >
              Upload
            </Button>
          </InputRightElement>
        </InputGroup>
      </FormControl>
      <Button colorScheme='blue' onClick={submit}>
        Submit
      </Button>
    </>
  )
}
