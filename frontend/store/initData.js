import { ref, reactive } from 'vue'
import { defineStore } from 'pinia'

export const useInitDataStore = defineStore('initData', () => {
  const authDate = ref('')
  const chatInstance = ref('')
  const chatType = ref('')
  const hash = ref('')
  const user = reactive({
    id: 0,
    first_name: '',
    last_name: '',
    username: '',
    language_code: '',
    chat_type: '',
    chat_instance: '',
    auth_date: '',
    hash: '',
    allows_write_to_pm: false
  })

  function setUser(data) {
    user.id = data.id
    user.first_name = data.first_name
    user.last_name = data.last_name
    user.username = data.username
    user.language_code = data.language_code
    user.chat_type = data.chat_type
    user.chat_instance = data.chat_instance
    user.auth_date = data.auth_date
    user.hash = data.hash
    user.allows_write_to_pm = data.allows_write_to_pm
  }


  return {
    user,
    setUser,
    authDate,
    chatInstance,
    chatType,
    hash
  }
})
