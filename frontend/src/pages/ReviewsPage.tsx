import { Box } from '@mui/material'
import { ReviewCard } from '../entities/review'
import { PageHeader, StatCard } from '../shared/ui'
import { reviews } from '../data'

function ReviewsPage() {
  return (
    <Box>
      <PageHeader title="Мои проверки" subtitle="Все назначенные вам анонимные работы." />

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
        <StatCard value="3" label="назначено" />
        <StatCard value="2" label="осталось выполнить" color="#F3B35E" />
        <StatCard value="1" label="завершено" color="#57D3A0" />
      </Box>

      <Box sx={{ display: 'grid', gap: 2 }}>
        {reviews.map((review) => <ReviewCard key={review.id} review={review} />)}
      </Box>
    </Box>
  )
}

export default ReviewsPage
