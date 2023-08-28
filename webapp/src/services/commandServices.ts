import api from "./api"

export async function createNewCommand(workflowId: string, name: string): Promise<ICommand | null> {
  try {
    const response = await api.post<ICommand>(`/command/create`, {
      workflowId,
      name
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
