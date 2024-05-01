import { AxiosError } from "axios"
import api from "./api"

export async function getProjectsByUser(token: string): Promise<Array<IProject> | 401> {
  try {
    const response = await api.get<Array<IProject>>(`/project/list`, {
      headers: {
        Authorization: 'Bearer ' + token
      }
    })
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    if (axiosError.status)
      return 401
    return []
  }
}

export async function createNewProject(token: string, name: string): Promise<IProject | null> {
  console.log()
  // todo: add header and remove userId
  try {
    const response = await api.post<IProject>(
      `/project/create`,
      { name },
      {
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
