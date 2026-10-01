export const assignments = [
  { id: 1, groupId: 1, group: 'ИВТ-21', title: 'Лабораторная работа №1', course: 'Веб-разработка', deadline: '30 сентября, 23:59', status: 'Нужно сдать', submitted: 24, total: 28, reviews: 34, reviewsTotal: 48, feedback: [] },
  { id: 2, groupId: 2, group: 'ПИ-22', title: 'Лабораторная работа №2', course: 'Базы данных', deadline: '14 октября, 23:59', status: 'На проверке', submitted: 27, total: 28, reviews: 18, reviewsTotal: 54, feedback: [] },
  {
    id: 3,
    groupId: 1,
    group: 'ИВТ-21',
    title: 'Лабораторная работа №3',
    course: 'Алгоритмы',
    deadline: '28 октября, 23:59',
    status: 'Завершено',
    submitted: 28,
    total: 28,
    reviews: 56,
    reviewsTotal: 56,
    feedback: [
      { score: 90, comment: 'Алгоритмы реализованы верно, код легко читать. Стоит добавить обработку пустого массива.' },
      { score: 84, comment: 'Хорошая работа и понятный README. Не хватает теста для массива с повторяющимися значениями.' },
    ],
  },
]

export type GroupMember = {
  id: number
  name: string
  email: string
  joinedAt: string
}

export type StudyGroup = {
  id: number
  name: string
  teacher: string
  inviteCode: string
  students: GroupMember[]
}

export const groups: StudyGroup[] = [
  {
    id: 1,
    name: 'ИВТ-21',
    teacher: 'Ирина Иванова',
    inviteCode: 'IVT21WEB',
    students: [
      { id: 1, name: 'Анна Смирнова', email: 'anna@example.com', joinedAt: '12 сентября' },
      { id: 2, name: 'Максим Петров', email: 'maxim@example.com', joinedAt: '12 сентября' },
      { id: 3, name: 'Елена Кузнецова', email: 'elena@example.com', joinedAt: '13 сентября' },
      { id: 4, name: 'Даниил Волков', email: 'daniil@example.com', joinedAt: '14 сентября' },
    ],
  },
  {
    id: 2,
    name: 'ПИ-22',
    teacher: 'Ирина Иванова',
    inviteCode: 'DATABASE',
    students: [
      { id: 5, name: 'Софья Орлова', email: 'sofia@example.com', joinedAt: '16 сентября' },
      { id: 6, name: 'Артём Соколов', email: 'artem@example.com', joinedAt: '16 сентября' },
      { id: 7, name: 'Мария Лебедева', email: 'maria@example.com', joinedAt: '17 сентября' },
    ],
  },
]

export const reviews = [
  { id: 1, assignment: 'Лабораторная работа №1', deadline: '2 октября, 23:59', status: 'Новая', comment: '' },
  { id: 2, assignment: 'Лабораторная работа №2', deadline: '16 октября, 23:59', status: 'В процессе', comment: 'Хорошая структура проекта. Нужно подробнее описать запуск базы данных.' },
  { id: 3, assignment: 'Лабораторная работа №3', deadline: '30 октября, 23:59', status: 'Готово', comment: 'Алгоритмы реализованы верно, тесты покрывают основные случаи. Стоит добавить обработку пустого массива.' },
]

export const cardSx = {
  bgcolor: 'background.paper',
  border: '1px solid',
  borderColor: 'divider',
  borderRadius: 3,
  p: { xs: 2, md: 3 },
}

export const rowSx = {
  display: 'flex',
  alignItems: 'center',
  justifyContent: 'space-between',
  gap: 2,
  flexWrap: 'wrap',
}
