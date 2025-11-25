import { defineStore } from 'pinia'
import { ref, type Ref } from 'vue'

export const useAuthStore = defineStore('auth', () => {
    const token: Ref<string | null> = ref(localStorage.getItem('token') || null)

    function setToken(newToken: string) {
        token.value = newToken
        localStorage.setItem('token', newToken)
    }

    function clearToken() {
        token.value = null
        localStorage.removeItem('token')
    }

    return {
        token,
        setToken,
        clearToken,
    }
})
