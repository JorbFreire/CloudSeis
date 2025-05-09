import { useState } from "react"

import { useSelectedWorkflowsStore } from "store/selectedWorkflowsStore"
import { useGatherKeyStore } from "store/gatherKeyStore"
import { useLogsStore } from "store/logsStore"
import { updateFile } from 'services/fileServices'

import { CommandActionButtonStyled } from './styles'

export default function RunWorkflowButton() {
  const {
    singleSelectedWorkflowId,
  } = useSelectedWorkflowsStore((state) => ({
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
  }))
  const gatherKeys = useGatherKeyStore((state) => state.gatherKeys)
  const pushNewLog = useLogsStore(state => state.pushNewLog)

  const [isLoading, setIsLoading] = useState(false)

  const runWorkflow = () => {
    setIsLoading(true)
    if (!singleSelectedWorkflowId) return
    updateFile(singleSelectedWorkflowId).then((result) => {
      if (!result) return

      pushNewLog(singleSelectedWorkflowId, result)

      let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
      const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
      if (gatherKeyFromStore)
        vizualizerURL += `gather_key=${gatherKeyFromStore}&`
      window.open(`${vizualizerURL}workflowId=${singleSelectedWorkflowId}`, '_blank')
    }).finally(() => {
      setIsLoading(false)
    })
  }

  return (
    <CommandActionButtonStyled
      color="primary"
      variant="outlined"
      onClick={runWorkflow}
      loading={isLoading}
    >
      Run workflow
    </CommandActionButtonStyled>
  )
}
