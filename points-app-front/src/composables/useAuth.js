import apiClient, { setToken } from "@/plugins/axios";
import router from "@/router";
import { ref } from "vue";

export const useAuth = () => {
  const token = ref(null);
  const loading = ref(false);
  const error = ref(null);
  const firstName = ref("");
  const profileData = ref(null);
  const registerErrors = ref({
    email: "",
    first_name: "",
    password: "",
  });
  const loginError = ref(null);

  const getDataProfile = async () => {
    try {
      const token = localStorage.getItem("authToken") || "";
      setToken(token);
      const res = await apiClient.get("api/user/profile", {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      profileData.value = res.data;
      firstName.value = profileData.value.first_name;
      localStorage.setItem("profileData", JSON.stringify(profileData.value));
    } catch (err) {}
  };

  const updateProfile = async () => {
    try {
      const res = await apiClient.get("api/user/profile");
      profileData.value = res.data;
      firstName.value = profileData.value.first_name;
      localStorage.setItem("profileData", JSON.stringify(profileData.value));
    } catch (err) {}
  };

  const handleLogin = async (email, password) => {
    loading.value = true;
    loginError.value = false;
    try {
      const data = {
        email,
        password,
      };
      const res = await apiClient.post("api/auth/login", data);
      token.value = res.data.access;
      setToken(token.value);
      loading.value = false;
      router.push("/");
    } catch (err) {
      loading.value = false;
      if (err.response && err.response.data && err.response.data.detail) {
        loginError.value = err.response.data.detail;
      } else {
        console.log({ err });
      }
    }
  };

  const handleRegister = async (firstName, email, password) => {
    loading.value = true;
    try {
      const data = {
        first_name: firstName,
        email,
        password,
      };
      const res = await apiClient.post("api/auth/register", data, {
        headers: {
          Authorization: null,
        },
      });
      if (res.data) {
        profileData.value = res.data;
        localStorage.setItem("profileData", JSON.stringify(profileData.value));
        handleLogin(email, password);
      }
    } catch (err) {
      console.log({ err });
      if (err.response && err.response.data) {
        registerErrors.value = err.response.data;
        loading.value = false;
      }
    }
  };

  const removeCredentials = () => {
    try {
      console.log("Removiendo...");

      localStorage.removeItem("authToken");
      localStorage.removeItem("profileData");

      const authTokenRemoved = localStorage.getItem("authToken") === null;
      const profileDataRemoved = localStorage.getItem("profileData") === null;

      if (!authTokenRemoved || !profileDataRemoved) {
        setTimeout(() => {
          removeCredentials();
        }, 200);
      } else {
        delete apiClient.defaults.headers.common["Authorization"];
        firstName.value = "";
        profileData.value = null;
        token.value = null;
      }
    } catch (error) {
      console.error(
        "Error al remover las credenciales del localStorage:",
        error
      );
      delete apiClient.defaults.headers.common["Authorization"];
      firstName.value = "";
      profileData.value = null;
      token.value = null;
    }
  };

  const handleLogOut = () => {
    removeCredentials();
    router.push("/login");
    localStorage.removeItem("authToken");
    localStorage.removeItem("profileData");
    // setTimeout(() => {
    // }, 1000);
  };

  const reloadFirstName = () => {
    if (localStorage.getItem("profileData")) {
      const initialData = JSON.parse(
        localStorage.getItem("profileData") || "{}"
      );
      firstName.value = initialData.first_name || "";
    } else {
      setTimeout(() => {
        reloadFirstName();
      }, 200);
    }
  };

  const loadDataIntoView = () => {
    if (localStorage.getItem("profileData")) {
      profileData.value = JSON.parse(
        localStorage.getItem("profileData") || "{}"
      );
    } else {
      getDataProfile(token.value);
      setTimeout(() => {
        loadDataIntoView();
      }, 200);
    }
  };

  return {
    loading,
    error,
    handleLogin,
    getDataProfile,
    handleRegister,
    handleLogOut,
    firstName,
    reloadFirstName,
    profileData,
    loadDataIntoView,
    updateProfile,
    registerErrors,
    loginError,
  };
};
