import { useState } from 'react'
import { Box, Button, Chip, TextField, Typography } from '@mui/material'
import { Link, useParams } from 'react-router-dom'
import { PageHeader } from '../shared/ui'
import { cardSx, reviews } from '../data'

const criteria = [['Корректность решения', 40], ['Качество кода', 30], ['Тесты и документация', 30]] as const

function ReviewPage() {
  const { id } = useParams()
  const review = reviews.find((item) => item.id === Number(id)) ?? reviews[0]
  const [sent, setSent] = useState(false)
  const [comment, setComment] = useState(review.comment)
  const completed = review.status === 'Готово' || sent

  return (
    <Box>
      <Button component={Link} to="/reviews" sx={{ mb: 2 }}>← Все проверки</Button>
      <PageHeader title={review.assignment} subtitle={`Анонимная проверка · срок ${review.deadline}`} action={<Chip label="Автор скрыт" />} />

      <Box sx={{ ...cardSx, mb: 2, display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 2, flexWrap: 'wrap' }}>
        <Box><Typography sx={{ fontWeight: 750 }}>student-work.zip</Typography><Typography variant="body2" color="text.secondary">Сначала изучите работу, затем заполните рубрику.</Typography></Box>
        <Button variant="outlined">Скачать работу</Button>
      </Box>

      {completed ? (
        <Box sx={cardSx}>
          <Chip label="Отзыв отправлен" color="success" size="small" sx={{ mb: 2 }} />
          <Typography variant="h6" sx={{ fontWeight: 750 }}>Итоговая оценка: 87 из 100</Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 1.5, my: 2 }}>
            {[['Корректность', '36 / 40'], ['Качество кода', '25 / 30'], ['Тесты', '26 / 30']].map(([name, score]) => (
              <Box key={name} sx={{ p: 1.5, bgcolor: 'rgba(87,211,160,.07)', borderRadius: 2 }}>
                <Typography variant="caption" color="text.secondary">{name}</Typography>
                <Typography sx={{ fontWeight: 750 }}>{score}</Typography>
              </Box>
            ))}
          </Box>
          <Typography variant="body2" color="text.secondary">Комментарий</Typography>
          <Typography sx={{ mt: 0.5 }}>{comment || 'Комментарий не оставлен.'}</Typography>
        </Box>
      ) : (
        <Box sx={cardSx}>
          <Typography variant="h6" sx={{ fontWeight: 750, mb: 2 }}>Рубрика оценки</Typography>
          {criteria.map(([name, max]) => (
            <Box key={name} sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 2, py: 1.5, borderTop: '1px solid', borderColor: 'divider' }}>
              <Typography>{name} (до {max})</Typography>
              <TextField type="number" size="small" slotProps={{ htmlInput: { min: 0, max } }} sx={{ width: 90 }} />
            </Box>
          ))}
          <TextField label="Что сделано хорошо и что улучшить" value={comment} onChange={(event) => setComment(event.target.value)} multiline rows={4} fullWidth sx={{ my: 2 }} />
          <Button variant="contained" onClick={() => setSent(true)}>Отправить отзыв</Button>
        </Box>
      )}
    </Box>
  )
}

export default ReviewPage
