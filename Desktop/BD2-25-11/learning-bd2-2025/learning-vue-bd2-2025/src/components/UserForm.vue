<script setup lang="ts">
import type { User } from '@/interfaces'
import { ref, watch } from 'vue'
import { useRouter } from 'vue-router'

const props = defineProps<{
    inputUserData?: User | null
}>()
const emit = defineEmits<{
    (e: 'save-user', user: User): void
}>()

const router = useRouter()
const userData = ref({
    username: '',
    fullname: '',
})
const loading = ref(false)

watch(props, () => {
    if (props.inputUserData) {
        userData.value.username = props.inputUserData.username
        userData.value.fullname = props.inputUserData.fullname
    }
}, { immediate: true })

async function saveUser() {
    loading.value = true
    try {
        emit('save-user', {
            username: userData.value.username,
            fullname: userData.value.fullname,
        } as User)
    } finally {
        loading.value = false
    }
}

function cancel() {
    router.push({ name: 'home' })
}
</script>

<template>
    <v-container>
        <v-row justify="center">
            <v-col cols="12" md="8" lg="6">
                <v-card elevation="4">
                    <v-card-title class="bg-primary pa-6">
                        <v-icon icon="mdi-account-edit" size="large" class="mr-3"></v-icon>
                        <span class="text-h4">Formulario de Usuario</span>
                    </v-card-title>

                    <v-card-text class="pa-6">
                        <v-form @submit.prevent="saveUser">
                            <v-text-field
                                v-model="userData.username"
                                label="Usuario"
                                prepend-inner-icon="mdi-account"
                                variant="outlined"
                                color="primary"
                                :disabled="loading"
                                class="mb-4"
                            ></v-text-field>

                            <v-text-field
                                v-model="userData.fullname"
                                label="Nombre completo"
                                prepend-inner-icon="mdi-card-account-details"
                                variant="outlined"
                                color="primary"
                                :disabled="loading"
                                class="mb-4"
                            ></v-text-field>

                            <v-divider class="my-6"></v-divider>

                            <div class="d-flex gap-3">
                                <v-btn
                                    type="submit"
                                    color="primary"
                                    size="large"
                                    prepend-icon="mdi-content-save"
                                    :loading="loading"
                                >
                                    Guardar
                                </v-btn>
                                <v-btn
                                    color="grey"
                                    size="large"
                                    variant="outlined"
                                    prepend-icon="mdi-cancel"
                                    @click="cancel"
                                    :disabled="loading"
                                >
                                    Cancelar
                                </v-btn>
                            </div>
                        </v-form>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>
