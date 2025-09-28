import React, { useState, useEffect } from "react";
import { auth } from "../firebase";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import Footer from "../components/Footer";
import { registerStudent } from "../api";

// Fixed API function
export async function checkRegistrationStatus(token) {
  const API_BASE_URL = import.meta.env.VITE_APP_API_URL || "http://127.0.0.1:8000";
  
  try {
    const response = await axios.get(`${API_BASE_URL}/check-registration`, {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    });
    
    console.log("Registration status response:", response.data);
    return response.data;
  } catch (error) {
    console.error("Failed to check registration status:", error);
    throw error;
  }
}

function RegistrationForm() {
  const [formData, setFormData] = useState({
    display_name: "",
    age: "",
    education_level: "",
    phone_number: "",
    email: "",
    firebase_uid: ""
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const [user, setUser] = useState(null);
  const [checkingStatus, setCheckingStatus] = useState(true); // New state for status check

  const API_BASE_URL = import.meta.env.VITE_APP_API_URL || "http://127.0.0.1:8000";
  const navigate = useNavigate();
  const educationLevels = [
    "High School",
    "Diploma", 
    "Associate's Degree",
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "Professional Certification",
    "Trade School",
    "Other"
  ];

  // Check registration status when user is authenticated
  const checkUserRegistration = async (currentUser) => {
    try {
      setCheckingStatus(true);
      const token = await currentUser.getIdToken();
      const statusResponse = await checkRegistrationStatus(token);
      
      // If user is already registered, redirect to dashboard
      if (statusResponse.is_registered) {
        console.log("User is already registered, redirecting to dashboard");
        navigate("/dashboard");
        return;
      }
      
      console.log("User is not registered, showing registration form");
    } catch (error) {
      console.error("Error checking registration status:", error);
      // If there's an error checking status, we'll show the form anyway
      // This could happen if the endpoint doesn't exist yet or user isn't registered
    } finally {
      setCheckingStatus(false);
    }
  };

  // Get user info from Firebase on component mount
  useEffect(() => {
    const unsubscribe = auth.onAuthStateChanged(async (currentUser) => {
      if (currentUser) {
        setUser(currentUser);
        setFormData(prev => ({
          ...prev,
          email: currentUser.email || "",
          firebase_uid: currentUser.uid,
          display_name: currentUser.displayName || ""
        }));
        
        // Check if user is already registered
        await checkUserRegistration(currentUser);
      } else {
        // If no user, redirect to login
        navigate("/login");
      }
    });

    return () => unsubscribe();
  }, [navigate]);

  const handleInputChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    
    try {
      setLoading(true);
      setMessage("");
      
      if (!auth.currentUser) {
        setMessage("❌ Please sign in first to complete registration");
        return;
      }

      const token = await auth.currentUser.getIdToken();
      const registrationData = {
        display_name: formData.display_name,
        age: parseInt(formData.age),
        education_level: formData.education_level,
        phone_number: formData.phone_number,
        email: formData.email,
        firebase_uid: formData.firebase_uid
      };

      const response = await registerStudent(token, registrationData);

      console.log("Registration successful:", response.data);
      setMessage("✅ Registration completed successfully! Welcome to your personalized career journey!");
      
      // Redirect after successful registration
      setTimeout(() => {
        navigate("/dashboard");
      }, 1500);

    } catch (err) {
      console.error("Registration error:", err);
      
      if (err.response) {
        const errorMessage = err.response.data?.detail || "Registration failed";
        setMessage(`❌ ${errorMessage}`);
      } else if (err.request) {
        setMessage("❌ Unable to connect to server. Please check your connection and try again.");
      } else {
        setMessage(`❌ Registration failed: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = 
    formData.display_name.trim().length >= 2 &&
    formData.age && parseInt(formData.age) >= 16 && parseInt(formData.age) <= 100 &&
    formData.education_level &&
    formData.phone_number.trim().length >= 10 &&
    formData.email.includes('@');

  const completedFields = Object.values(formData).filter(val => val && val.toString().trim()).length - 1; // Subtract firebase_uid as it's auto-filled

  // Show loading spinner while checking registration status
  if (checkingStatus) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-violet-50 via-blue-50 to-cyan-50 flex items-center justify-center">
        <div className="text-center">
          <div className="inline-block animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mb-4"></div>
          <p className="text-lg text-gray-600">Checking your registration status...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-violet-50 via-blue-50 to-cyan-50 py-8 px-4 sm:px-6 lg:px-8 relative overflow-hidden">
      {/* Animated Background Elements */}
      <div className="absolute inset-0 overflow-hidden pointer-events-none">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-gradient-to-br from-blue-400 to-purple-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-gradient-to-br from-cyan-400 to-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
        <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-80 h-80 bg-gradient-to-br from-violet-400 to-pink-400 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse animation-delay-4000"></div>
      </div>

      <div className="max-w-2xl mx-auto relative z-10">
        {/* Main Card */}
        <div className="bg-white/80 backdrop-blur-xl shadow-2xl rounded-3xl p-8 border border-white/20 transition-all duration-500 hover:shadow-3xl">
          {/* Header */}
          <div className="text-center mb-10">
            <div className="mx-auto flex items-center justify-center h-16 w-16 rounded-2xl bg-gradient-to-r from-blue-500 to-purple-600 mb-6 transform transition-all duration-300 hover:scale-110">
              <svg className="h-8 w-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h1 className="text-4xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent mb-4">
              Complete Your Profile
            </h1>
            <p className="text-lg text-gray-600 max-w-md mx-auto leading-relaxed">
              Help us personalize your career journey with some basic information about yourself
            </p>
          </div>

          {/* User Info Display */}
          {user && (
            <div className="mb-8 p-4 bg-gradient-to-r from-blue-50 to-purple-50 rounded-xl border border-blue-100">
              <div className="flex items-center space-x-4">
                {user.photoURL ? (
                  <img src={user.photoURL} alt="Profile" className="w-12 h-12 rounded-full border-2 border-white shadow-lg" />
                ) : (
                  <div className="w-12 h-12 rounded-full bg-gradient-to-r from-blue-500 to-purple-500 flex items-center justify-center">
                    <span className="text-white font-semibold text-lg">
                      {user.displayName ? user.displayName.charAt(0).toUpperCase() : user.email.charAt(0).toUpperCase()}
                    </span>
                  </div>
                )}
                <div>
                  <p className="font-medium text-gray-900">Signed in as</p>
                  <p className="text-sm text-gray-600">{user.email}</p>
                </div>
              </div>
            </div>
          )}

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Display Name Field */}
            <div className="group">
              <label className="block text-sm font-semibold text-gray-900 mb-3">
                Display Name <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  name="display_name"
                  placeholder="How would you like to be called?"
                  value={formData.display_name}
                  onChange={handleInputChange}
                  disabled={loading}
                  className="w-full px-4 py-4 pl-12 pr-4 text-gray-900 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 group-hover:bg-gray-100 disabled:opacity-50"
                  required
                />
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              </div>
              {formData.display_name && formData.display_name.trim().length < 2 && (
                <p className="mt-2 text-sm text-red-500 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Name must be at least 2 characters
                </p>
              )}
            </div>

            {/* Email Field (Read-only) */}
            <div className="group">
              <label className="block text-sm font-semibold text-gray-900 mb-3">
                Email Address
              </label>
              <div className="relative">
                <input
                  type="email"
                  name="email"
                  value={formData.email}
                  disabled={true}
                  className="w-full px-4 py-4 pl-12 pr-4 text-gray-600 bg-gray-100 border border-gray-200 rounded-xl cursor-not-allowed"
                />
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                  </svg>
                </div>
                <div className="absolute inset-y-0 right-0 pr-4 flex items-center">
                  <svg className="h-5 w-5 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M2.166 4.999A11.954 11.954 0 0010 1.944 11.954 11.954 0 0017.834 5c.11.65.166 1.32.166 2.001 0 5.225-3.34 9.67-8 11.317C5.34 16.67 2 12.225 2 7c0-.682.057-1.35.166-2.001zm11.541 3.708a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                  </svg>
                </div>
              </div>
              <p className="mt-2 text-sm text-gray-500">✓ Verified from your account</p>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              {/* Age Field */}
              <div className="group">
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Age <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <input
                    type="number"
                    name="age"
                    placeholder="Your age"
                    value={formData.age}
                    onChange={handleInputChange}
                    disabled={loading}
                    min="16"
                    max="100"
                    className="w-full px-4 py-4 pl-12 pr-4 text-gray-900 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 group-hover:bg-gray-100 disabled:opacity-50"
                    required
                  />
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3a4 4 0 118 0v4m-4 8a1 1 0 100-2 1 1 0 000 2z" />
                    </svg>
                  </div>
                </div>
                {formData.age && (parseInt(formData.age) < 16 || parseInt(formData.age) > 100) && (
                  <p className="mt-2 text-sm text-red-500 flex items-center">
                    <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                    </svg>
                    Age must be between 16 and 100
                  </p>
                )}
              </div>

              {/* Education Level Field */}
              <div className="group">
                <label className="block text-sm font-semibold text-gray-900 mb-3">
                  Education Level <span className="text-red-500">*</span>
                </label>
                <div className="relative">
                  <select
                    name="education_level"
                    value={formData.education_level}
                    onChange={handleInputChange}
                    disabled={loading}
                    className="w-full px-4 py-4 pl-12 pr-10 text-gray-900 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 group-hover:bg-gray-100 disabled:opacity-50 appearance-none cursor-pointer"
                    required
                  >
                    <option value="">Select your education level</option>
                    {educationLevels.map((level) => (
                      <option key={level} value={level}>
                        {level}
                      </option>
                    ))}
                  </select>
                  <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                    </svg>
                  </div>
                  <div className="absolute inset-y-0 right-0 pr-4 flex items-center pointer-events-none">
                    <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                    </svg>
                  </div>
                </div>
              </div>
            </div>

            {/* Phone Number Field */}
            <div className="group">
              <label className="block text-sm font-semibold text-gray-900 mb-3">
                Phone Number <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="tel"
                  name="phone_number"
                  placeholder="Enter your phone number with country code"
                  value={formData.phone_number}
                  onChange={handleInputChange}
                  disabled={loading}
                  className="w-full px-4 py-4 pl-12 pr-4 text-gray-900 bg-gray-50 border border-gray-200 rounded-xl focus:ring-4 focus:ring-blue-100 focus:border-blue-500 transition-all duration-200 group-hover:bg-gray-100 disabled:opacity-50"
                  required
                />
                <div className="absolute inset-y-0 left-0 pl-4 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400 group-hover:text-blue-500 transition-colors" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
              </div>
              {formData.phone_number && formData.phone_number.trim().length < 10 && (
                <p className="mt-2 text-sm text-red-500 flex items-center">
                  <svg className="w-4 h-4 mr-1" fill="currentColor" viewBox="0 0 20 20">
                    <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                  </svg>
                  Phone number must be at least 10 digits
                </p>
              )}
              <p className="mt-2 text-sm text-gray-500">
                Include country code (e.g., +1234567890 or +91987654321)
              </p>
            </div>

            {/* Enhanced Progress Indicator */}
            <div className="space-y-3">
              <div className="flex justify-between items-center">
                <span className="text-sm font-medium text-gray-700">Profile Completion</span>
                <span className="text-sm font-bold text-blue-600">{Math.round((completedFields / 4) * 100)}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-3 overflow-hidden">
                <div 
                  className="h-3 rounded-full bg-gradient-to-r from-blue-500 to-purple-600 transition-all duration-500 ease-out relative overflow-hidden"
                  style={{ width: `${(completedFields / 4) * 100}%` }}
                >
                  <div className="absolute inset-0 bg-white bg-opacity-20 animate-pulse"></div>
                </div>
              </div>
            </div>

            {/* Submit Button */}
            <div className="space-y-6">
              <button
                type="submit"
                disabled={loading || !isFormValid}
                className={`w-full py-4 px-8 rounded-xl text-white font-semibold text-lg transition-all duration-300 transform ${
                  loading || !isFormValid
                    ? 'bg-gray-300 cursor-not-allowed'
                    : 'bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 hover:scale-105 hover:shadow-2xl active:scale-95'
                } disabled:opacity-50 shadow-lg`}
              >
                <div className="flex items-center justify-center space-x-3">
                  {loading && (
                    <svg className="animate-spin h-6 w-6 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  )}
                  <span>{loading ? "Creating Your Profile..." : "Complete Registration"}</span>
                  {!loading && (
                    <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 7l5 5m0 0l-5 5m5-5H6" />
                    </svg>
                  )}
                </div>
              </button>

              {/* Form Validation Summary */}
              {!isFormValid && completedFields > 0 && (
                <div className="bg-amber-50 border border-amber-200 rounded-xl p-6 transition-all duration-300">
                  <div className="flex items-start">
                    <div className="flex-shrink-0">
                      <svg className="h-6 w-6 text-amber-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-4">
                      <h3 className="text-sm font-semibold text-amber-800 mb-2">
                        Please complete the remaining fields
                      </h3>
                      <div className="text-sm text-amber-700 space-y-1">
                        {formData.display_name.trim().length < 2 && <p>• Enter a valid display name (min 2 characters)</p>}
                        {(!formData.age || parseInt(formData.age) < 16 || parseInt(formData.age) > 100) && <p>• Enter age between 16-100</p>}
                        {!formData.education_level && <p>• Select your education level</p>}
                        {formData.phone_number.trim().length < 10 && <p>• Enter a valid phone number</p>}
                        {!formData.email.includes('@') && <p>• Valid email is required</p>}
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Message Display */}
            {message && (
              <div className={`p-6 rounded-xl border transition-all duration-300 ${
                message.includes("✅") 
                  ? "bg-green-50 border-green-200 text-green-800" 
                  : "bg-red-50 border-red-200 text-red-800"
              }`}>
                <div className="flex items-start">
                  <div className="flex-shrink-0">
                    {message.includes("✅") ? (
                      <svg className="h-6 w-6 text-green-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clipRule="evenodd" />
                      </svg>
                    ) : (
                      <svg className="h-6 w-6 text-red-500" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                      </svg>
                    )}
                  </div>
                  <div className="ml-3">
                    <p className="font-medium">
                      {message}
                    </p>
                  </div>
                </div>
              </div>
            )}
          </form>

          {/* Security Notice */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-center space-x-2 text-sm text-gray-500">
              <svg className="h-5 w-5 text-green-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>Your information is secured with enterprise-grade encryption</span>
            </div>
          </div>
        </div>

        {/* Enhanced Info Cards */}
        <div className="mt-12 grid md:grid-cols-3 gap-6">
          {[
            {
              icon: "🎯",
              title: "Personalized Career Paths",
              description: "Get tailored recommendations based on your education and experience level"
            },
            {
              icon: "📊",
              title: "Smart Analytics",
              description: "Track your progress with detailed insights and milestone achievements"
            },
            {
              icon: "🚀",
              title: "Future-Ready Skills",
              description: "Learn skills that matter in tomorrow's job market with AI-driven suggestions"
            }
          ].map((feature, index) => (
            <div key={index} className="bg-white/60 backdrop-blur-lg rounded-2xl p-6 border border-white/30 hover:bg-white/80 transition-all duration-300 transform hover:-translate-y-1 hover:shadow-xl group">
              <div className="text-4xl mb-4 transform group-hover:scale-110 transition-transform duration-300">
                {feature.icon}
              </div>
              <h3 className="text-lg font-semibold text-gray-900 mb-3 group-hover:text-blue-600 transition-colors">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>

        {/* Benefits Section */}
        <div className="mt-12 bg-gradient-to-r from-blue-50 to-purple-50 rounded-3xl p-8 border border-blue-100">
          <h3 className="text-2xl font-bold text-center text-gray-900 mb-8">
            Why Complete Your Profile?
          </h3>
          <div className="grid md:grid-cols-2 gap-6">
            {[
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                ),
                title: "Tailored Recommendations",
                description: "Career paths and learning resources matched to your education and goals"
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                  </svg>
                ),
                title: "Age-Appropriate Guidance",
                description: "Timeline and strategies designed for your specific life stage"
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
                  </svg>
                ),
                title: "Direct Communication",
                description: "Important updates and opportunities delivered when you need them"
              },
              {
                icon: (
                  <svg className="h-6 w-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 100 4m0-4v2m0-6V4" />
                  </svg>
                ),
                title: "Progress Tracking",
                description: "Monitor your career development journey with detailed analytics"
              }
            ].map((benefit, index) => (
              <div key={index} className="flex items-start space-x-4 p-4 bg-white/50 rounded-xl hover:bg-white/70 transition-all duration-200">
                <div className="flex-shrink-0 w-12 h-12 bg-gradient-to-r from-blue-500 to-purple-500 rounded-xl flex items-center justify-center text-white">
                  {benefit.icon}
                </div>
                <div>
                  <h4 className="font-semibold text-gray-900 mb-2">{benefit.title}</h4>
                  <p className="text-gray-600 text-sm leading-relaxed">{benefit.description}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

      </div>
      <Footer />
      <style jsx>{`
        @keyframes fade-in {
          from {
            opacity: 0;
            transform: translateY(20px);
          }
          to {
            opacity: 1;
            transform: translateY(0);
          }
        }

        @keyframes slide-in {
          from {
            opacity: 0;
            transform: translateX(-20px);
          }
          to {
            opacity: 1;
            transform: translateX(0);
          }
        }

        .animate-fade-in {
          animation: fade-in 0.6s ease-out;
        }

        .animate-slide-in {
          animation: slide-in 0.8s ease-out 0.2s both;
        }

        .animation-delay-2000 {
          animation-delay: 2s;
        }

        .animation-delay-4000 {
          animation-delay: 4s;
        }

        .group:hover .group-hover\\:scale-110 {
          transform: scale(1.1);
        }

        .group:hover .group-hover\\:text-blue-600 {
          color: #2563eb;
        }

        .group:hover .group-hover\\:text-blue-500 {
          color: #3b82f6;
        }

        .shadow-3xl {
          box-shadow: 0 35px 60px -12px rgba(0, 0, 0, 0.25);
        }
      `}</style>
    </div>
  );
}

export default RegistrationForm;