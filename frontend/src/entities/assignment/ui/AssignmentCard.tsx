import { Box, Button, Chip, LinearProgress, Typography } from '@mui/material'
import { Link } from 'react-router-dom'
import { cardSx, rowSx } from '../../../data'

type Assignment = {
  id: number
  title: string
  course: string
  group?: string
  deadline: string
  status: string
  submitted: number
  total: number
}

function AssignmentCard({ item, teacher = false }: { item: Assignment; teacher?: boolean }) {
  const progress = Math.round(item.submitted / item.total * 100)
  const chipColor = item.status === 'Завершено' ? 'success' : item.status === 'Нужно сдать' ? 'warning' : 'primary'

  return (
    <Box sx={{ ...cardSx, ...rowSx, boxShadow: '0 12px 30px rgba(0,0,0,.14)', transition: 'transform .2s ease, border-color .2s ease, box-shadow .2s ease', '&:hover': { transform: 'translateY(-2px)', borderColor: 'rgba(114,230,196,.32)', boxShadow: '0 18px 38px rgba(0,0,0,.24)' } }}>
      <Box>
        <Chip label={teacher ? (progress === 100 ? 'Завершено' : 'Активно') : item.status} size="small" color={teacher ? (progress === 100 ? 'success' : 'primary') : chipColor} sx={{ mb: 1 }} />
        <Typography variant="h6" sx={{ fontWeight: 750 }}>{item.title}</Typography>
        <Typography color="text.secondary">{item.course}{item.group ? ` · ${item.group}` : ''}</Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>Срок: {item.deadline}</Typography>
      </Box>
      {teacher ? (
        <Box sx={{ width: { xs: '100%', sm: 230 } }}>
          <Typography variant="body2" sx={{ mb: 1 }}>Сдано {item.submitted} из {item.total}</Typography>
          <LinearProgress variant="determinate" value={progress} sx={{ mb: 1.5, height: 7, borderRadius: 4 }} />
          <Button component={Link} to={`/teacher/assignments/${item.id}`} size="small">Результаты →</Button>
        </Box>
      ) : (
        <Button component={Link} to={`/assignments/${item.id}`} variant="contained">
          {item.status === 'Нужно сдать' ? 'Сдать работу' : 'Открыть'}
        </Button>
      )}
    </Box>
  )
}

export default AssignmentCard
