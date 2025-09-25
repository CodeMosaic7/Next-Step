// src/api.js
const API_BASE = import.meta.env.VITE_PUBLIC_API_URL||"http://localhost:8000";

export async function getProtectedData(token) {
  const response = await fetch(`${API_BASE}/protected`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  }); 

  if (!response.ok) {
    throw new Error("Failed to fetch protected data");
  }

  return await response.json();
}

export async function registerStudent(token, studentData) {
  const response = await fetch(`${API_BASE}/register-student`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(studentData),
  });

  if (!response.ok) {
    throw new Error("Failed to register student");
  }

  return await response.json();
}
