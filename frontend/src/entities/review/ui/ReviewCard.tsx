import { Box, Button, Chip, Typography } from '@mui/material'
import { Link } from 'react-router-dom'
import { cardSx, rowSx } from '../../../data'

type Review = { id: number; assignment: string; deadline: string; status: string; comment: string }

function ReviewCard({ review }: { review: Review }) {
  return (
    <Box sx={{ ...cardSx, ...rowSx, boxShadow: '0 12px 30px rgba(0,0,0,.14)' }}>
      <Box>
        <Chip label={review.status} size="small" color={review.status === 'Готово' ? 'success' : review.status === 'Новая' ? 'primary' : 'warning'} sx={{ mb: 1 }} />
        <Typography variant="h6" sx={{ fontWeight: 750 }}>{review.assignment}</Typography>
        <Typography color="text.secondary">Автор скрыт</Typography>
        <Typography variant="body2" sx={{ mt: 1 }}>Проверить до {review.deadline}</Typography>
        {review.comment && (
          <Box sx={{ mt: 1.5, p: 1.5, maxWidth: 580, bgcolor: 'rgba(87,211,160,.07)', border: '1px solid rgba(87,211,160,.12)', borderRadius: 2 }}>
            <Typography variant="caption" color="text.secondary">Комментарий</Typography>
            <Typography variant="body2">{review.comment}</Typography>
          </Box>
        )}
      </Box>
      <Button component={Link} to={`/reviews/${review.id}`} variant={review.status === 'Готово' ? 'outlined' : 'contained'}>
        {review.status === 'Новая' ? 'Начать' : review.status === 'В процессе' ? 'Продолжить' : 'Посмотреть'}
      </Button>
    </Box>
  )
}

export default ReviewCard
