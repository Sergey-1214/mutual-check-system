import { useState } from 'react'
import { Box, Button, Chip, TextField, Typography } from '@mui/material'
import { Link, useParams } from 'react-router-dom'
import { PageHeader } from '../shared/ui'
import { assignments, cardSx } from '../data'

function AssignmentPage() {
  const { id } = useParams()
  const assignment = assignments.find((item) => item.id === Number(id)) ?? assignments[0]
  const [file, setFile] = useState('Файл не выбран')
  const [sent, setSent] = useState(false)

  return (
    <Box>
      <Button component={Link} to="/assignments" sx={{ mb: 2 }}>← Все работы</Button>
      <PageHeader title={assignment.title} subtitle={`${assignment.course} · срок ${assignment.deadline}`} action={<Chip label={assignment.status} color="primary" />} />

      <Box sx={{ ...cardSx, mb: 2 }}>
        <Typography variant="h6" sx={{ fontWeight: 750, mb: 1 }}>Что нужно сделать</Typography>
        <Typography color="text.secondary">Загрузить архив проекта, добавить README и кратко описать результат. После срока работу анонимно проверят два студента.</Typography>
      </Box>

      {assignment.status === 'Нужно сдать' && (
        <Box sx={cardSx}>
          <Typography variant="h6" sx={{ fontWeight: 750, mb: 2 }}>Отправка работы</Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, flexWrap: 'wrap', mb: 2 }}>
            <Button component="label" variant="outlined">
              Выбрать файл
              <Box component="input" type="file" hidden onChange={(event) => setFile(event.currentTarget.files?.[0]?.name ?? 'Файл не выбран')} />
            </Button>
            <Typography variant="body2" color="text.secondary">{file}</Typography>
          </Box>
          <TextField label="Комментарий" multiline rows={3} fullWidth sx={{ mb: 2 }} />
          <Button variant="contained" disabled={file === 'Файл не выбран'} onClick={() => setSent(true)}>Отправить работу</Button>
          {sent && <Typography color="success.main" sx={{ mt: 2 }}>Работа отправлена. Теперь она появится в списке проверок у другого студента.</Typography>}
        </Box>
      )}

      {assignment.status === 'На проверке' && (
        <Box sx={cardSx}>
          <Typography variant="h6" sx={{ fontWeight: 750, mb: 1 }}>Работа отправлена</Typography>
          <Typography color="text.secondary">project.zip · получен 1 отзыв из 2. Итог появится после завершения всех проверок.</Typography>
        </Box>
      )}

      {assignment.status === 'Завершено' && (
        <Box sx={cardSx}>
          <Typography variant="h6" sx={{ fontWeight: 750 }}>Результат: 87 из 100</Typography>
          <Typography color="text.secondary" sx={{ mt: 1, mb: 2 }}>Получено два анонимных отзыва. Работа принята.</Typography>
          {assignment.feedback.map((item, index) => (
            <Box key={item.comment} sx={{ p: 2, mt: 1.5, bgcolor: 'rgba(167,139,250,.07)', borderRadius: 2, borderLeft: '3px solid', borderLeftColor: 'secondary.main' }}>
              <Typography variant="body2" sx={{ fontWeight: 750 }}>Отзыв №{index + 1} · {item.score} баллов</Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>{item.comment}</Typography>
            </Box>
          ))}
        </Box>
      )}
    </Box>
  )
}

export default AssignmentPage
