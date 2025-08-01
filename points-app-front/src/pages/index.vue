<script setup>
import NavBar from "@/components/NavBar.vue";
import { useAuth } from "@/composables/useAuth";

const { getDataProfile } = useAuth();

getDataProfile();
</script>

<template>
  <NavBar />
  <v-container fluid class="d-flex align-center justify-center h-100">
    <v-row>
      <v-col class="d-flex align-center justify-center">
        <h1 class="text-h1 text-blue-darken-3">POINTS APP</h1>
      </v-col>
    </v-row>
  </v-container>
</template>
