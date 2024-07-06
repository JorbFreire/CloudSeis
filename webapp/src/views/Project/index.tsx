import { useEffect, useState } from 'react'
import { useNavigate } from '@tanstack/react-location';

// Fav button icons need futter optimiation and animation
import KeyboardDoubleArrowRightRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowRightRounded';
import KeyboardDoubleArrowLeftRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowLeftRounded';
import KeyboardDoubleArrowDownRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowDownRounded';
import KeyboardDoubleArrowUpRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowUpRounded';

import { useLinesStore } from 'store/linesStore';
import { useSelectedWorkflows } from 'providers/SelectedWorkflowsProvider'
import { useCommands } from 'providers/CommandsProvider';
import { useSelectedCommandIndex } from 'providers/SelectedCommandProvider';

import Console from 'components/Console'
import ProgramsDrawer from 'components/ProgramsDrawer';
import ProjectTab from 'components/ProjectTab';
import CustomTabsNavigation from 'components/CustomTabsNavigation';
import CommandParameters from 'components/CommandParameters';
import DefaultDNDList from 'components/DefaultDNDList';

import { getWorkflowByID } from 'services/workflowServices'

import {
  Container,
  SelectedWorkflowsContainer,
  FloatButton,
} from './styles'

interface IProjectProps {
  projectId: number
}

export default function Project({ projectId }: IProjectProps) {
  const navigate = useNavigate()
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId,
  } = useSelectedWorkflows()
  const [isConsoleOpen, setIsConsoleOpen] = useState(true)
  const [isOptionsDrawerOpen, setIsOptionsDrawerOpen] = useState(true)

  const loadLines = useLinesStore((state) => state.loadLines)
  const { commands, setCommands } = useCommands()
  const { selectedCommandIndex, setSelectedCommandIndex } = useSelectedCommandIndex()

  useEffect(() => {
    loadLines(projectId)
  }, [projectId])

  useEffect(() => {
    if (!singleSelectedWorkflowId)
      return
    const token = localStorage.getItem("jwt")
    if (!token)
      return navigate({ to: "/login" })
    getWorkflowByID(token, singleSelectedWorkflowId)
      .then((result) => {
        if (!result)
          return
        if (result === 401)
          return navigate({ to: "/login" })

        setCommands([...result.commands])
        if (result.commands.length < 1)
          return;
        setSelectedCommandIndex(result.commands[0].id)
      })
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
              tabs={commands}
              setTabs={setCommands}
              selectedTab={selectedCommandIndex}
              setSelectedTab={setSelectedCommandIndex}
              CustomDndContext={DefaultDNDList}
              color='white'
              orientation='vertical'
            >
              {
                selectedCommandIndex && (
                  <CommandParameters
                    command={commands.find(({ id }) => id == selectedCommandIndex)}
                  />
                )
              }
            </CustomTabsNavigation>
          </CustomTabsNavigation>
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
