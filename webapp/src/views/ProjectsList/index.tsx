import { useState, useEffect } from 'react';
import { useNavigate } from '@tanstack/react-location';
import { Link } from '@tanstack/react-location';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';
import IconButton from '@mui/material/IconButton'

import DeleteRoundedIcon from '@mui/icons-material/DeleteRounded'

import UserMenu from 'components/UserMenu';
import { getProjectsByUser } from 'services/projectServices';
import NewProjectDialog from './NewProjectDialog';
import {
  Container,
  CustomHeadCell,
} from './styles'

export default function ProjectsList() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState<Array<IProject>>([])

  const pushNewProject = (newProject: IProject) => {
    setProjects([...projects, newProject])
  }

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    if (!token)
      return navigate({ to: "/login" })
    getProjectsByUser(token)
      .then((result) => {
        if (result === 401)
          return navigate({ to: "/login" })
        setProjects(result)
      })
  }, [])

  return (
    <Container>
      <Table stickyHeader	>
        <TableHead>
          <TableRow>
            <CustomHeadCell>
              Name
            </CustomHeadCell>

            <CustomHeadCell>
              Created at
            </CustomHeadCell>

            <CustomHeadCell>
              Last modified at
            </CustomHeadCell>

            <CustomHeadCell align="right">
              <UserMenu />
            </CustomHeadCell>
          </TableRow>
        </TableHead>

        <TableBody>
          {projects.map((project) => (
            <TableRow
              key={project.id}
              hover
            >
              <TableCell>
                <Link to={`/projects/${project.id}`}>
                  {project.name}
                </Link>
              </TableCell>

              <TableCell>
                {project.created_at}
              </TableCell>

              <TableCell>
                {project.modified_at}
              </TableCell>

              <TableCell>
                <IconButton onClick={() => console.log("delete project")}>
                  <DeleteRoundedIcon />
                </IconButton>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>

      <NewProjectDialog pushNewProject={pushNewProject} />
    </Container>
  )
}
