export type Memo = {
  id: string
  title: string
  categories: string[]
  content: string
  createdAt: number
  updatedAt: number
}

export type Quiz = {
  id: string
  writer: string
  type: string
  count: string
  difficulty: string
}

export type Problem = {
  id: string
  quizid: string
  question: string
  answer: string
  options: string[]
}

export type User = {
  nickname: string
  accountID: string
  password: string
}
