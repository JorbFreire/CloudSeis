import api from "./api"

export async function getWorkflowByID(id: string): Promise<IWorkflow | null> {
  try {
    const response = await api.get<IWorkflow>(`/workflow/show/${id}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function createNewWorkflow(lineId: string, name: string): Promise<IWorkflow | null> {
  try {
    const response = await api.post<ILine>(`/workflow/create`, {
      lineId,
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
