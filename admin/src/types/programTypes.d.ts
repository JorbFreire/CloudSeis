declare interface IParameter {
  id: number
  name: string
  description: string
  input_type: string
  // *** "hasChanges" shall not be sent to database ***
  hasChanges?: boolean
}

interface IGenericProgramConstructor {
  name: string
  description: string
  path_to_executable_file: string
  groupId: number
}

declare interface IGenericProgram extends IGenericProgramConstructor {
  id: number
  // parameters: Array<IParameter>
}

declare interface IProgramsGroupConstructor {
  name: string
  description: string
}

  declare interface IProgramsGroup extends IProgramsGroupConstructor {
  id: number
  programs: Array<IGenericProgram>  
}

