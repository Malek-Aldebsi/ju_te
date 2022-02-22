import React from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { actions } from '../../reducers/engine'
import { Box, Center, HStack, VStack, Flex } from '@chakra-ui/layout'
import { Image } from '@chakra-ui/image'
import { Button } from '@chakra-ui/button'

export function Result ({ aspect }) {
  const assessment = useSelector(({ engine }) => engine[aspect].assessment)
  console.log(assessment)
  const dispatch = useDispatch()

  return (
    <Box w='100%' h='100%'>
      <Flex w='100%' direction={['column', 'row', 'row']}>
        <HStack w={['100%', '50%', '40%']} mb={6}>
          <Center w='100%'>
            <Image src={assessment.processed_image} maxH='600px' w='auto' />
          </Center>
          <Center w='100%'>
            <Image src={assessment.shape_match_image} maxH='600px' w='auto' />
          </Center>
        </HStack>
        <VStack
          mb={6}
          maxH='600px'
          w={['100%', '50%', '60%']}
          overflow='scroll'
        >
          {assessment.notes.map(({ note }, idx) => (
            <Box
              w='100%'
              p={6}
              borderTop='1px'
              borderColor='gray.200'
              key={idx}
            >
              {note}
            </Box>
          ))}
        </VStack>
      </Flex>

      <HStack w='100%' justify='left' spacing={6}>
        <Button
          size='lg'
          colorScheme='yellow'
          onClick={e => dispatch(actions.deleteCurrentAssessment(aspect))}
        >
          ReSubmit Another
        </Button>
        <Button
          size='lg'
          colorScheme='blue'
          as='a'
          download
          href={`engine/api/assessments/${assessment.id}/report/`}
        >
          Save
        </Button>
      </HStack>
    </Box>
  )
}
