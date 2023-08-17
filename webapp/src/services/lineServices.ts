import api from "./api"

export async function getLinesByProjectID(projectID: string): Promise<Array<IWorkflow> | []> {
  try {
    const response = await api.get<Array<ILine>>(`/seismic-line/list/${projectID}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewLine(projectID: string, name: string): Promise<IWorkflow | null> {
  try {
    const response = await api.post<ILine>(`/seismic-line/list/${projectID}`, {
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
