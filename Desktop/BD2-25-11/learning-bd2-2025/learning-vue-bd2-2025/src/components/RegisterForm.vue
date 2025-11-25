<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { registerUser } from '@/api'

const username = ref('')
const fullname = ref('')
const password = ref('')
const passwordConfirm = ref('')
const loading = ref(false)
const showPassword = ref(false)
const errorMessage = ref('')

const router = useRouter()

async function doRegister() {
  if (!username.value || !fullname.value || !password.value) {
    errorMessage.value = 'Por favor complete todos los campos'
    return
  }

  if (password.value !== passwordConfirm.value) {
    errorMessage.value = 'Las contraseñas no coinciden'
    return
  }

  loading.value = true
  errorMessage.value = ''

  try {
    await registerUser(username.value, fullname.value, password.value)
    // Redirigir al login tras registro exitoso
    router.push({ name: 'login' })
  } catch (err: any) {
    errorMessage.value = err.message || 'Error al registrar usuario. Intenta de nuevo.'
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
          <v-icon icon="mdi-account-plus" size="large" class="mr-2"></v-icon>
          Registro
        </v-card-title>

        <v-card-text class="pa-8">
          <v-form @submit.prevent="doRegister">
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
              v-model="fullname"
              label="Nombre completo"
              prepend-inner-icon="mdi-account-box"
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

            <v-text-field
              v-model="passwordConfirm"
              label="Confirmar contraseña"
              prepend-inner-icon="mdi-lock-check"
              :type="showPassword ? 'text' : 'password'"
              variant="outlined"
              color="primary"
              :disabled="loading"
              class="mb-4"
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
              Registrarse
            </v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-col>
  </v-row>
</template>

<style scoped></style>
