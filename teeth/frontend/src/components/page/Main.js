import React from 'react'
import { Box, Center } from '@chakra-ui/layout'
import { Tabs, TabList, Tab, TabPanels, TabPanel } from '@chakra-ui/tabs'
import { ToothWrapper } from '../engine/ToothWrapper'

export function Main () {
  return (
    <Center w='100%'>
      <Box
        bg='white'
        w={['100%', '100%', '60%']}
        m={16}
        rounded='lg'
        shadow='sm'
        border='1px solid lightgray'
      >
        <Tabs isFitted>
          <TabList>
            <Tab>Buccal</Tab>
            <Tab>Lingual</Tab>
            <Tab>Mesial</Tab>
            <Tab>Distal</Tab>
            <Tab>Top View</Tab>
          </TabList>
          <TabPanels>
            <TabPanel>
              <ToothWrapper aspect='buccal' title='Buccal' />
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
              <ToothWrapper aspect='top_view' title='Top View' />
            </TabPanel>
          </TabPanels>
        </Tabs>
      </Box>
    </Center>
  )
}
