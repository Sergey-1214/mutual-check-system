import { Box, Chip, LinearProgress, Typography } from '@mui/material'

function StudentRow({ name, status, reviews, progress }: { name: string; status: string; reviews: string; progress: number }) {
  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: { xs: '1fr', sm: '2fr 1.4fr 1fr 2fr' }, gap: 1, alignItems: 'center', py: 1.5, borderTop: '1px solid', borderColor: 'divider' }}>
      <Typography sx={{ fontWeight: 650 }}>{name}</Typography>
      <Chip label={status} size="small" color={progress === 0 ? 'error' : progress > 80 ? 'success' : 'default'} sx={{ justifySelf: 'start' }} />
      <Typography variant="body2">{reviews}</Typography>
      <LinearProgress variant="determinate" value={progress} sx={{ width: '100%', height: 7, borderRadius: 4 }} />
    </Box>
  )
}

export default StudentRow
