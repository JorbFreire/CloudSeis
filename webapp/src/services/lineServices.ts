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

export async function createNewLine(projectID: string, name: string): Promise<ILine | null> {
  try {
    const response = await api.post<ILine>(`/line/list/${projectID}`, {
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
