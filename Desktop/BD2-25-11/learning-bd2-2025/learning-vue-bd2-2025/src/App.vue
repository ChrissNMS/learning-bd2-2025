<script setup lang="ts">
import { useAuthStore } from './stores/auth'
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const auth = useAuthStore()
const router = useRouter()

const isLoggedIn = computed(() => !!auth.token)

function logout() {
    auth.clearToken()
    router.push({ name: 'login' })
}
</script>

<template>
    <v-app>
        <v-app-bar color="primary" prominent>
            <v-app-bar-title>
                <v-icon icon="mdi-account-group" class="mr-2"></v-icon>
                User Management
            </v-app-bar-title>

            <v-spacer></v-spacer>

            <v-btn
                v-if="!isLoggedIn"
                :to="{ name: 'login' }"
                variant="text"
            >
                <v-icon icon="mdi-login" class="mr-1"></v-icon>
                Login
            </v-btn>

            <v-btn
                v-if="!isLoggedIn"
                :to="{ name: 'register' }"
                variant="text"
            >
                <v-icon icon="mdi-account-plus" class="mr-1"></v-icon>
                Register
            </v-btn>

            <template v-else>
                <v-btn
                    :to="{ name: 'home' }"
                    variant="text"
                >
                    <v-icon icon="mdi-home" class="mr-1"></v-icon>
                    Home
                </v-btn>
                <v-btn
                    @click="logout"
                    variant="text"
                >
                    <v-icon icon="mdi-logout" class="mr-1"></v-icon>
                    Cerrar sesión
                </v-btn>
            </template>
        </v-app-bar>

        <v-main>
            <v-container fluid>
                <RouterView />
            </v-container>
        </v-main>
    </v-app>
</template>

<style scoped></style>
