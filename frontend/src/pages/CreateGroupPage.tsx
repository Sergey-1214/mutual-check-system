import { useState } from 'react'
import { Alert, Box, Button, TextField } from '@mui/material'
import { Link } from 'react-router-dom'
import { PageHeader } from '../shared/ui'
import { cardSx } from '../data'

function CreateGroupPage() {
  const [created, setCreated] = useState(false)

  return (
    <Box>
      <Button component={Link} to="/teacher/groups" sx={{ mb: 2 }}>← Все группы</Button>
      <PageHeader title="Новая группа" subtitle="Создайте группу и отправьте студентам код приглашения." />

      <Box component="form" sx={{ ...cardSx, display: 'grid', gap: 2 }} onSubmit={(event) => { event.preventDefault(); setCreated(true) }}>
        <TextField label="Название группы" placeholder="Например, ИВТ-21" required fullWidth />
        <Box sx={{ display: 'flex', gap: 1 }}>
          <Button type="submit" variant="contained">Создать группу</Button>
          <Button component={Link} to="/teacher/groups">Отмена</Button>
        </Box>
        {created && <Alert severity="success">Группа создана. Код приглашения: GROUP003</Alert>}
      </Box>
    </Box>
  )
}

export default CreateGroupPage
