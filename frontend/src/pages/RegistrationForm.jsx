import React, { useState } from "react";
import { auth } from "../firebase";
import axios from "axios";

function RegistrationForm() {
  const [formData, setFormData] = useState({
    name: "",
    age: "",
    education_level: "",
    phone_no: ""
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const API_BASE_URL = import.meta.env.VITE_APP_API_URL || "http://127.0.0.1:8000";

  const educationLevels = [
    "High School",
    "Diploma", 
    "Bachelor's Degree",
    "Master's Degree",
    "PhD",
    "Other"
  ];

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
        ...formData,
        age: parseInt(formData.age)
      };

      
      const response = await axios.post(`${API_BASE_URL}/registration`, registrationData, {
        headers: {
          'Authorization': `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000
      });

      console.log("Registration successful:", response.data);
      setMessage("✅ Registration completed successfully!");
      
      // Optional: Reset form or redirect
      // setFormData({ name: "", age: "", education_level: "", phone_no: "" });

    } catch (err) {
      console.error("Registration error:", err);
      
      if (err.response) {
        const errorMessage = err.response.data?.detail || "Registration failed";
        setMessage(`❌ ${errorMessage}`);
      } else if (err.request) {
        setMessage("❌ Cannot connect to server. Is the backend running?");
      } else {
        setMessage(`❌ Registration failed: ${err.message}`);
      }
    } finally {
      setLoading(false);
    }
  };

  const isFormValid = 
    formData.name.trim().length >= 2 &&
    formData.age && parseInt(formData.age) >= 16 && parseInt(formData.age) <= 100 &&
    formData.education_level &&
    formData.phone_no.trim().length >= 10;

  return (
    <div className="min-h-screen bg-gradient-to-br from-indigo-100 via-white to-cyan-100 py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md mx-auto">
        <div className="bg-white shadow-2xl rounded-xl p-8 animate-fade-in">
          {/* Header */}
          <div className="text-center mb-8">
            <div className="mx-auto flex items-center justify-center h-12 w-12 rounded-full bg-indigo-100">
              <svg className="h-6 w-6 text-indigo-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h2 className="mt-4 text-3xl font-bold text-gray-900">
              Complete Your Profile
            </h2>
            <p className="mt-2 text-sm text-gray-600">
              Tell us about yourself to get personalized career guidance
            </p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Name Field */}
            <div>
              <label className="form-label">
                Full Name <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="text"
                  name="name"
                  placeholder="Enter your full name"
                  value={formData.name}
                  onChange={handleInputChange}
                  disabled={loading}
                  className="form-input pl-10"
                  required
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
              </div>
              {formData.name && formData.name.trim().length < 2 && (
                <p className="mt-1 text-xs text-red-500">Name must be at least 2 characters</p>
              )}
            </div>

            {/* Age Field */}
            <div>
              <label className="form-label">
                Age <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="number"
                  name="age"
                  placeholder="Enter your age"
                  value={formData.age}
                  onChange={handleInputChange}
                  disabled={loading}
                  min="16"
                  max="100"
                  className="form-input pl-10"
                  required
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 7V3a4 4 0 118 0v4m-4 8a1 1 0 100-2 1 1 0 000 2zm4 0a1 1 0 100-2 1 1 0 000 2z" />
                  </svg>
                </div>
              </div>
              {formData.age && (parseInt(formData.age) < 16 || parseInt(formData.age) > 100) && (
                <p className="mt-1 text-xs text-red-500">Age must be between 16 and 100</p>
              )}
            </div>

            {/* Education Level Field */}
            <div>
              <label className="form-label">
                Education Level <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <select
                  name="education_level"
                  value={formData.education_level}
                  onChange={handleInputChange}
                  disabled={loading}
                  className="form-input pl-10 pr-10 appearance-none cursor-pointer"
                  required
                >
                  <option value="">Select your education level</option>
                  {educationLevels.map((level) => (
                    <option key={level} value={level}>
                      {level}
                    </option>
                  ))}
                </select>
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l9-5-9-5-9 5 9 5z" />
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 14l6.16-3.422a12.083 12.083 0 01.665 6.479A11.952 11.952 0 0012 20.055a11.952 11.952 0 00-6.824-2.998 12.078 12.078 0 01.665-6.479L12 14z" />
                  </svg>
                </div>
                <div className="absolute inset-y-0 right-0 pr-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                  </svg>
                </div>
              </div>
            </div>

            {/* Phone Number Field */}
            <div>
              <label className="form-label">
                Phone Number <span className="text-red-500">*</span>
              </label>
              <div className="relative">
                <input
                  type="tel"
                  name="phone_no"
                  placeholder="Enter your phone number"
                  value={formData.phone_no}
                  onChange={handleInputChange}
                  disabled={loading}
                  className="form-input pl-10"
                  required
                />
                <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
                  <svg className="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                  </svg>
                </div>
              </div>
              {formData.phone_no && formData.phone_no.trim().length < 10 && (
                <p className="mt-1 text-xs text-red-500">Phone number must be at least 10 digits</p>
              )}
              <p className="mt-1 text-xs text-gray-500">
                Include country code (e.g., +1234567890)
              </p>
            </div>

            {/* Progress Indicator */}
            <div className="bg-gray-200 rounded-full h-2">
              <div 
                className="bg-gradient-to-r from-indigo-500 to-blue-500 h-2 rounded-full transition-all duration-300"
                style={{ 
                  width: `${(Object.values(formData).filter(Boolean).length / 4) * 100}%` 
                }}
              ></div>
            </div>
            <p className="text-xs text-gray-500 text-center">
              {Object.values(formData).filter(Boolean).length}/4 fields completed
            </p>

            {/* Submit Button */}
            <div className="space-y-4">
              <button
                type="submit"
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
                  {loading ? "Completing Registration..." : "Complete Registration"}
                </div>
              </button>

              {/* Form Validation Summary */}
              {!isFormValid && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                  <div className="flex">
                    <div className="flex-shrink-0">
                      <svg className="h-5 w-5 text-yellow-400" viewBox="0 0 20 20" fill="currentColor">
                        <path fillRule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <div className="ml-3">
                      <h3 className="text-sm font-medium text-yellow-800">
                        Please complete all required fields
                      </h3>
                      <div className="mt-2 text-sm text-yellow-700">
                        <ul className="list-disc pl-5 space-y-1">
                          {formData.name.trim().length < 2 && <li>Enter a valid name (min 2 characters)</li>}
                          {(!formData.age || parseInt(formData.age) < 16 || parseInt(formData.age) > 100) && <li>Enter age between 16-100</li>}
                          {!formData.education_level && <li>Select your education level</li>}
                          {formData.phone_no.trim().length < 10 && <li>Enter a valid phone number</li>}
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </div>

            {/* Message Display */}
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
          </form>

          {/* Footer */}
          <div className="mt-8 pt-6 border-t border-gray-200">
            <div className="flex items-center justify-center space-x-2 text-xs text-gray-500">
              <svg className="h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 15v2m-6 4h12a2 2 0 002-2v-6a2 2 0 00-2-2H6a2 2 0 00-2 2v6a2 2 0 002 2zm10-10V7a4 4 0 00-8 0v4h8z" />
              </svg>
              <span>Your information is secure and encrypted</span>
            </div>
          </div>
        </div>

        {/* Side Tips */}
        <div className="mt-8 bg-indigo-50 rounded-lg p-6 animate-slide-in">
          <h3 className="text-lg font-medium text-indigo-900 mb-4">
            Why we need this information
          </h3>
          <div className="space-y-3 text-sm text-indigo-700">
            <div className="flex items-start space-x-3">
              <svg className="h-5 w-5 text-indigo-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
              </svg>
              <span><strong>Personalized Recommendations:</strong> We'll suggest careers that match your education level and experience.</span>
            </div>
            <div className="flex items-start space-x-3">
              <svg className="h-5 w-5 text-indigo-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
              </svg>
              <span><strong>Age-Appropriate Guidance:</strong> Career paths and timelines tailored to your life stage.</span>
            </div>
            <div className="flex items-start space-x-3">
              <svg className="h-5 w-5 text-indigo-500 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              <span><strong>Direct Communication:</strong> We'll send important updates and opportunities via phone when needed.</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RegistrationForm;