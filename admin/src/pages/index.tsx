import Grid from '@mui/material/Grid'
import { TreeView } from '@mui/x-tree-view/TreeView';
import { TreeItem } from '@mui/x-tree-view/TreeItem';

import ProgramForm from '../components/ProgramForm';
import { useProgramGroups } from '../providers/GroupsProvider'
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider'

export default function Home() {
  const { programGroups } = useProgramGroups()
  const { setSelectedProgram } = useSelectedProgramCommand()

  return (
    <Grid container sx={{ height: "100%" }}>
      <Grid item xs={2}>
        <TreeView>
          {programGroups.map(group => (
            <TreeItem
              key={`group-${group.id}`}
              nodeId={`group-${group.id}`}
              label={group.name}
            >
              {group.programs.map(program => (
                <TreeItem
                  key={`${group.id}-program-${program.id}`}
                  nodeId={`${group.id}-program-${program.id}`}
                  label={program.name}
                  onClick={() => setSelectedProgram(program)}
                />
              ))}
            </TreeItem>
          ))}
        </TreeView>
      </Grid>

      <Grid item xs={10}>
        <ProgramForm />
      </Grid>
    </Grid>
  )
}
