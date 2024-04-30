import { AxiosError } from "axios"
import api from "./api"

export async function getProjectsByUserID(userID: string): Promise<Array<IProject> | 401> {
  try {
    const response = await api.get<Array<IProject>>(`/project/list/${userID}`)
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    if (axiosError.status)
      return 401
    return []
  }
}

export async function createNewProject(userID: string, name: string): Promise<IProject | null> {
  try {
    const response = await api.post<IProject>(`/project/create/${userID}`, {
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
