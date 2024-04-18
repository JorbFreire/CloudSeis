import { useState } from 'react'

// Fav button icons need futter optimiation and animation
import KeyboardDoubleArrowRightRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowRightRounded';
import KeyboardDoubleArrowLeftRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowLeftRounded';
import KeyboardDoubleArrowDownRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowDownRounded';
import KeyboardDoubleArrowUpRoundedIcon from '@mui/icons-material/KeyboardDoubleArrowUpRounded';

import { useSelectedWorkflows } from 'providers/SelectedWorkflowsProvider'

import Console from 'components/Console'
import ProgramsDrawer from 'components/ProgramsDrawer';
import ProjectTab from 'components/ProjectTab';
import CustomTabsNavigation from 'components/CustomTabsNavigation';
import DefaultDNDList from 'components/DefaultDNDList';


import {
  Container,
  ProjectsContainer,
  FloatButton,
} from './styles'

interface IProjectProps {
  projectName?: string
  projectId?: string
}

export default function Project({ projectName }: IProjectProps) {
  const {
    selectedWorkflows,
    setSelectedWorkflows,
    singleSelectedWorkflowId,
    setSingleSelectedWorkflowId,
  } = useSelectedWorkflows()
  const [isConsoleOpen, setIsConsoleOpen] = useState(true)
  const [isOptionsDrawerOpen, setIsOptionsDrawerOpen] = useState(true)

  return (
    <>
      <Container>
        <ProjectTab />

        <ProjectsContainer>
          <CustomTabsNavigation
            tabs={selectedWorkflows}
            setTabs={setSelectedWorkflows}
            selectedTab={singleSelectedWorkflowId}
            setSelectedTab={setSingleSelectedWorkflowId}
            CustomDndContext={DefaultDNDList}
          />
        </ProjectsContainer>

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
