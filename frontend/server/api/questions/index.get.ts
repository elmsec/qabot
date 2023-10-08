export default defineEventHandler(async (event) => {
  return {
    questions: [
      {
        id: '1',
        text: 'What is your favorite color?',
        answer: 'I want to know your favorite color',
        created: new Date(),
      },
      {
        id: '2',
        text: 'What is your favorite color?',
        answer: 'I want to know your favorite color',
        created: new Date(),
      },
    ],
  }
})
