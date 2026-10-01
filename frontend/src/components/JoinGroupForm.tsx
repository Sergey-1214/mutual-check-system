import type { FormEvent } from 'react'
import { Box, Button, TextField, Typography } from '@mui/material'
import { cardSx } from '../data'

function JoinGroupForm({ onJoin }: { onJoin: (code: string) => boolean }) {
  function submit(event: FormEvent) {
    event.preventDefault()
    const form = event.currentTarget as HTMLFormElement
    const input = form.elements.namedItem('inviteCode') as HTMLInputElement
    input.setCustomValidity('')
    if (!onJoin(input.value)) {
      input.setCustomValidity('Группа с таким кодом не найдена')
      input.reportValidity()
      return
    }
    form.reset()
  }

  return (
    <Box component="form" onSubmit={submit} sx={{ ...cardSx, mb: 3 }}>
      <Typography variant="h6" sx={{ fontWeight: 800 }}>Вступить в новую группу</Typography>
      <Typography color="text.secondary" sx={{ mt: 0.5, mb: 2 }}>Введите код, который прислал преподаватель.</Typography>
      <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 1.5, flexWrap: 'wrap' }}>
        <TextField name="inviteCode" label="Код приглашения" placeholder="Например, DATABASE" required size="small" sx={{ flex: '1 1 240px' }} />
        <Button type="submit" variant="contained">Вступить</Button>
      </Box>
    </Box>
  )
}

export default JoinGroupForm
