import { create } from 'zustand'

import {
  getLinesByProjectID,
  createNewLine,
  deleteLine,
} from 'services/lineServices'
import { createNewWorkflow, deleteWorkflow } from 'services/workflowServices'

type linesType = Array<ILine>

interface ILinesStoreState {
  lines: linesType
  loadLines: (projectId: number) => void
  saveNewLine: (projectId: number, name: string) => void
  removeLine: (lineId: number) => void
  removeWorkflowFromLine: (lineId: number, workflowId: number) => void
  pushNewWorkflowToLine: (lineId: number, name: string) => void
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
  removeLine: (lineId: number) => {
    deleteLine(lineId).then(result => {
      if (!result)
        return
      set((state) => ({
        lines: state.lines.filter((line) => line.id != lineId)
      }))
    })
  },
  removeWorkflowFromLine: (lineId: number, workflowId: number) => {
    deleteWorkflow(workflowId).then(result => {
      if (!result)
        return
      set((state) => ({
        lines: state.lines.map((line) => {
          if (line.id == lineId)
            line.workflows = line.workflows.filter((workflow) => workflow.id != workflowId)
          return line
        })
      }))
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
