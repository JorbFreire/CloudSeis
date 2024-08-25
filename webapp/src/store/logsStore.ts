import { create } from 'zustand'


interface ILogsStore {
  logs: Map<number, Array<string>>
  pushNewLog: (workflowId: number, newLog: string) => void
}

export const useLogsStore = create<ILogsStore>((set) => ({
  logs: new Map(),
  pushNewLog: (workflowId, newLog) => {
    set((state) => {
      const tempLogs = new Map(state.logs)
      let workflowLogs = tempLogs.get(workflowId)
      if (!workflowLogs)
        workflowLogs = []

      if (!newLog) {
        newLog = "Comando executado com sucesso, sem avisos"
      }

      workflowLogs.push(newLog)

      tempLogs.set(workflowId, workflowLogs)
      return { logs: tempLogs }
    })
  }
}))
