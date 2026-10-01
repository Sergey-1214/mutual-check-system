import { Box, Button, Chip, Typography } from '@mui/material'
import { Link } from 'react-router-dom'
import type { StudyGroup } from '../data'
import { assignments, cardSx } from '../data'

function GroupCard({ group, teacher = false }: { group: StudyGroup; teacher?: boolean }) {
  const groupAssignments = assignments.filter((item) => item.groupId === group.id)
  const path = teacher ? `/teacher/groups/${group.id}` : `/groups/${group.id}`

  return (
    <Box sx={{ ...cardSx, display: 'flex', flexDirection: 'column', minHeight: 225, boxShadow: '0 12px 30px rgba(0,0,0,.14)' }}>
      <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between', gap: 1 }}>
        <Box>
          <Typography variant="h6" sx={{ fontWeight: 800 }}>{group.name}</Typography>
          <Typography color="text.secondary" variant="body2" sx={{ mt: 0.5 }}>
            {teacher ? `${group.students.length} студентов` : `Преподаватель: ${group.teacher}`}
          </Typography>
        </Box>
        <Chip label={`${groupAssignments.length} заданий`} size="small" color="primary" variant="outlined" />
      </Box>

      {teacher && (
        <Box sx={{ mt: 2, p: 1.5, bgcolor: 'rgba(167,139,250,.08)', border: '1px solid rgba(167,139,250,.18)', borderRadius: 2 }}>
          <Typography variant="caption" color="text.secondary">Код приглашения</Typography>
          <Typography sx={{ fontWeight: 850, letterSpacing: '0.12em' }}>{group.inviteCode}</Typography>
        </Box>
      )}

      <Button component={Link} to={path} sx={{ mt: 'auto', alignSelf: 'flex-start' }}>
        {teacher ? 'Управлять группой →' : 'Открыть группу →'}
      </Button>
    </Box>
  )
}

export default GroupCard
