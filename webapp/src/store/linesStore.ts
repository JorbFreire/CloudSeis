import { create } from 'zustand'

import { getLinesByProjectID } from 'services/lineServices'
import { createNewLine } from 'services/lineServices'
import { createNewWorkflow } from 'services/workflowServices'

type linesType = Array<ILine>

interface ILinesStoreState {
  lines: linesType
  loadLines: (projectId: number) => void
  pushNewWorkflowToLine: (lineId: number, name: string) => void
  saveNewLine: (projectId: number, name: string) => void
}

export const useLinesStore = create<ILinesStoreState>((set) => ({
  lines: [],
  loadLines: (projectId: number) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    getLinesByProjectID(token, projectId)
      .then((result) => {
        if (Array.isArray(result))
          set({ lines: result })
      })
  },

  saveNewLine: (projectId: number, name: string) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    createNewLine(token, projectId, name)
      .then(result => {
        if (!result)
          return
        set((state) => ({ lines: [...state.lines, result] }))
      })
  },
  pushNewWorkflowToLine: (lineId: number, name: string) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return

    createNewWorkflow(token, lineId, "lineId", name)
      .then(result => {
        if (!result)
          return
        set((state) => ({
          lines: state.lines.map((line) => {
            if (line.id == lineId)
              line.workflows.push(result)
            return line
          })
        }))
      })
  }
}))
