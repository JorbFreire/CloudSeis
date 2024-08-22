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
import {
  restrictToVerticalAxis,
  restrictToHorizontalAxis,
  restrictToWindowEdges,
} from '@dnd-kit/modifiers';

import { IDefaultDNDListProps } from './types'

function getOrientation(orientation: navigationOrientationType) {
  if (orientation == "horizontal")
    return horizontalListSortingStrategy
  return verticalListSortingStrategy
}

function getModifiers(orientation: navigationOrientationType) {
  const modifiers = [restrictToWindowEdges]
  if (orientation == "horizontal")
    return [...modifiers, restrictToHorizontalAxis]
  return [...modifiers, restrictToVerticalAxis]
}

export default function DefaultDNDList<T extends IgenericTab>({
  children,
  orientation = "horizontal",
  items,
  setItems,
}: IDefaultDNDListProps<T>) {
  const sensors = useSensors(
    useSensor(PointerSensor),
    useSensor(KeyboardSensor, {
      coordinateGetter: sortableKeyboardCoordinates,
    })
  );

  // ! issue: item with id "0" cant be drag
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
    <DndContext
      sensors={sensors}
      collisionDetection={closestCenter}
      onDragEnd={handleDragEnd}
      modifiers={getModifiers(orientation)}
    >
      <SortableContext
        items={items}
        strategy={getOrientation(orientation)}
      >
        {children}
      </SortableContext>
    </DndContext>
  )
}
