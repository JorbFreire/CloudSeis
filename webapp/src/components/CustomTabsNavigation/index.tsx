import type { Dispatch, SetStateAction } from 'react'

import Tabs from '@mui/material/Tabs';
import CustomTab from 'components/CustomTab';

import {
  Container,
  TabContent,
} from './styles'

interface ICustomTabsNavigationProps {
  tabs: Array<IgenericEntitiesType>
  color?: navigationColorType
  orientation?: navigationOrientationType
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
          <CustomTab
            key={tab.id}
            value={tab.id}
            label={tab.name}
            $color={color}
            $orientation={orientation}
          />
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
