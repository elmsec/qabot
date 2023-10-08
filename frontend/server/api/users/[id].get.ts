export default defineEventHandler(async (event) =>{
  const id: number = parseInt(event.context.params!.id) as number
  if (!Number.isInteger(id)) {
    throw createError({
      statusCode: 400,
      statusMessage: 'ID should be an integer',
    })
  }

  return {
    id: 1,
    name: "John Doe",
  }
})
