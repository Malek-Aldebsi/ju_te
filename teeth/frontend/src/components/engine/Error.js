import { Text, Box, Divider } from '@chakra-ui/layout'

export function Error ({ message, status }) {
  return (
    <Box flex={true} h='100%' flexDirection='column'>
      <Text fontSize='2xl' color='red.300'>
        Something Went Wrong
      </Text>
      <Text>{`Status: ${status}`}</Text>
      <Divider orientation='horizontal' w='100%' />
      <Text as='p' fontSize='lg'>
        {message}
      </Text>
    </Box>
  )
}
