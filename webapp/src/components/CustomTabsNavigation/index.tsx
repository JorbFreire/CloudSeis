import type { ComponentType, ReactNode } from 'react'

import Tabs from '@mui/material/Tabs';
import CustomTab from 'components/CustomTab';
import { IDefaultDNDListProps } from 'components/DefaultDNDList/types'
import { StaticTabKey, isFixedTab } from 'enums/StaticTabKey'

import {
  Container,
  TabContent,
} from './styles'

type selectedTabType = number | StaticTabKey | undefined

// *** once <T> accepts any type extending "IgenericTab"
// *** it shall be capable to render any matching array
// *** not needing to convert it removing other filds missing at "IgenericTab"
interface ICustomTabsNavigationProps<T extends IgenericTab> {
  tabs: Array<T>
  setTabs: genericSetterType<T>
  selectedTab: selectedTabType
  setSelectedTab: genericSetterType<selectedTabType>
  onRemove?: onRemoveActionType

  children?: ReactNode
  color?: navigationColorType
  orientation?: navigationOrientationType

  CustomDndContext?: ComponentType<IDefaultDNDListProps<T>>
}

export default function CustomTabsNavigation<T extends IgenericTab>({
  tabs,
  setTabs,
  selectedTab,
  setSelectedTab,
  onRemove,

  children,
  color = "primary",
  orientation = "horizontal",

  // *** render empty element by default when no FixedLastTabOptions provided
  CustomDndContext = ({ children }) => (<>{children}</>),
}: ICustomTabsNavigationProps<T>) {
  // ? conditional rendering could be a high order component ?
  const removeElementFromState = () => {
    if (!selectedTab || isFixedTab(selectedTab))
      return

    const newTabs = tabs.filter((element, index) =>
      index != selectedTab &&
      !isFixedTab(element.id)
    )

    if (onRemove && typeof selectedTab == "number")
      onRemove(tabs[selectedTab].id)

    setTabs(newTabs)
    setSelectedTab(StaticTabKey.Input)
  }

  return Boolean(tabs.length) ? (
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
              onRemove={removeElementFromState}
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
  ) : (
    <></>
  )
}
