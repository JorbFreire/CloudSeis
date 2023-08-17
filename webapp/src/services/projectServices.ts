import api from "./api"

export async function getProjectsByUserID(userID: string): Promise<Array<IProject> | []> {
  try {
    const response = await api.get<Array<IProject>>(`/seismic-project/list/${userID}`)
    return response.data
  } catch (error) {
    console.error(error)
    return []
  }
}

export async function createNewProject(userID: string, name: string): Promise<IProject | null> {
  try {
    const response = await api.post<IProject>(`/seismic-project/create/${userID}`, {
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
