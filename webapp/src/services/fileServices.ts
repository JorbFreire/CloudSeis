import api from "./api"

export async function listFiles(
  token: string,
  projectId: number,
): Promise<any | null> {
  try {
    const response = await api.get(
      `/su-file/list/${projectId}`,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: 'Bearer ' + token
        },
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function createFile(
  token: string,
  projectId: number,
  formData: any,
): Promise<any | null> {
  try {
    const response = await api.post(
      `/su-file/create/${projectId}`,
      formData,
      {
        headers: {
          'Content-Type': 'multipart/form-data',
          Authorization: 'Bearer ' + token
        },
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function updateFile(
  token: string,
  workflowId: number
): Promise<any | null> {
  try {
    const response = await api.put(
      `/su-file/update/${workflowId}`,
      {
        foo: "ok"
      },
      {
        headers: {
          Authorization: 'Bearer ' + token
        },
      }
    )
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
