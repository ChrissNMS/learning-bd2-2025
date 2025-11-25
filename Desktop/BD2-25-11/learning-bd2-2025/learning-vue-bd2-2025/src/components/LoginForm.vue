<script setup lang="ts">
import { login } from '@/api'
import { useAuthStore } from '@/stores/auth'
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const loading = ref(false)
const showPassword = ref(false)
const errorMessage = ref('')

const router = useRouter()

const emit = defineEmits<{
    (e: 'login-success', token: string): void
}>()

async function doLogin() {
    if (!username.value || !password.value) {
        errorMessage.value = 'Por favor complete todos los campos'
        return
    }

    loading.value = true
    errorMessage.value = ''
    
    try {
        const loginData = await login(username.value, password.value)
        const auth = useAuthStore()

        if (loginData) {
            username.value = ''
            password.value = ''
            auth.setToken(loginData.access_token)
            router.push({ name: 'home' })
        } else {
            errorMessage.value = 'Inicio de sesión incorrecto'
        }
    } catch (error) {
        errorMessage.value = 'Error al iniciar sesión. Por favor intente nuevamente.'
    } finally {
        loading.value = false
    }
}
</script>

<template>
    <v-row justify="center" align="center" style="min-height: 70vh;">
        <v-col cols="12" sm="8" md="6" lg="4">
            <v-card elevation="8" rounded="lg">
                <v-card-title class="text-h4 text-center bg-primary pa-6">
                    <v-icon icon="mdi-lock" size="large" class="mr-2"></v-icon>
                    Iniciar Sesión
                </v-card-title>

                <v-card-text class="pa-8">
                    <v-form @submit.prevent="doLogin">
                        <v-text-field
                            v-model="username"
                            label="Usuario"
                            prepend-inner-icon="mdi-account"
                            variant="outlined"
                            color="primary"
                            :disabled="loading"
                            class="mb-4"
                        ></v-text-field>

                        <v-text-field
                            v-model="password"
                            label="Contraseña"
                            prepend-inner-icon="mdi-lock"
                            :append-inner-icon="showPassword ? 'mdi-eye' : 'mdi-eye-off'"
                            :type="showPassword ? 'text' : 'password'"
                            variant="outlined"
                            color="primary"
                            :disabled="loading"
                            @click:append-inner="showPassword = !showPassword"
                            class="mb-2"
                        ></v-text-field>

                        <v-alert
                            v-if="errorMessage"
                            type="error"
                            variant="tonal"
                            class="mb-4"
                        >
                            {{ errorMessage }}
                        </v-alert>

                        <v-btn
                            type="submit"
                            color="primary"
                            size="large"
                            block
                            :loading="loading"
                            class="mt-4"
                        >
                            Iniciar sesión
                        </v-btn>
                    </v-form>
                </v-card-text>
            </v-card>
        </v-col>
    </v-row>
</template>
