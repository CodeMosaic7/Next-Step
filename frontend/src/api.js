// src/api.js
const API_BASE = import.meta.env.VITE_PUBLIC_API_URL||"http://localhost:8000";

export async function getProtectedData(token) {
  const response = await axios.get(`${API_BASE}/protected`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }); 

  if (!response.ok) {
    throw new Error("Failed to fetch protected data");
  }

  return await response.json();
}

export async function registerStudent (token,registrationData) {
  const response = await axios.post(`${API_BASE}/registration`, registrationData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 15000
      });
      if (!response.ok) {
    throw new Error("Failed to register student");
  }

  return await response.json();
}

export async function checkRegistrationStatus(token){
  const response = await axios.get(`${API_BASE}/check-registration`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });
  if (!response.ok) {
    throw new Error("Failed to check registration status");
  }
  console.log("Registration status response:", response);
  return await response.json();
}