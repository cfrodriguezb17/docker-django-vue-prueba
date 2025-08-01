<script setup>
import { useAuth } from "@/composables/useAuth";
import { ref } from "vue";
const visible = ref(false);
const firstName = ref("");
const email = ref("");
const password = ref("");

const { getDataProfile, handleRegister, loading, registerErrors } = useAuth();

getDataProfile();
</script>

<template>
  <div class="d-flex align-center w-100 h-100">
    <v-card
      class="mx-auto pa-12 pb-8 w-100"
      elevation="8"
      max-width="448"
      rounded="lg"
    >
      <div class="text-subtitle-1 text-medium-emphasis">Primer Nombre</div>

      <v-text-field
        density="compact"
        placeholder="Primer Nombre"
        prepend-inner-icon="mdi-account-circle-outline"
        variant="outlined"
        v-model="firstName"
      ></v-text-field>

      <div class="text-subtitle-1 text-medium-emphasis">Correo Electronico</div>

      <v-text-field
        density="compact"
        placeholder="Correo Electronico"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        v-model="email"
        :error-messages="registerErrors.email"
      ></v-text-field>

      <div
        class="text-subtitle-1 text-medium-emphasis d-flex align-center justify-space-between"
      >
        Contraseña
      </div>

      <v-text-field
        :append-inner-icon="visible ? 'mdi-eye-off' : 'mdi-eye'"
        :type="visible ? 'text' : 'password'"
        density="compact"
        placeholder="Contraseña"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
        :error-messages="registerErrors.password"
        v-model="password"
      ></v-text-field>

      <v-btn
        class="mb-8"
        color="teal"
        size="large"
        variant="tonal"
        block
        @click="handleRegister(firstName, email, password)"
        :loading="loading"
      >
        Registrarse
      </v-btn>
      <v-card-text class="text-center">
        <v-btn
          to="/login"
          variant="text"
          color="teal"
          append-icon="mdi-chevron-right"
        >
          Log in
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>
