import { createContext, useContext, useState } from 'react'
import type { ReactNode, Dispatch, SetStateAction } from 'react'

import { createNewLine } from 'services/lineServices'
import { createNewWorkflow } from 'services/workflowServices'

type linesType = Array<ILine>
type setlinesType = Dispatch<SetStateAction<linesType>>
type saveNewLineType = (projectId: number, name: string) => void | undefined
type pushNewWorkflowToLineType = (lineId: number, name: string) => void | undefined

type uselinesType = {
  lines: linesType,
  setLines: setlinesType,
  saveNewLine: saveNewLineType
  pushNewWorkflowToLine: pushNewWorkflowToLineType
}

interface ILinesProviderProps {
  children: ReactNode | Array<ReactNode>
}

interface ILinesProviderContext {
  lines: linesType
  setLines: setlinesType
  saveNewLine: saveNewLineType
  pushNewWorkflowToLine: pushNewWorkflowToLineType
}

const LinesProviderContext = createContext<ILinesProviderContext>({
  lines: [],
  setLines: () => undefined,
  saveNewLine: () => undefined,
  pushNewWorkflowToLine: () => undefined,
});

export default function LinesProvider({ children }: ILinesProviderProps) {
  const [lines, setLines] = useState<linesType>([])


  const openNewLineDialog = (projectId: number) => {
    // todo: put into a component
    // todo: open modal, create empty or baser or copy a line from other project
  }

  const saveNewLine = (projectId: number, name: string) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return
    createNewLine(token, projectId, name)
      .then(result => {
        if (!result)
          return
        setLines([...lines, result])
      })
  }

  const pushNewWorkflowToLine = (lineId: number, name: string) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return

    createNewWorkflow(token, lineId, "lineId", name)
      .then(result => {
        if (!result)
          return
        const tempLines = lines.map((line) => {
          if (line.id == lineId)
            line.workflows.push(result)
          return line
        })
        setLines([...tempLines])
      })
  }

  return (
    <LinesProviderContext.Provider
      value={{
        lines,
        setLines,
        saveNewLine,
        pushNewWorkflowToLine,
      }}
    >
      {children}
    </LinesProviderContext.Provider>
  )
}

export function useLines(): uselinesType {
  const context = useContext(LinesProviderContext)
  if (!context)
    throw new Error('useLines must be used within a LinesProvider')
  const {
    lines,
    setLines,
    saveNewLine,
    pushNewWorkflowToLine,
  } = context
  return {
    lines,
    setLines,
    saveNewLine,
    pushNewWorkflowToLine,
  }
}
