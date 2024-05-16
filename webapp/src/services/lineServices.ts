import { AxiosError } from "axios"
import api from "./api"

export async function getLinesByProjectID(
  token: string,
  projectId: number
): Promise<Array<ILine> | number> {
  try {
    const response = await api.get<Array<ILine>>(`/line/list/${projectId}`, {
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

export async function createNewLine(
  token: string,
  projectId: number,
  name: string
): Promise<ILine | null> {
  try {
    const response = await api.post<ILine>(
      `/line/create`,
      {
        projectId,
        name
      },
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
