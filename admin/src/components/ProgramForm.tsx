import { useEffect, useState } from 'react'

import Stack from '@mui/material/Stack';
import TextField from '@mui/material/TextField'
import Select from '@mui/material/Select'
import MenuItem from '@mui/material/MenuItem'
import Button from '@mui/material/Button';
import InputLabel from '@mui/material/InputLabel';
import FormControl from '@mui/material/FormControl';

import ParameterForm from './ParameterForm';
import GroupFormDialog from './GroupFormDialog';
import { createNewProgram, deleteProgram } from '../services/programServices'
import { useProgramGroups } from '../providers/GroupsProvider'
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider'


export default function ProgramForm() {
  const { programGroups } = useProgramGroups()
  const { selectedProgram } = useSelectedProgramCommand()

  const [openGroupFormDialog, setOpenGroupFormDialog] = useState<boolean>(false)

  const [programName, setProgramName] = useState("")
  const [programDescription, setProgramDescription] = useState("")
  // todo: add checkbox to alow upload a binary file or use a command
  const [programPath, setProgramPath] = useState("")
  const [groupId, setGroupId] = useState<number | null>(null)

  useEffect(() => {
    console.log("selectedProgram.groupId")
    console.log(selectedProgram)
    console.log("***")
    if (!selectedProgram) {
      setProgramName("")
      setProgramDescription("")
      setProgramPath("")
      setGroupId(null)
      return
    }
    setProgramName(selectedProgram.name)
    setProgramDescription(selectedProgram.description)
    setProgramPath(selectedProgram.path_to_executable_file)
    setGroupId(selectedProgram.groupId)
  }, [selectedProgram])

  return (
    <Stack direction="column" sx={{ gap: "32px", padding: "32px" }} >
      <TextField
        label="Nome do Programa"
        value={programName}
        onChange={(event) => setProgramName(event.target.value)}
      />
      <TextField
        label="Descrição do Programa"
        value={programDescription}
        onChange={(event) => setProgramDescription(event.target.value)}
      />
      {/* todo: add checkbox to alow upload a binary file or use a command */}
      <TextField
        label="Commando ou caminho do Programa"
        value={programPath}
        onChange={(event) => setProgramPath(event.target.value)}
      />
      <FormControl>
        <InputLabel id="groupId-select">Grupo</InputLabel>
        <Select
          label="Grupo"
          value={groupId}
          onChange={(event) => setGroupId(event.target.value as number)}
          labelId="groupId-select"
        >
          {programGroups.map(group => (
            <MenuItem key={group.id} value={group.id}>
              {group.name}
            </MenuItem>
          ))}
          <Button onClick={() => setOpenGroupFormDialog(true)}>
            Novo Grupo
          </Button>
        </Select>
      </FormControl>

      <Stack direction="row" sx={{ gap: "8px" }} >
        <Button
          variant="contained"
          onClick={() => groupId && createNewProgram(
            groupId,
            {
              name: programName,
              description: programDescription,
              path_to_executable_file: programPath
            }
          )}
        >
          Salvar {!selectedProgram && " Novo Programa"}
        </Button>
        {selectedProgram && (
          <Button onClick={() => deleteProgram(selectedProgram.id)}>
            Apagar programa
          </Button>
        )}
      </Stack>

      <ParameterForm />

      <GroupFormDialog
        open={openGroupFormDialog}
        setOpen={setOpenGroupFormDialog}
      />
    </Stack>
  )
}
