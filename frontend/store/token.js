import { ref } from 'vue'
import { defineStore } from 'pinia'

export const useTokenStore = defineStore('token', () => {
  const token = ref('')

  const runtimeConfig = useRuntimeConfig()
  const apiBaseUrl = computed(() => runtimeConfig.public.apiBaseUrl)

  async function requestToken(data) {
    const { data: result, error } = await useFetch(
      `${apiBaseUrl.value}/token`,
      {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          web_app_data: data
        })
      }
    )

    if (error.value) {
      console.error(error.value)
      return
    }

    token.value = result.value.access_token
  }

  return {
    token,
    requestToken,
  }
})
