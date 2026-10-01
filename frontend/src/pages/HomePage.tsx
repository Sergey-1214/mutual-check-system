import { Box, Button, Chip, Typography } from '@mui/material'
import { Link } from 'react-router-dom'
import { StatCard } from '../shared/ui'
import { cardSx } from '../data'

const sections = [
  {
    number: '01',
    title: 'Сдавайте работы',
    text: 'Следите за сроками, загружайте файлы и получайте итоговые оценки.',
    action: 'Мои работы',
    path: '/assignments',
  },
  {
    number: '02',
    title: 'Проверяйте анонимно',
    text: 'Оценивайте работы других студентов по общей рубрике и оставляйте комментарии.',
    action: 'Мои проверки',
    path: '/reviews',
  },
  {
    number: '03',
    title: 'Управляйте курсом',
    text: 'Создавайте задания и наблюдайте за прогрессом группы в одном месте.',
    action: 'Задания курса',
    path: '/teacher/assignments',
  },
]

function HomePage() {
  return (
    <Box>
      <Box sx={{ position: 'relative', overflow: 'hidden', color: 'text.primary', background: 'linear-gradient(135deg, #111B20 0%, #142A29 50%, #191729 100%)', border: '1px solid', borderColor: 'rgba(114,230,196,.2)', borderRadius: { xs: 3, md: 5 }, px: { xs: 3, md: 6 }, py: { xs: 5, md: 7 }, mb: 3, boxShadow: '0 24px 60px rgba(0,0,0,.32)' }}>
        <Box sx={{ position: 'absolute', inset: 0, opacity: .16, backgroundImage: 'linear-gradient(rgba(114,230,196,.16) 1px, transparent 1px), linear-gradient(90deg, rgba(114,230,196,.16) 1px, transparent 1px)', backgroundSize: '44px 44px', maskImage: 'linear-gradient(90deg, transparent 25%, black)' }} />
        <Box sx={{ position: 'absolute', width: 310, height: 310, borderRadius: '50%', border: '64px solid rgba(167,139,250,.09)', right: -90, top: -115 }} />
        <Box sx={{ position: 'absolute', width: 110, height: 110, borderRadius: '28% 72% 60% 40%', bgcolor: 'rgba(114,230,196,.14)', right: '25%', bottom: -60, transform: 'rotate(24deg)' }} />
        <Chip label="Система взаимных проверок" sx={{ position: 'relative', mb: 2, bgcolor: 'rgba(114,230,196,.12)', color: 'primary.light', border: '1px solid rgba(114,230,196,.28)' }} />
        <Typography variant="h3" component="h1" sx={{ position: 'relative', maxWidth: 700, fontWeight: 800, lineHeight: 1.04, letterSpacing: '-0.04em', fontSize: { xs: '2.35rem', md: '3.35rem' } }}>
          Учитесь на своих работах и обратной связи одногруппников
        </Typography>
        <Typography sx={{ position: 'relative', maxWidth: 650, mt: 2, mb: 3, color: 'text.secondary', fontSize: 17 }}>
          PeerReview помогает сдавать задания, проводить анонимные проверки по понятным критериям и видеть прогресс всего курса.
        </Typography>
        <Button component={Link} to="/assignments" variant="contained" sx={{ position: 'relative' }}>
          Перейти к работам
        </Button>
      </Box>

      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: 'repeat(3, 1fr)' }, gap: 2, mb: 3 }}>
        <StatCard value="3" label="активных задания" />
        <StatCard value="2" label="проверки на работу" color="#A78BFA" />
        <StatCard value="87" label="средний балл курса" color="#57D3A0" />
      </Box>

      <Typography variant="h5" sx={{ fontWeight: 800, mb: 2 }}>Как работает платформа</Typography>
      <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', md: 'repeat(3, 1fr)' }, gap: 2 }}>
        {sections.map((section) => (
          <Box key={section.number} sx={{ ...cardSx, position: 'relative', overflow: 'hidden', display: 'flex', flexDirection: 'column', minHeight: 230, boxShadow: '0 12px 34px rgba(0,0,0,.16)', '&::after': { content: '""', position: 'absolute', width: 70, height: 70, borderRadius: '50%', bgcolor: section.number === '01' ? 'rgba(114,230,196,.08)' : section.number === '02' ? 'rgba(167,139,250,.09)' : 'rgba(87,211,160,.08)', right: -24, top: -24 } }}>
            <Typography variant="body2" sx={{ color: section.number === '02' ? 'secondary.main' : section.number === '03' ? 'success.main' : 'primary.main', fontWeight: 850 }}>{section.number}</Typography>
            <Typography variant="h6" sx={{ fontWeight: 750, mt: 1 }}>{section.title}</Typography>
            <Typography color="text.secondary" sx={{ mt: 1, mb: 2, flexGrow: 1 }}>{section.text}</Typography>
            <Button component={Link} to={section.path} sx={{ alignSelf: 'flex-start' }}>{section.action} →</Button>
          </Box>
        ))}
      </Box>
    </Box>
  )
}

export default HomePage
