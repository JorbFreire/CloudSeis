import type { Dispatch, SetStateAction, ComponentType } from 'react'

import Tabs from '@mui/material/Tabs';
import CustomTab from 'components/CustomTab';
import { IDefaultDNDListProps } from 'components/DefaultDNDList/types'

import {
  Container,
  TabContent,
} from './styles'

interface ICustomTabsNavigationProps {
  tabs: Array<IgenericEntitiesType>
  setTabs: Dispatch<SetStateAction<Array<IgenericEntitiesType>>>
  selectedTab: number
  setSelectedTab: Dispatch<SetStateAction<number>>
  color?: navigationColorType
  orientation?: navigationOrientationType
  CustomDndContext?: ComponentType<IDefaultDNDListProps>
}

export default function CustomTabsNavigation({
  tabs,
  setTabs,
  color = "primary",
  orientation = "horizontal",
  selectedTab,
  setSelectedTab,
  // *** render empty element by default when no DndContextProvided
  CustomDndContext = ({ children }) => (<>{children}</>),
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
        {/* *** CustomDndContext is passed by props and optional *** */}
        <CustomDndContext
          orientation={orientation}
          items={tabs}
          setItems={setTabs}
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
        </CustomDndContext>
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
