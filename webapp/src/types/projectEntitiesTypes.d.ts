declare interface IgenericEntitiesType {
  id: string
  name: string
}

declare interface IProject extends IgenericEntitiesType { }

declare interface ILine extends IgenericEntitiesType {
  workflows: Array<IWorkflow>
}

declare interface IWorkflow extends IgenericEntitiesType { }
