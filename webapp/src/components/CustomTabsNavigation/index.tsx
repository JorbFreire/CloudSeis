import type { Dispatch, SetStateAction } from 'react'
import { useState } from 'react';
import {
  DndContext,
  closestCenter,
  KeyboardSensor,
  PointerSensor,
  useSensor,
  useSensors,
} from '@dnd-kit/core';
import {
  arrayMove,
  SortableContext,
  sortableKeyboardCoordinates,
  horizontalListSortingStrategy,
  verticalListSortingStrategy,
} from '@dnd-kit/sortable';

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

function getOrientation(orientation: navigationOrientationType) {
  if (orientation == "horizontal")
    return horizontalListSortingStrategy
  return verticalListSortingStrategy
}

export default function CustomTabsNavigation({
  tabs,
  color = "primary",
  orientation = "horizontal",
  selectedTab,
  setSelectedTab,
}: ICustomTabsNavigationProps) {
  const [items, setItems] = useState(tabs);
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  function handleDragEnd(event: any) {
    const { active, over } = event;

    if (active.id !== over.id) {
      setItems((items) => {
        const oldIndex = items.findIndex((item) => item.id == active.id);
        const newIndex = items.findIndex((item) => item.id == over.id);

        const result = arrayMove(items, oldIndex, newIndex);
        return result
      });
    }
  }

  return (
    <Container $orientation={orientation}>
      <Tabs
        value={selectedTab}
        onChange={(_, newId) => setSelectedTab(newId)}
        variant="scrollable"
        scrollButtons="auto"
        orientation={orientation}
      >
        <DndContext
          sensors={sensors}
          collisionDetection={closestCenter}
          onDragEnd={handleDragEnd}
        >
          <SortableContext
            items={items}
            strategy={getOrientation(orientation)}
          >
            {items.map((tab) => (
              <CustomTab
                key={tab.id}
                value={tab.id}
                label={tab.name}
                $color={color}
                $orientation={orientation}
              />
            ))}
          </SortableContext>
        </DndContext>
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
