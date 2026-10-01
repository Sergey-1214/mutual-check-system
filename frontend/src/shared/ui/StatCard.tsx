import { Box, Typography } from '@mui/material'

function StatCard({ value, label, color = '#72E6C4' }: { value: string; label: string; color?: string }) {
  return (
    <Box sx={{ bgcolor: 'background.paper', border: '1px solid', borderColor: 'divider', borderRadius: 3, p: 2.25, boxShadow: '0 12px 30px rgba(0,0,0,.14)', borderLeft: `4px solid ${color}` }}>
      <Typography variant="h5" sx={{ fontWeight: 850, color }}>{value}</Typography>
      <Typography variant="body2" color="text.secondary">{label}</Typography>
    </Box>
  )
}

export default StatCard
