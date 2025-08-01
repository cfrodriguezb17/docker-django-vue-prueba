<template>
  <NavBar />
  <v-sheet class="mx-auto mt-8" width="300">
    <v-form ref="form" @submit.prevent="sendForm">
      <v-number-input
        :reverse="false"
        controlVariant="default"
        label="Cantidad a redimir"
        :hideInput="false"
        :inset="false"
        :rules="[(v) => !!v || 'Este campo es requerido']"
        v-model="amount"
      ></v-number-input>
      <v-textarea
        label="Descripción"
        v-model="description"
        :rules="[(v) => !!v || 'Este campo es requerido']"
      ></v-textarea>
      <v-btn class="mt-2" block type="submit">Enviar</v-btn>
    </v-form>
  </v-sheet>
  <v-dialog
    width="400"
    transition="dialog-bottom-transition"
    v-model="showDialog"
  >
    <v-card>
      <v-toolbar
        :color="dialogOptions.color"
        :title="dialogOptions.title"
      ></v-toolbar>

      <v-card-text class="text-body-1">{{
        dialogOptions.description
      }}</v-card-text>

      <v-card-actions class="justify-end">
        <v-btn text="Cerrar" @click="showDialog = false"></v-btn>
      </v-card-actions>
    </v-card>
  </v-dialog>
</template>
<script setup>
import NavBar from "@/components/NavBar.vue";
import { useAuth } from "@/composables/useAuth";
import apiClient from "@/plugins/axios";
import { ref } from "vue";

const { getDataProfile } = useAuth();

getDataProfile();

const form = ref(null);
const loading = ref(false);
const amount = ref(0);
const description = ref("");
const showDialog = ref(false);
const dialogOptions = ref({
  title: "Error",
  color: "red",
  description: "Hello world",
});

const resetForm = () => {
  form.value.reset();
};

const sendForm = async () => {
  const { valid } = await form.value.validate();
  if (valid) {
    loading.value = true;
    try {
      const data = {
        amount: amount.value,
        description: description.value,
      };
      const res = await apiClient.post("api/user/redeem", data);
      if (res.data) {
        console.log("data");
        loading.value = false;
        dialogOptions.value.title = "Hecho";
        dialogOptions.value.color = "green";
        dialogOptions.value.description = res.data.message;
        showDialog.value = true;
        resetForm();
      }
    } catch (err) {
      console.log({ err });
      loading.value = false;
      const error = err.response.data.error
        ? err.response.data.error
        : err.response.data.amount[0];
      dialogOptions.value = {
        title: "Error",
        color: "red",
        description: error,
      };
      showDialog.value = true;
    }
  }
};
</script>
