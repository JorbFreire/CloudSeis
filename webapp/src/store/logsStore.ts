import { create } from 'zustand'


interface ILogsStore {
  logs: Array<string>
  loadLogs: () => void
  updateLogs: () => void
}

export const useLogsStore = create<ILogsStore>((set) => ({
  logs: [""],
  loadLogs: () => {
    set({ logs: [""] })
  },
  updateLogs: () => {
    set({ logs: [""] })
  },
}))
