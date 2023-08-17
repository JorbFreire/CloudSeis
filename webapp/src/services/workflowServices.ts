import api from "./api"

export async function getWorkflowByID(id: string): Promise<IWorkflow | null> {
  try {
    const response = await api.get<IWorkflow>(`/seismic-workflow/show/${id}`)
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}

export async function createNewWorkflow(projectID: string, name: string): Promise<IWorkflow | null> {
  try {
    const response = await api.post<ILine>(`/seismic-workflow/create/${projectID}`, {
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
