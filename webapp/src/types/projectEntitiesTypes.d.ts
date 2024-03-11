// *** generic entities also represets for of "resumed" version of entities ***
declare interface IgenericEntitiesType {
  id: number
  name: string
}

declare interface IProject extends IgenericEntitiesType {
  userId: string
}

declare interface ILine extends IgenericEntitiesType {
  workflows: Array<IWorkflow>
}

declare interface IWorkflow extends IgenericEntitiesType {
  commands: Array<ICommand>
}

declare interface ICommand extends IgenericEntitiesType {
  // stringfied json
  parameters: string
  workflowId: number
}

declare type listOfCommandIdsType = Array<string>

declare interface IOrderedCommandsList {
  id: string
  workflowId: string
  commandIds: listOfCommandIdsType
}
