import { Box, Button } from '@mui/material'
import { Link } from 'react-router-dom'
import { AssignmentCard } from '../entities/assignment'
import { PageHeader, StatCard } from '../shared/ui'
import { assignments } from '../data'

function TeacherAssignmentsPage() {
  return (
    <Box>
      <PageHeader
        title="Управление заданиями"
        subtitle="Создавайте задания и следите за сдачей."
        action={<Button component={Link} to="/teacher/assignments/new" variant="contained">+ Создать задание</Button>}
      />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
        <StatCard value="3" label="всего заданий" />
        <StatCard value="2" label="активных" color="#A78BFA" />
        <StatCard value="79" label="работ сдано" color="#57D3A0" />
      </Box>

      <Box sx={{ display: 'grid', gap: 2 }}>
        {assignments.map((item) => <AssignmentCard key={item.id} item={item} teacher />)}
      </Box>
    </Box>
  )
}

export default TeacherAssignmentsPage
