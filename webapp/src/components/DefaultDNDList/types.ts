import { Dispatch, ReactNode, SetStateAction } from "react"

// ? make tabs compatible with dnd items
// ? not needing to use tabs in every DND list
interface IgenericEntityWithOptionalName {
  name?: string;
}

type itemType = IgenericEntitiesType & IgenericEntityWithOptionalName;

type itemsListType<T extends itemType> = Array<T>

export interface IDefaultDNDListProps<T extends itemType> {
  children: ReactNode
  orientation?: navigationOrientationType
  items: itemsListType<T>
  setItems: Dispatch<SetStateAction<itemsListType<T>>>
}
