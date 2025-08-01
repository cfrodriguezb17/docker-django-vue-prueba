<script setup>
import { ref } from "vue";
import { useAuth } from "@/composables/useAuth";
const { loading, handleLogin, loginError } = useAuth();

const visible = ref(false);
const email = ref("");
const password = ref("");
</script>

<template>
  <div class="d-flex align-center w-100 h-100">
    <v-card
      class="mx-auto pa-12 pb-8 w-100"
      elevation="8"
      max-width="448"
      rounded="lg"
    >
      <v-alert
        v-if="loginError"
        :text="loginError"
        border="start"
        close-label="Error!"
        color="red"
        title="Error!"
        variant="tonal"
        closable
      ></v-alert>
      <div class="text-subtitle-1 text-medium-emphasis">Correo Electronico</div>

      <v-text-field
        density="compact"
        placeholder="Correo Electronico"
        prepend-inner-icon="mdi-email-outline"
        variant="outlined"
        v-model="email"
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
        placeholder="Escribe tu Contraseña"
        prepend-inner-icon="mdi-lock-outline"
        variant="outlined"
        @click:append-inner="visible = !visible"
        v-model="password"
      ></v-text-field>

      <v-btn
        class="mb-8"
        color="teal"
        size="large"
        variant="tonal"
        block
        :loading="loading"
        @click="handleLogin(email, password)"
      >
        Log In
      </v-btn>

      <v-card-text class="text-center">
        <v-btn
          to="/register"
          variant="text"
          color="teal"
          append-icon="mdi-chevron-right"
        >
          Registrarse
        </v-btn>
      </v-card-text>
    </v-card>
  </div>
</template>
