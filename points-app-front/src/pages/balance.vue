<script setup lang="ts">
import NavBar from "@/components/NavBar.vue";
import { useAuth } from "@/composables/useAuth";
import { computed } from "vue";
const { profileData, getDataProfile } = useAuth();

getDataProfile();

const pointsCop = computed(() => {
  if (profileData && profileData.value) {
    const points = parseFloat(profileData.value.points);
    return points * 10;
  }
  return 0;
});
</script>

<template>
  <NavBar />
  <v-card class="mx-auto mt-8" max-width="500" border flat>
    <v-card-text class="text-medium-emphasis pa-6">
      <div class="text-h6 mb-6">Aproximadamente {{ pointsCop }} COP$ 🤑📈</div>

      <div class="text-h4 font-weight-black mb-4">
        {{ profileData ? profileData.points.split(".")[0] : 0 }} 🟢
      </div>
      <v-progress-linear
        bg-color="surface-variant"
        class="mb-6"
        color="primary"
        height="10"
        model-value="50"
        rounded="pill"
      ></v-progress-linear>
    </v-card-text>
  </v-card>
</template>
