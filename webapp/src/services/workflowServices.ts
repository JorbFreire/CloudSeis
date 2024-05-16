import api from "./api"

export async function getWorkflowByID(
  token: string,
  id: string,
): Promise<IResumedWorkflow | null> {
  try {
    const response = await api.get<IResumedWorkflow>(
      `/workflow/show/${id}`,
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

export async function createNewWorkflow(
  token: string,
  parentId: number,
  parentType: "projectId" | "lineId",
  name: string,
): Promise<IResumedWorkflow | null> {
  try {
    const response = await api.post<IResumedWorkflow>(
      `/workflow/create/${parentId}`,
      {
        parentType,
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
