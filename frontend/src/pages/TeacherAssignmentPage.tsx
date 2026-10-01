import { Box, Button, Typography } from '@mui/material'
import { Link, useParams } from 'react-router-dom'
import StudentRow from '../components/StudentRow'
import { PageHeader, StatCard } from '../shared/ui'
import { assignments, cardSx } from '../data'

const students = [
  ['Анна Смирнова', 'Сдано', '2 из 2', 92],
  ['Максим Петров', 'Сдано', '1 из 2', 50],
  ['Елена Кузнецова', 'Ожидает проверок', '0 из 2', 20],
  ['Даниил Волков', 'Не сдано', '0 из 2', 0],
] as const

function TeacherAssignmentPage() {
  const { id } = useParams()
  const assignment = assignments.find((item) => item.id === Number(id)) ?? assignments[0]

  return (
    <Box>
      <Button component={Link} to="/teacher/assignments" sx={{ mb: 2 }}>← Все задания</Button>
      <PageHeader title={assignment.title} subtitle={`${assignment.course} · срок ${assignment.deadline}`} />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr 1fr', md: 'repeat(3, 1fr)' }, gap: 2, mb: 2 }}>
        <StatCard value={`${assignment.submitted} из ${assignment.total}`} label="работ сдано" />
        <StatCard value={`${assignment.reviews} из ${assignment.reviewsTotal}`} label="проверок готово" color="#A78BFA" />
        <StatCard value="87" label="средний балл" color="#57D3A0" />
      </Box>

      <Box sx={cardSx}>
        <Typography variant="h6" sx={{ fontWeight: 750, mb: 1 }}>Студенты</Typography>
        {students.map(([name, status, reviews, progress]) => <StudentRow key={name} name={name} status={status} reviews={reviews} progress={progress} />)}
      </Box>
    </Box>
  )
}

export default TeacherAssignmentPage
