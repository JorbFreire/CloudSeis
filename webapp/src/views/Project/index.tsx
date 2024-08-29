import { useEffect, useState } from 'react'


import { useGatherKeyStore } from 'store/gatherKeyStore'
import { useLogsStore } from 'store/logsStore';
import { useLinesStore } from 'store/linesStore';
import { useCommandsStore } from 'store/commandsStore';
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { updateFile } from 'services/fileServices'
import { deleteCommand } from 'services/commandServices'
import { StaticTabKey } from 'enums/StaticTabKey'

import Console from 'components/Console'
import ProgramsDrawer from 'components/ProgramsDrawer';
import ProjectTab from 'components/ProjectTab';
import CustomTabsNavigation from 'components/CustomTabsNavigation';
import DefaultDNDList from 'components/DefaultDNDList';

import FloatActions from './FloatActions';
import TabContentDisplayer from './TabContentDisplayer'
import {
  Container,
  SelectedWorkflowsContainer,
  RunButton,
} from './styles'

interface IProjectProps {
  projectId: number
}

export default function Project({ projectId }: IProjectProps) {
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId,
  } = useSelectedWorkflowsStore((state) => ({
    selectedWorkflows: state.selectedWorkflows,
    setSelectedWorkflows: state.setSelectedWorkflows,
    singleSelectedWorkflowId: state.singleSelectedWorkflowId,
    setSingleSelectedWorkflowId: state.setSingleSelectedWorkflowId,
  }))

  const pushNewLog = useLogsStore(state => state.pushNewLog)
  const gatherKeys = useGatherKeyStore((state) => state.gatherKeys)
  const [isConsoleOpen, setIsConsoleOpen] = useState(true)
  const [isOptionsDrawerOpen, setIsOptionsDrawerOpen] = useState(true)

  const loadLines = useLinesStore((state) => state.loadLines)
  const {
    commands,
    loadCommands,
    setCommands,
    selectedCommandIndex,
    setSelectedCommandIndex
  } = useCommandsStore((state) => ({
    commands: state.commands,
    loadCommands: state.loadCommands,
    setCommands: state.setCommands,
    selectedCommandIndex: state.selectedCommandIndex,
    setSelectedCommandIndex: state.setSelectedCommandIndex,
  }))

  const runWorkflow = () => {
    const token = localStorage.getItem("jwt")
    if (!token) return
    if (!singleSelectedWorkflowId) return
    updateFile(token, singleSelectedWorkflowId).then((result) => {
      if (!result) return

      pushNewLog(singleSelectedWorkflowId, result.process_output)
      if (result.process_output) return

      let vizualizerURL = `${import.meta.env.VITE_VISUALIZER_URL}/?`
      const gatherKeyFromStore = gatherKeys.get(singleSelectedWorkflowId)
      if (gatherKeyFromStore)
        vizualizerURL += `gather_key=${gatherKeyFromStore}&`
      window.open(`${vizualizerURL}workflowId=${singleSelectedWorkflowId}`, '_blank')
    })
  }

  useEffect(() => {
    loadLines(projectId)
  }, [projectId])

  useEffect(() => {
    if (!singleSelectedWorkflowId) return
    loadCommands(singleSelectedWorkflowId)
  }, [singleSelectedWorkflowId])

  return (
    <>
      <Container>
        <ProjectTab />
        <SelectedWorkflowsContainer>
          <CustomTabsNavigation
            tabs={selectedWorkflows}
            setTabs={setSelectedWorkflows}
            selectedTab={singleSelectedWorkflowId}
            setSelectedTab={setSingleSelectedWorkflowId}
            CustomDndContext={DefaultDNDList}
          >
            <CustomTabsNavigation
              tabs={[
                {
                  id: StaticTabKey.Input,
                  name: "Input"
                },
                ...commands,
                {
                  id: StaticTabKey.Output,
                  name: "Output"
                },
                {
                  id: StaticTabKey.Vizualizer,
                  name: "Visualization"
                },
              ]}
              setTabs={setCommands}
              selectedTab={selectedCommandIndex}
              setSelectedTab={setSelectedCommandIndex}
              onRemove={(selectedCommandId: number | StaticTabKey) => {
                const token = localStorage.getItem("jwt")
                if (!token) return
                deleteCommand(token, selectedCommandId.toString()).then()
              }}
              CustomDndContext={DefaultDNDList}
              color='white'
              orientation='vertical'
            >
              <TabContentDisplayer />
            </CustomTabsNavigation>
          </CustomTabsNavigation>

          <RunButton
            variant='contained'
            onClick={runWorkflow}
          >
            Run Workflow
          </RunButton>
        </SelectedWorkflowsContainer>


        <FloatActions
          isConsoleOpen={isConsoleOpen}
          setIsConsoleOpen={setIsConsoleOpen}
          isOptionsDrawerOpen={isOptionsDrawerOpen}
          setIsOptionsDrawerOpen={setIsOptionsDrawerOpen}
        />
      </Container >

      <Console isOpen={isConsoleOpen} setIsOpen={setIsConsoleOpen} />
      <ProgramsDrawer isOpen={isOptionsDrawerOpen} setIsOpen={setIsOptionsDrawerOpen} />
    </>
  )
}
