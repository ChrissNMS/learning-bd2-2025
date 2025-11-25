<script setup lang="ts">
import { fetchUser, patchUser } from '@/api'
import UserForm from '@/components/UserForm.vue'
import type { User } from '@/interfaces'
import { ref, type Ref } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()
const user: Ref<User | null> = ref(null)

async function loadUser() {
    user.value = await fetchUser(Number(route.params.id))
}
async function updateUser(updatedUser: User) {
    await patchUser(Number(route.params.id), updatedUser)
}

loadUser()
</script>

<template>
    <UserForm :inputUserData="user" @save-user="updateUser" />
</template>
