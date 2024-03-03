import type { Dispatch, SetStateAction } from 'react'

import Tabs from '@mui/material/Tabs';
import Tooltip from '@mui/material/Tooltip';

import {
  Container,
  TabContent,
  CustomTab,
  TabLabel,
} from './styles'
import type { orientationType } from './styles'

interface ICustomTabsNavigationProps {
  tabs: Array<IgenericEntitiesType>
  orientation?: orientationType
  selectedTab: number
  setSelectedTab: Dispatch<SetStateAction<number>>
}

export default function CustomTabsNavigation({
  tabs,
  orientation = "horizontal",
  selectedTab,
  setSelectedTab,
}: ICustomTabsNavigationProps) {
  return (
    <Container orientation={orientation}>
      <Tabs
        value={selectedTab}
        onChange={(_, newId) => setSelectedTab(newId)}
        variant="scrollable"
        scrollButtons="auto"
        orientation={orientation}
      >
        {tabs.map((tab) => (
          <Tooltip title={tab.name} key={tab.id}>
            <CustomTab
              value={tab.id}
              label={tab.name}
            />
          </Tooltip>
        ))}
      </Tabs>
      {tabs.map(
        (tab) => selectedTab == tab.id && (
          <TabContent key={tab.id}>
          </TabContent>
        )
      )}
    </Container>
  )
}
