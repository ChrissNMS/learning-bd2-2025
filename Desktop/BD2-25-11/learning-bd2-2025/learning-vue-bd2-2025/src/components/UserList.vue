<script setup lang="ts">
import { ref, type Ref, onMounted } from 'vue'
import type { User } from '@/interfaces'
import { fetchUsers } from '@/api'
import { useRouter } from 'vue-router'

const router = useRouter()
const users: Ref<User[]> = ref([])
const loading = ref(false)
const search = ref('')

const headers = [
    { title: 'ID', key: 'id', sortable: true },
    { title: 'Usuario', key: 'username', sortable: true },
    { title: 'Nombre Completo', key: 'fullname', sortable: true },
    { title: 'Acciones', key: 'actions', sortable: false }
]

async function getUsers() {
    loading.value = true
    try {
        users.value = await fetchUsers()
    } catch (error) {
        console.error('Error al cargar usuarios:', error)
    } finally {
        loading.value = false
    }
}

async function goToEditUser(userId: number) {
    await router.push({ name: 'userEdit', params: { id: userId } })
}

onMounted(() => {
    getUsers()
})
</script>

<template>
    <v-container>
        <v-row>
            <v-col cols="12">
                <v-card elevation="4">
                    <v-card-title class="d-flex align-center pa-6">
                        <v-icon icon="mdi-account-multiple" size="large" class="mr-3"></v-icon>
                        <span class="text-h4">Lista de Usuarios</span>
                        <v-spacer></v-spacer>
                        <v-btn
                            color="primary"
                            prepend-icon="mdi-refresh"
                            @click="getUsers"
                            :loading="loading"
                        >
                            Recargar
                        </v-btn>
                    </v-card-title>

                    <v-card-text>
                        <v-text-field
                            v-model="search"
                            prepend-inner-icon="mdi-magnify"
                            label="Buscar usuarios"
                            variant="outlined"
                            hide-details
                            class="mb-4"
                        ></v-text-field>

                        <v-data-table
                            :headers="headers"
                            :items="users"
                            :search="search"
                            :loading="loading"
                            loading-text="Cargando usuarios..."
                            no-data-text="No hay datos de usuarios cargados."
                            items-per-page="10"
                            class="elevation-1"
                        >
                            <template v-slot:item.username="{ item }">
                                <v-chip color="primary" variant="tonal">
                                    <v-icon icon="mdi-account" start></v-icon>
                                    {{ item.username }}
                                </v-chip>
                            </template>

                            <template v-slot:item.fullname="{ item }">
                                <span class="font-weight-medium">{{ item.fullname }}</span>
                            </template>

                            <template v-slot:item.actions="{ item }">
                                <v-btn
                                    color="info"
                                    variant="tonal"
                                    size="small"
                                    prepend-icon="mdi-pencil"
                                    @click="goToEditUser(item.id)"
                                >
                                    Editar
                                </v-btn>
                            </template>
                        </v-data-table>
                    </v-card-text>
                </v-card>
            </v-col>
        </v-row>
    </v-container>
</template>

<style scoped></style>
