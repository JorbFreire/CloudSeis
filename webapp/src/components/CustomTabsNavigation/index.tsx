import type { ComponentType, ReactNode } from 'react'

import Tabs from '@mui/material/Tabs';
import CustomTab from 'components/CustomTab';
import { IDefaultDNDListProps } from 'components/DefaultDNDList/types'
import { StaticTabKey } from 'constants/StaticTabKey'

import {
  Container,
  TabContent,
} from './styles'

type selectedTabIdType = number | StaticTabKey | undefined

// *** once <T> accepts any type extending "IgenericTab"
// *** it shall be capable to render any matching array
// *** not needing to convert it removing other filds missing at "IgenericTab"
interface ICustomTabsNavigationProps<T extends IgenericTab> {
  tabs: Array<T>
  setTabs: genericSetterType<T>
  selectedTabId: selectedTabIdType
  setSelectedTabId: genericSetterType<selectedTabIdType>
  onRemove?: onRemoveActionType

  children?: ReactNode
  color?: navigationColorType
  orientation?: navigationOrientationType

  CustomDndContext?: ComponentType<IDefaultDNDListProps<T>>
}

export default function CustomTabsNavigation<T extends IgenericTab>({
  tabs,
  setTabs,
  selectedTabId,
  setSelectedTabId,
  onRemove,

  children,
  color = "primary",
  orientation = "horizontal",

  // *** render empty element by default when no FixedLastTabOptions provided
  CustomDndContext = ({ children }) => (<>{children}</>),
}: ICustomTabsNavigationProps<T>) {
  // ? conditional rendering could be a high order component ?
  const removeElementFromState = () => {
    if (!selectedTabId || typeof selectedTabId == 'string')
      return

    const newTabs = tabs.filter((element) => element.id != selectedTabId)

    if (onRemove && typeof selectedTabId == "number")
      onRemove(selectedTabId)

    setTabs(newTabs)
    setSelectedTabId(StaticTabKey.Input)
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
          value={selectedTabId}
          onChange={(_, newId) => setSelectedTabId(newId)}
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
              $isActive={tab.is_active}
            />
          ))}
        </Tabs>
      </CustomDndContext>

      {tabs.map(
        (tab) => selectedTabId == tab.id && (
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
