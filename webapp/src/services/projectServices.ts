import { AxiosError } from "axios"
import api from "./api"

export async function getProjectsByUser(token: string): Promise<Array<IProject> | number> {
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
    if (axiosError.status === 401)
      return axiosError.status
    return []
  }
}

export async function createNewProject(token: string, name: string): Promise<IProject | null> {
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

export async function deleteProject(token: string, id: number): Promise<IProject | number> {
  try {
    const response = await api.delete<IProject>(
      `/project/delete/${id}`,
      {
        headers: {
          Authorization: 'Bearer ' + token
        }
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    const axiosError = error as AxiosError
    if (axiosError.status === 401)
      return axiosError.status
    return 400
  }
}
