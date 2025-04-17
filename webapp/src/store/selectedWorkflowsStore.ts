import { create } from 'zustand'

import { getWorkflowByID } from 'services/workflowServices'

type selectedWorkflowsType = Array<IWorkflow>
type singleSelectedWorkflowIdType = number | undefined

interface ISelectedWorkflowsStoreState {
  selectedWorkflows: selectedWorkflowsType
  // todo: "singleSelectedWorkflowId" shall be converted to "singleSelectedWorkflow"
  // *** this will improve performance by not needing many forEachs to get selectedWorkflow info  
  // *** at some components.
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

    getWorkflowByID(workflowId)
      .then(result => {
        if (!result)
          return

        set((state) => ({
          singleSelectedWorkflowId: result.id,
          selectedWorkflows: [
            ...state.selectedWorkflows,
            {
              id: result.id,
              name: result.name,
              file_link_id: result.file_link_id,
              commands: result.commands,
              output_name: result.output_name
            },
          ]
        }))
        afterSelect()
      })
  }
}))
