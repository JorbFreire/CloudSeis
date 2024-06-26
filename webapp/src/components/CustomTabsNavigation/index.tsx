import { type Dispatch, type SetStateAction, type ComponentType, type ReactNode, useEffect } from 'react'

import Tabs from '@mui/material/Tabs';
import CustomTab from 'components/CustomTab';
import { IDefaultDNDListProps } from 'components/DefaultDNDList/types'

import {
  Container,
  TabContent,
} from './styles'


// *** once <T> accepts any type extending "IgenericEntitiesType"
// *** it shall be capable to render any matching array
// *** not needing to convert it removing other filds missing at "IgenericEntitiesType"
interface ICustomTabsNavigationProps<T extends IgenericEntitiesType> {
  tabs: Array<T>
  setTabs: Dispatch<SetStateAction<Array<T>>>
  selectedTab: number | undefined
  setSelectedTab: Dispatch<SetStateAction<number | undefined>>

  children?: ReactNode

  color?: navigationColorType
  orientation?: navigationOrientationType
  CustomDndContext?: ComponentType<IDefaultDNDListProps<T>>
}

export default function CustomTabsNavigation<T extends IgenericEntitiesType>({
  tabs,
  setTabs,
  selectedTab,
  setSelectedTab,

  children,
  color = "primary",
  orientation = "horizontal",
  // *** render empty element by default when no DndContextProvided
  CustomDndContext = ({ children }) => (children),
}: ICustomTabsNavigationProps<T>) {
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
            {children}
          </TabContent>
        )
      )}
    </Container>
  )
}
