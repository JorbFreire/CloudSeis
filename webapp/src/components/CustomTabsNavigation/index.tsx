import type { Dispatch, SetStateAction } from 'react'

import Tabs from '@mui/material/Tabs';
import Tooltip from '@mui/material/Tooltip';

import {
  Container,
  TabContent,
  CustomTab,
} from './styles'
import type { colorType, orientationType } from "./styleGetters"

interface ICustomTabsNavigationProps {
  tabs: Array<IgenericEntitiesType>
  color?: colorType
  orientation?: orientationType
  selectedTab: number
  setSelectedTab: Dispatch<SetStateAction<number>>
}

export default function CustomTabsNavigation({
  tabs,
  color = "primary",
  orientation = "horizontal",
  selectedTab,
  setSelectedTab,
}: ICustomTabsNavigationProps) {
  return (
    <Container $orientation={orientation}>
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
              $color={color}
              $orientation={orientation}
            />
          </Tooltip>
        ))}
      </Tabs>

      {tabs.map(
        (tab) => selectedTab == tab.id && (
          <TabContent
            key={tab.id}
            $color={color}
            $orientation={orientation}
          >
          </TabContent>
        )
      )}
    </Container>
  )
}
