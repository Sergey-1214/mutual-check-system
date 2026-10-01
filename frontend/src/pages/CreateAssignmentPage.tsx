import { useState } from 'react'
import { Box, Button, MenuItem, TextField, Typography } from '@mui/material'
import { Link, useSearchParams } from 'react-router-dom'
import { PageHeader } from '../shared/ui'
import { cardSx, groups } from '../data'

function CreateAssignmentPage() {
  const [created, setCreated] = useState(false)
  const [searchParams] = useSearchParams()
  const requestedGroup = Number(searchParams.get('group'))
  const defaultGroupId = groups.some((group) => group.id === requestedGroup)
    ? requestedGroup
    : groups[0]?.id ?? ''

  return (
    <Box>
      <Button component={Link} to="/teacher/assignments" sx={{ mb: 2 }}>← Все задания</Button>
      <PageHeader title="Новое задание" subtitle="Заполните основные параметры. Их можно будет изменить позже." />

      <Box component="form" sx={{ ...cardSx, display: 'grid', gap: 2 }} onSubmit={(event) => { event.preventDefault(); setCreated(true) }}>
        <TextField label="Название" required fullWidth />
        <TextField select label="Учебная группа" required defaultValue={defaultGroupId} helperText="Задание увидят только студенты выбранной группы">
          {groups.map((group) => <MenuItem key={group.id} value={group.id}>{group.name} · {group.students.length} студентов</MenuItem>)}
        </TextField>
        <TextField label="Предмет" required fullWidth />
        <TextField label="Описание задания" required multiline rows={4} fullWidth />
        <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '1fr 1fr' }, gap: 2 }}>
          <TextField label="Срок сдачи" type="datetime-local" required slotProps={{ inputLabel: { shrink: true } }} />
          <TextField label="Срок проверки" type="datetime-local" required slotProps={{ inputLabel: { shrink: true } }} />
        </Box>
        <TextField label="Количество проверок на работу" type="number" defaultValue={2} slotProps={{ htmlInput: { min: 1, max: 5 } }} />
        <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
          <Button type="submit" variant="contained">Создать задание</Button>
          <Button component={Link} to="/teacher/assignments" variant="text">Отмена</Button>
        </Box>
        {created && <Typography color="success.main">Задание создано и добавлено в список.</Typography>}
      </Box>
    </Box>
  )
}

export default CreateAssignmentPage
