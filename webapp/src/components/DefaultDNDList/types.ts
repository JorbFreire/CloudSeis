import { Dispatch, ReactNode, SetStateAction } from "react"

// make tabs compatible with dnd items
// not needing to use tabs in every DND list
interface IgenericEntityWithOptionalName {
  name?: string;
}

type itemType = IgenericEntitiesType & IgenericEntityWithOptionalName;

type itemsListType = Array<itemType>

export interface IDefaultDNDListProps {
  children: ReactNode
  orientation?: navigationOrientationType
  items: itemsListType
  setItems: Dispatch<SetStateAction<itemsListType>>
}
