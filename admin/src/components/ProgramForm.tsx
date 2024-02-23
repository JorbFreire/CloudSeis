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
import ProgramCommandOrFileInput from './ProgramCommandOrFileInput';
import { createNewProgram, updateProgram, deleteProgram } from '../services/programServices'
import { useProgramGroups } from '../providers/GroupsProvider'
import { useSelectedProgramCommand } from '../providers/SelectedProgramProvider'


export default function ProgramForm() {
  const { programGroups } = useProgramGroups()
  const { selectedProgram } = useSelectedProgramCommand()

  const [openGroupFormDialog, setOpenGroupFormDialog] = useState<boolean>(false)

  const [programName, setProgramName] = useState("")
  const [programDescription, setProgramDescription] = useState("")
  const [programPath, setProgramPath] = useState("")
  const [groupId, setGroupId] = useState<number | null>(null)

  const [customProgram, setCustomProgram] = useState<FileList | null>(null)

  const submitProgram = () => {
    if(!groupId) return
    const programData = {
      name: programName,
      description: programDescription,
      path_to_executable_file: programPath,
      groupId: groupId
    }
    if(selectedProgram)
      return updateProgram(
        selectedProgram.id,
        customProgram,
        programData
      )

    return createNewProgram(
      groupId,
      customProgram,
      programData
    )
  }

  useEffect(() => {
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
      <ProgramCommandOrFileInput
        programPath={programPath}
        setProgramPath={setProgramPath}
        setCustomProgram={setCustomProgram}
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
        <Button variant="contained" onClick={submitProgram}>
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
