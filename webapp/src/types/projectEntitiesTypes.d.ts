// *** generic entities also represets for of "resumed" version of entities ***
declare interface IgenericEntitiesType {
  id: number
  name: string
}

declare interface IProject extends IgenericEntitiesType {
  userId: string
  // !turn into isostring date type
  created_at: string
  modified_at: string
}

declare interface ILine extends IgenericEntitiesType {
  projectId: number
  workflows: Array<IResumedWorkflow>
}

declare interface IWorkflow extends IgenericEntitiesType {
  file_link_id: number
  commands: Array<ICommand>
}

declare interface IResumedWorkflow extends IgenericEntitiesType {
}

declare interface ICommand extends IgenericEntitiesType {
  workflowId: number
  // *** stringfied json, but currently [commit 7640f54] accepts any object
  parameters: string
}

declare type listOfCommandIdsType = Array<string>

declare interface IOrderedCommandsList {
  id: string
  workflowId: string
  commandIds: listOfCommandIdsType
}
