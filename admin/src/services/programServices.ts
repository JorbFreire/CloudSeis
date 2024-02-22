import api from "./api"

export async function getPrograms(groupId: number): Promise<Array<IGenericProgram>> {
  try {
    const response = await api.get<Array<IGenericProgram>>(`/programs/list/${groupId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewProgram(
  groupId: number,
  programData: IGenericProgramConstructor
): Promise<IGenericProgram | null> {
  try {
    const response = await api.post<IGenericProgram>(`/programs/create/${groupId}`, {
      ...programData
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function updateProgram(
  programId: number,
  programData: IGenericProgramConstructor
): Promise<IGenericProgram | null> {
  try {
    const response = await api.put<IGenericProgram>(`/programs/update/${programId}`, {
      ...programData
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function deleteProgram(programId: number): Promise<IGenericProgram | null> {
  try {
    const response = await api.delete(`/programs/delete/${programId}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
