<script setup>
import { useAuth } from "@/composables/useAuth";
import { ref } from "vue";
const { profileData, loadDataIntoView, handleLogOut } = useAuth();

if (!profileData.value) {
  loadDataIntoView();
}
const items = ref([
  { title: "Log Out", icon: "mdi-logout", action: handleLogOut },
]);
</script>
<template>
  <v-app-bar color="teal-darken-4">
    <template v-slot:image>
      <v-img
        gradient="to top right, rgba(19,84,122,.8), rgba(128,208,199,.8)"
      ></v-img>
    </template>

    <!-- <template v-slot:prepend>
      <v-app-bar-nav-icon></v-app-bar-nav-icon>
    </template> -->
    <v-app-bar-title>
      <router-link
        to="/"
        class="cursor-pointer text-white text-decoration-none"
      >
        Points App
      </router-link>
    </v-app-bar-title>

    <v-btn variant="outlined" class="mr-2" to="/balance">Saldo</v-btn>
    <v-btn variant="outlined" class="mr-2" to="/history">Historial</v-btn>
    <v-btn variant="outlined" class="mr-2" to="/redeem">Redimir</v-btn>
    <v-btn
      v-if="profileData ? profileData.is_admin : false"
      variant="outlined"
      class="mr-2 ml-6"
      to="/grant"
      >Otorgar</v-btn
    >
    <span class="text-body-1 ml-4">{{
      profileData ? profileData.first_name : ""
    }}</span>
    <v-btn icon>
      <v-icon>mdi-account-circle</v-icon>
      <v-menu activator="parent">
        <v-list>
          <v-list-item
            v-for="(item, index) in items"
            :key="index"
            :value="index"
            @click="item.action"
          >
            <v-list-item-title class="d-flex"
              >{{ item.title }}
              <v-icon class="ml-2">{{ item.icon }}</v-icon></v-list-item-title
            >
          </v-list-item>
        </v-list>
      </v-menu>
    </v-btn>
  </v-app-bar>
</template>
