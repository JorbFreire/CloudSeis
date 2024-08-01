import api from "./api"

export async function createNewCommand(
  token: string,
  workflowId: number,
  name: string,
): Promise<ICommand | null> {
  try {
    const response = await api.post<ICommand>(
      `/command/create/${workflowId}`,
      {
        name,
        parameters: "[]"
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

export async function updateCommand(
  token: string,
  id: number,
  newParameters: string
): Promise<ICommand | null> {
  try {
    const response = await api.put<ICommand>(
      `/command/update/${id}`,
      {
        parameters: newParameters
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

export async function updateCommandsOrder(
  workflowId: string,
  newOrder: listOfCommandIdsType
): Promise<IOrderedCommandsList | null> {
  try {
    const response = await api.put<IOrderedCommandsList>(`/command/order`, {
      workflowId,
      newOrder
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
