import { create } from 'zustand'

import { getWorkflowByID } from 'services/workflowServices'

type selectedWorkflowsType = Array<IWorkflow>
type singleSelectedWorkflowIdType = number | undefined

interface ISelectedWorkflowsStoreState {
  selectedWorkflows: selectedWorkflowsType
  singleSelectedWorkflowId: singleSelectedWorkflowIdType
  setSelectedWorkflows: (newWorkflows: selectedWorkflowsType) => void
  setSingleSelectedWorkflowId: (newWorkflowId: singleSelectedWorkflowIdType) => void
  selectWorkflow: (
    workflowId: number,
    afterSelect: () => any
  ) => void
}

export const useSelectedWorkflowsStore = create<ISelectedWorkflowsStoreState>((set, get) => ({
  selectedWorkflows: [],
  singleSelectedWorkflowId: undefined,

  setSelectedWorkflows: (newWorkflow) =>
    set({ selectedWorkflows: newWorkflow }),
  setSingleSelectedWorkflowId: (newWorkflowId) =>
    set({ singleSelectedWorkflowId: newWorkflowId }),

  selectWorkflow: (workflowId: number, afterSelect) => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return

    if (get().singleSelectedWorkflowId != undefined) {
      const isAlredySingleSelected = workflowId == get().singleSelectedWorkflowId;
      if (isAlredySingleSelected)
        return
    }

    const isAlredySelected = get().selectedWorkflows.findIndex(
      (element) => element.id == workflowId
    ) >= 0

    if (isAlredySelected) {
      set({
        singleSelectedWorkflowId: workflowId
      })
      afterSelect()
      return
    }

    getWorkflowByID(token, workflowId)
      .then(result => {
        if (!result)
          return
        if (result === 401)
          return
        set((state) => ({
          singleSelectedWorkflowId: result.id,
          selectedWorkflows: [
            ...state.selectedWorkflows,
            {
              id: result.id,
              name: result.name,
              file_name: result.file_name,
              commands: result.commands
            },
          ]
        }))
        afterSelect()
      })
  }
}))
