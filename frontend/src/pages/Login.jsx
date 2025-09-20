import React, { useState } from "react";
import { login, register, logout, auth } from "../firebase";
import axios from "axios";

function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  // API base URL - consider moving to environment variable
  const API_BASE_URL = import.meta.env.VITE_APP_API_URL || "http://127.0.0.1:8000";

  const handleRegister = async () => {
    try {
      setLoading(true);
      setMessage("");
      
      await register(email, password);
      setMessage("✅ User registered successfully!");
      
      // Optional: Auto-login after registration
      // await handleLogin();
      
    } catch (err) {
      setMessage(`❌ Registration failed: ${err.message}`);
      console.error("Registration error:", err);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = async () => {
    try {
      setLoading(true);
      setMessage("");
      
      // Login with Firebase
      await login(email, password);
      
      // Get Firebase ID token
      const token = await auth.currentUser.getIdToken();
      
      // Test protected endpoint
      const response = await axios.get(`${API_BASE_URL}/protected`, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000, // 10 second timeout
      });
      
      console.log("Backend Response:", response.data);
      setMessage(`✅ Login successful! Welcome ${response.data.user}`);
      
      // Optional: Store token or user data in localStorage/context
      // localStorage.setItem('authToken', token);
      
    } catch (err) {
      console.error("Login error:", err);
      
      if (err.response) {
        // Server responded with error
        const errorMessage = err.response.data?.detail || "Server error";
        setMessage(`❌ ${errorMessage}`);
      } else if (err.request) {
        // Request made but no response
        setMessage("❌ Cannot connect to server. Is the backend running?");
      } else {
        // Other error (Firebase, etc.)
        setMessage(`❌ Login failed: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    try {
      setLoading(true);
      await logout();
      setMessage("✅ Logged out successfully!");
      setEmail("");
      setPassword("");
    } catch (err) {
      setMessage(`❌ Logout failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Input validation
  const isFormValid = email.trim() !== "" && password.length >= 6;

  return (
    <div className="min-h-screen bg-gradient-primary flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full space-y-8">
        <div className="glass-effect rounded-xl shadow-2xl p-8 animate-bounce-in">
          {/* Header */}
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Next-Step
            </h2>
            <p className="text-gray-600 text-sm">
              Sign in to your account or create a new one
            </p>
          </div>

          {/* Form */}
          <div className="mt-8 space-y-6">
            {/* Email Input */}
            <div>
              <label className="form-label">
                Email Address
              </label>
              <input
                type="email"
                placeholder="Enter your email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                disabled={loading}
                className="form-input"
                required
              />
            </div>

            {/* Password Input */}
            <div>
              <label className="form-label">
                Password
              </label>
              <input
                type="password"
                placeholder="Enter your password (min 6 chars)"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                disabled={loading}
                className="form-input"
                required
              />
              <p className="text-xs text-gray-500 mt-1">
                Password must be at least 6 characters long
              </p>
            </div>

            {/* Buttons */}
            <div className="space-y-3">
              <button 
                onClick={handleLogin}
                disabled={loading || !isFormValid}
                className="w-full btn-primary"
              >
                <div className="flex items-center justify-center">
                  {loading && (
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  )}
                  {loading ? "Signing In..." : "Sign In"}
                </div>
              </button>
              
              <button 
                onClick={handleRegister}
                disabled={loading || !isFormValid}
                className="w-full btn-secondary"
              >
                <div className="flex items-center justify-center">
                  {loading && (
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  )}
                  {loading ? "Creating Account..." : "Create Account"}
                </div>
              </button>
              
              <button 
                onClick={handleLogout}
                disabled={loading}
                className="w-full btn-danger"
              >
                Sign Out
              </button>
            </div>

            {/* Divider */}
            <div className="relative">
              <div className="absolute inset-0 flex items-center">
                <div className="w-full border-t border-gray-300"></div>
              </div>
              <div className="relative flex justify-center text-sm">
                <span className="px-2 bg-white text-gray-500">Authentication Status</span>
              </div>
            </div>

            {/* Message */}
            {message && (
              <div className={message.includes("✅") ? "message-success" : "message-error"}>
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    {message.includes("✅") ? (
                      <svg className="h-5 w-5 text-green-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  <div className="ml-3">
                    <p className="text-sm font-medium">
                      {message}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="mt-6 text-center">
            <p className="text-xs text-gray-500">
              By continuing, you agree to our Terms of Service and Privacy Policy
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;