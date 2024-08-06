import { useEffect, useState } from 'react'

// Fav button icons need futter optimiation and animation
import KeyboardDoubleArrowRightRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowRightRounded';
import KeyboardDoubleArrowLeftRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowLeftRounded';
import KeyboardDoubleArrowDownRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowDownRounded';
import KeyboardDoubleArrowUpRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowUpRounded';

import { useLinesStore } from 'store/linesStore';
import { useCommandsStore } from 'store/commandsStore';
import { useSelectedWorkflowsStore } from 'store/selectedWorkflowsStore'
import { updateFile } from 'services/fileServices'
import { deleteCommand } from 'services/commandServices'

import Console from 'components/Console'
import ProgramsDrawer from 'components/ProgramsDrawer';
import ProjectTab from 'components/ProjectTab';
import CustomTabsNavigation from 'components/CustomTabsNavigation';
import CommandParameters from 'components/CommandParameters';
import DefaultDNDList from 'components/DefaultDNDList';
import InputSelectorOptions from 'components/InputSelectorOptions';

import {
  Container,
  SelectedWorkflowsContainer,
  FloatButton,
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
    if (!token)
      return
    if (!singleSelectedWorkflowId)
      return
    updateFile(token, singleSelectedWorkflowId)
  }

  useEffect(() => {
    loadLines(projectId)
  }, [projectId])

  useEffect(() => {
    if (!singleSelectedWorkflowId)
      return
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
                  id: 999999,
                  name: "Input"
                },
                ...commands,
              ]}
              setTabs={setCommands}
              selectedTab={selectedCommandIndex}
              setSelectedTab={setSelectedCommandIndex}
              onRemove={(selectedCommandId: number) => {
                const token = localStorage.getItem("jwt")
                if (!token)
                  return
                deleteCommand(token, selectedCommandId.toString()).then()
              }}
              CustomDndContext={DefaultDNDList}
              color='white'
              orientation='vertical'
            >
              {
                selectedCommandIndex && selectedCommandIndex < 999999 ? (
                  <CommandParameters
                    command={commands.find(({ id }) => id == selectedCommandIndex)}
                  />
                ) : (
                  <InputSelectorOptions />
                )
              }
            </CustomTabsNavigation>
          </CustomTabsNavigation>

          <RunButton
            variant='contained'
            onClick={runWorkflow}
          >
            Run Workflow
          </RunButton>
        </SelectedWorkflowsContainer>


        <FloatButton
          $top='16px'
          $right={isOptionsDrawerOpen ? "468px" : "16px"}
          onClick={() => setIsOptionsDrawerOpen(!isOptionsDrawerOpen)}
        >
          {isOptionsDrawerOpen ? (
            <KeyboardDoubleArrowRightRoundedIcon />
          ) : (
            <KeyboardDoubleArrowLeftRoundedIcon />
          )}
        </FloatButton>

        <FloatButton
          $bottom={isConsoleOpen ? '60px' : "16px"}
          $left='16px'
          onClick={() => setIsConsoleOpen(!isConsoleOpen)}
        >
          {isConsoleOpen ? (
            <KeyboardDoubleArrowDownRoundedIcon />
          ) : (
            <KeyboardDoubleArrowUpRoundedIcon />
          )}
        </FloatButton>
      </Container >

      <Console isOpen={isConsoleOpen} setIsOpen={setIsConsoleOpen} />
      <ProgramsDrawer
        isOpen={isOptionsDrawerOpen}
        setIsOpen={setIsOptionsDrawerOpen}
      />
    </>
  )
}
