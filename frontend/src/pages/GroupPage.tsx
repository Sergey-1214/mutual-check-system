import { Box, Button, Chip, Typography } from '@mui/material'
import { Link, Navigate, useParams } from 'react-router-dom'
import GroupMemberRow from '../components/GroupMemberRow'
import { AssignmentCard } from '../entities/assignment'
import { PageHeader, StatCard } from '../shared/ui'
import { assignments, cardSx, groups } from '../data'

function GroupPage({ teacher = false }: { teacher?: boolean }) {
  const { id } = useParams()
  const group = groups.find((item) => item.id === Number(id))

  if (!group) {
    return <Navigate to={teacher ? '/teacher/groups' : '/groups'} replace />
  }
  const groupAssignments = assignments.filter((item) => item.groupId === group.id)
  const backPath = teacher ? '/teacher/groups' : '/groups'

  return (
    <Box>
      <Button component={Link} to={backPath} sx={{ mb: 2 }}>← Все группы</Button>
      <PageHeader
        title={group.name}
        subtitle={teacher ? 'Студенты и задания учебной группы.' : `Преподаватель: ${group.teacher}`}
        action={teacher ? <Button component={Link} to={`/teacher/assignments/new?group=${group.id}`} variant="contained">+ Создать задание</Button> : <Chip label="Вы участник" color="success" />}
      />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
        <StatCard value={String(group.students.length)} label="студентов" />
        <StatCard value={String(groupAssignments.length)} label="заданий" color="#A78BFA" />
        <StatCard value={teacher ? group.inviteCode : group.teacher.split(' ')[0]} label={teacher ? 'код приглашения' : 'преподаватель'} color="#57D3A0" />
      </Box>

      {teacher && (
        <Box sx={{ ...cardSx, mb: 3, display: 'flex', justifyContent: 'space-between', alignItems: { xs: 'flex-start', sm: 'center' }, flexDirection: { xs: 'column', sm: 'row' }, gap: 2 }}>
          <Box>
            <Typography variant="h6" sx={{ fontWeight: 800 }}>Приглашение студентов</Typography>
            <Typography color="text.secondary" sx={{ mt: 0.5 }}>Отправьте студентам код <Box component="span" sx={{ fontWeight: 850, color: 'text.primary', letterSpacing: '0.1em' }}>{group.inviteCode}</Box></Typography>
          </Box>
          <Button variant="outlined" onClick={() => navigator.clipboard.writeText(group.inviteCode)}>Копировать код</Button>
        </Box>
      )}

      {teacher && (
        <Box sx={{ ...cardSx, mb: 3 }}>
          <Typography variant="h6" sx={{ fontWeight: 800, mb: 1 }}>Студенты</Typography>
          {group.students.length > 0
            ? group.students.map((member) => <GroupMemberRow key={member.id} member={member} />)
            : <Typography color="text.secondary" sx={{ py: 2 }}>В группе пока нет студентов. Отправьте им код приглашения.</Typography>}
        </Box>
      )}

      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>Задания группы</Typography>
      <Box sx={{ display: 'grid', gap: 2 }}>
        {groupAssignments.length > 0
          ? groupAssignments.map((assignment) => <AssignmentCard key={assignment.id} item={assignment} teacher={teacher} />)
          : <Box sx={cardSx}><Typography color="text.secondary">Для этой группы ещё нет заданий.</Typography></Box>}
      </Box>
    </Box>
  )
}

export default GroupPage
