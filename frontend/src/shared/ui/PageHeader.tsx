import type { ReactNode } from 'react'
import { Box, Typography } from '@mui/material'

function PageHeader({ title, subtitle, action }: { title: string; subtitle: string; action?: ReactNode }) {
  return (
    <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: { xs: 'flex-start', sm: 'center' }, gap: 2, flexDirection: { xs: 'column', sm: 'row' }, mb: 3 }}>
      <Box>
        <Typography variant="h4" component="h1" sx={{ fontWeight: 850, letterSpacing: '-0.03em' }}>{title}</Typography>
        <Typography color="text.secondary" sx={{ mt: 0.5 }}>{subtitle}</Typography>
      </Box>
      {action}
    </Box>
  )
}

export default PageHeader
