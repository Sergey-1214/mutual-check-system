import { Avatar, Box, Typography } from '@mui/material'
import type { GroupMember } from '../data'

function GroupMemberRow({ member }: { member: GroupMember }) {
  const initials = member.name.split(' ').map((part) => part[0]).join('').slice(0, 2)

  return (
    <Box sx={{ display: 'grid', gridTemplateColumns: '44px minmax(160px, 1fr) minmax(190px, 1fr) auto', gap: 1.5, alignItems: 'center', py: 1.5, borderTop: '1px solid', borderColor: 'divider', overflowX: 'auto' }}>
      <Avatar sx={{ width: 38, height: 38, bgcolor: 'rgba(167,139,250,.13)', color: 'secondary.light', fontSize: 13, fontWeight: 800 }}>{initials}</Avatar>
      <Typography sx={{ fontWeight: 700 }}>{member.name}</Typography>
      <Typography variant="body2" color="text.secondary">{member.email}</Typography>
      <Typography variant="body2" color="text.secondary" sx={{ whiteSpace: 'nowrap' }}>с {member.joinedAt}</Typography>
    </Box>
  )
}

export default GroupMemberRow
