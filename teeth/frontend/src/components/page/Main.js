import React from 'react'
import { Box, Center, Flex } from '@chakra-ui/layout'
import { Tabs, TabList, Tab, TabPanels, TabPanel } from '@chakra-ui/tabs'
import { ToothWrapper } from '../engine/ToothWrapper'

export function Main () {
  return (
    <Flex
      flexDir='column'
      justify='center'
      alignItems='center'
      w={['100%', '100%', '100%']}
      mt={[0, 16, 24]}
      h='100%'
    >
      <Box
        bg='white'
        rounded={['none', 'lg', 'lg']}
        shadow='sm'
        border='1px solid lightgray'
      >
        <Tabs isFitted>
          <TabList>
            <Tab>Buccal/Facial</Tab>
            <Tab>Lingual</Tab>
            <Tab>Mesial</Tab>
            <Tab>Distal</Tab>
            <Tab>Top</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <ToothWrapper aspect='buccal' title='Buccal/Facial' />
            </TabPanel>
            <TabPanel>
              <ToothWrapper aspect='lingual' title='Lingual' />
            </TabPanel>
            <TabPanel>
              <ToothWrapper aspect='mesial' title='Mesial' />
            </TabPanel>
            <TabPanel>
              <ToothWrapper aspect='distal' title='Destial' />
            </TabPanel>
            <TabPanel>
              <ToothWrapper aspect='top_view' title='Top' />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Flex>
  )
}
