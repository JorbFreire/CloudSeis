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
    getLinesByProjectID(projectId)
      .then((result) => {
        if (Array.isArray(result))
          set({ lines: result })
      })
  },

  saveNewLine: (projectId: number, name: string) => {
    createNewLine(projectId, name)
      .then(result => {
        if (!result)
          return
        set((state) => ({ lines: [...state.lines, result] }))
      })
  },
  pushNewWorkflowToLine: (lineId: number, name: string) => {
    createNewWorkflow(lineId, "lineId", name)
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
