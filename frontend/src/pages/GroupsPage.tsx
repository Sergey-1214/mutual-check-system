import { useState } from 'react'
import { Alert, Box, Button } from '@mui/material'
import { Link } from 'react-router-dom'
import GroupCard from '../components/GroupCard'
import JoinGroupForm from '../components/JoinGroupForm'
import { PageHeader, StatCard } from '../shared/ui'
import { assignments, groups } from '../data'

function GroupsPage({ teacher = false }: { teacher?: boolean }) {
  const [joinedSecondGroup, setJoinedSecondGroup] = useState(false)
  const visibleGroups = teacher || joinedSecondGroup ? groups : groups.slice(0, 1)
  const studentsCount = new Set(groups.flatMap((group) => group.students.map((student) => student.email))).size
  const assignmentsCount = teacher
    ? assignments.length
    : assignments.filter((assignment) => visibleGroups.some((group) => group.id === assignment.groupId)).length

  function joinGroup(code: string) {
    if (code.trim().toUpperCase() !== groups[1].inviteCode || joinedSecondGroup) return false
    setJoinedSecondGroup(true)
    return true
  }

  return (
    <Box>
      <PageHeader
        title={teacher ? 'Управление группами' : 'Мои группы'}
        subtitle={teacher ? 'Создавайте группы, приглашайте студентов и назначайте задания.' : 'Группы, преподаватели и доступные вам задания.'}
        action={teacher ? <Button component={Link} to="/teacher/groups/new" variant="contained">+ Создать группу</Button> : undefined}
      />

      {!teacher && <JoinGroupForm onJoin={joinGroup} />}
      {!teacher && joinedSecondGroup && <Alert severity="success" sx={{ mb: 3 }}>Вы вступили в группу {groups[1].name}.</Alert>}

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
        <StatCard value={String(visibleGroups.length)} label={teacher ? 'учебных групп' : 'моих групп'} />
        <StatCard value={String(teacher ? studentsCount : visibleGroups.reduce((sum, group) => sum + group.students.length, 0))} label={teacher ? 'уникальных студентов' : 'одногруппников'} color="#A78BFA" />
        <StatCard value={String(assignmentsCount)} label="заданий" color="#57D3A0" />
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(2, 1fr)' }, gap: 2 }}>
        {visibleGroups.map((group) => <GroupCard key={group.id} group={group} teacher={teacher} />)}
      </Box>
    </Box>
  )
}

export default GroupsPage
