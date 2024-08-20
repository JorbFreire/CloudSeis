import type { StaticTabKey } from 'enums/StaticTabKey'
// *** generic entities also represets "resumed" version of entities ***

declare global {
  interface IgenericEntitiesType {
    id: number | StaticTabKey
    name: string
  }

  interface IProject extends IgenericEntitiesType {
    userId: string
    // !turn into isostring date type
    created_at: string
    modified_at: string
  }

  interface ILine extends IgenericEntitiesType {
    projectId: number
    workflows: Array<IResumedWorkflow>
  }

  interface IWorkflow extends IgenericEntitiesType {
    file_link_id: number
    commands: Array<ICommand>
  }

  interface IResumedWorkflow extends IgenericEntitiesType {
  }

  interface ICommand extends IgenericEntitiesType {
    workflowId: number
    program_id: number
    // *** stringfied json, but currently [commit 7640f54] accepts any object
    parameters: string
  }

  type listOfCommandIdsType = Array<string>

  interface IOrderedCommandsList {
    id: string
    workflowId: string
    commandIds: listOfCommandIdsType
  }
}
