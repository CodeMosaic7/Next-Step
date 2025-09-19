// src/api.js

export async function getProtectedData(token) {
  const response = await fetch("http://localhost:8000/protected", {
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
  const response = await fetch("http://localhost:8000/register-student", {
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
