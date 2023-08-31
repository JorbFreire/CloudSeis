import { suCommandsQueue } from "types/seismicUnixTypes"
import api from "./api"

export async function updateFile(
  unique_filename: string,
  seismicUnixCommandsQueue: suCommandsQueue
): Promise<ILine | null> {
  try {
    const response = await api.put<ILine>(`/su-file/${unique_filename}/filters`, {
      unique_filename,
      seismicUnixCommandsQueue
    })
    return response.data
  } catch (error) {
    console.error(error)
    return null
  }
}
