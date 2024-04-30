import { useState, useEffect } from 'react';
import { useNavigate } from '@tanstack/react-location';

import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableHead from '@mui/material/TableHead';
import TableRow from '@mui/material/TableRow';
import TableCell from '@mui/material/TableCell';

import { Link } from '@tanstack/react-location';

import UserMenu from 'components/UserMenu';
import { getProjectsByUserID } from 'services/projectServices';
import {
  Container,
  CustomHeadCell,
} from './styles'

export default function ProjectsList() {
  const navigate = useNavigate()
  const [projects, setProjects] = useState<Array<IProject>>([])

  useEffect(() => {
    const token = localStorage.getItem("jwt")
    token && getProjectsByUserID(token)
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

              <TableCell />
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Container>
  )
}
