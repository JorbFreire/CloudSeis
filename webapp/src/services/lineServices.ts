import api from "./api"

export async function getLinesByProjectID(projectID: string): Promise<Array<ILine> | []> {
  try {
    const response = await api.get<Array<ILine>>(`/line/list/${projectID}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewLine(projectId: string, name: string): Promise<ILine | null> {
  try {
    const response = await api.post<ILine>(`/line/create`, {
      projectId,
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
