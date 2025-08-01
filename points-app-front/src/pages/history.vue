<script setup>
import NavBar from "@/components/NavBar.vue";
import { useAuth } from "@/composables/useAuth";
import apiClient from "@/plugins/axios";
import { ref } from "vue";
const history = ref(null);

const { getDataProfile } = useAuth();

getDataProfile();

const getHistory = async () => {
  const res = await apiClient.get("api/user/history");
  if (res.data) {
    history.value = res.data.results;
  }
};

getHistory();
</script>

<template>
  <NavBar />
  <v-card class="mx-auto mt-8" max-width="400">
    <v-card-text>
      <div class="font-weight-bold ms-1 mb-2">Transacciones</div>

      <v-timeline align="start" density="compact">
        <v-timeline-item
          v-for="entry in history"
          :key="entry.id"
          :dot-color="entry.transaction_type === 'redeem' ? 'red' : 'green'"
          size="x-small"
        >
          <div class="mb-4">
            <div class="font-weight-normal">
              {{
                entry.transaction_type === "redeem" ? "Gastados" : "Agregados"
              }}:
              <strong>{{ entry.amount.split(".")[0] }}</strong>
            </div>
            <div>Fecha: {{ entry.created_at }}</div>
            <div>Descripción: {{ entry.description }}</div>
          </div>
        </v-timeline-item>
      </v-timeline>
    </v-card-text>
  </v-card>
</template>
