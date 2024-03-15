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
  selectedTab: number | undefined
  setSelectedTab: Dispatch<SetStateAction<number | undefined>>
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
  CustomDndContext = ({ children }) => (children),
}: ICustomTabsNavigationProps) {

  return Boolean(tabs.length) && (
    <Container $orientation={orientation}>
      {/* *** CustomDndContext is passed by optional props *** */}
      <CustomDndContext
        orientation={orientation}
        items={tabs}
        setItems={setTabs}
      >
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
      </CustomDndContext>

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
