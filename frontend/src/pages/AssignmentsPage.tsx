import { Box } from '@mui/material'
import { AssignmentCard } from '../entities/assignment'
import { PageHeader, StatCard } from '../shared/ui'
import { assignments } from '../data'

function AssignmentsPage() {
  return (
    <Box>
      <PageHeader title="Мои работы" subtitle="Все задания, сроки и результаты в одном месте." />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
        <StatCard value="3" label="всего заданий" />
        <StatCard value="1" label="нужно сдать" color="#F3B35E" />
        <StatCard value="87" label="средний балл" color="#57D3A0" />
      </Box>

      <Box sx={{ display: 'grid', gap: 2 }}>
        {assignments.map((item) => <AssignmentCard key={item.id} item={item} />)}
      </Box>
    </Box>
  )
}

export default AssignmentsPage
