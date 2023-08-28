declare interface IgenericEntitiesType {
  id: string
  name: string
}

declare interface IProject extends IgenericEntitiesType { }

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
