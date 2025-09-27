import { createContext, useContext, useState, useEffect } from 'react';
import {   
  Navigate, 
  useLocation,
  } from 'react-router-dom';
import Footer from '../components/Footer';
// 1. Auth Context
const AuthContext = createContext();

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within AuthProvider');
  }
  return context;
};

// 2. Auth Provider
export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check authentication status on app load
    const token = localStorage.getItem('authToken');
    const userData = localStorage.getItem('userData');
    
    if (token && userData) {
      try {
        const parsedUser = JSON.parse(userData);
        setUser(parsedUser);
      } catch (error) {
        console.error('Error parsing user data:', error);
        localStorage.removeItem('authToken');
        localStorage.removeItem('userData');
      }
    }
    setLoading(false);
  }, []);

  const login = (token, userData) => {
    localStorage.setItem('authToken', token);
    localStorage.setItem('userData', JSON.stringify(userData));
    setUser(userData);
  };

  const logout = () => {
    localStorage.removeItem('authToken');
    localStorage.removeItem('userData');
    setUser(null);
  };

  return (
    <AuthContext.Provider 
      value={{ 
        user, 
        login, 
        logout, 
        loading,
        isAuthenticated: !!user,
        isRegistered: user?.isRegistered || false
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

// 3. Protected Route Component
export const ProtectedRoute = ({ children, requiresRegistration = false }) => {
  const { isAuthenticated, loading, isRegistered } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  // Not authenticated - redirect to login
  if (!isAuthenticated) {
    return <Navigate to="/login" state={{ from: location }} replace />;
  }

  // // Authenticated but not registered - redirect to register
  // if (isAuthenticated && !isRegistered && location.pathname !== '/register') {
  //   return <Navigate to="/register" replace />;
  // }

  // Authenticated and registered but trying to access register page
  // if (isAuthenticated && isRegistered && location.pathname === '/register') {
  //   return <Navigate to="/dashboard" replace />;
  // }

  // // Additional check for routes that require registration
  // if (requiresRegistration && !isRegistered) {
  //   return <Navigate to="/register" replace />;
  // }

  return children;
};

// 4. Public Route (for login and home pages)
export const PublicRoute = ({ children, redirectIfAuthenticated = true }) => {
  const { isAuthenticated, loading, isRegistered } = useAuth();
  const location = useLocation();

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>
    );
  }

  if (isAuthenticated && redirectIfAuthenticated) {
    // Determine redirect destination based on registration status
    const redirectTo = isRegistered ? '/dashboard' : '/register';
    const from = location.state?.from?.pathname || redirectTo;
    return <Navigate to={from} replace />;
  }

  return children;
};

// 5. Updated Login Component with Firebase integration
export const Login = () => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");
  const { login, logout } = useAuth();

  const API_BASE_URL = import.meta.env.VITE_PUBLIC_API_URL || "http://127.0.0.1:8000";

  const handleRegister = async () => {
    try {
      setLoading(true);
      setMessage("");
      
      // Import your Firebase register function
      const { register } = await import("../firebase");
      await register(email, password);
      
      setMessage("✅ User registered successfully! Please sign in.");
      
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
      
      // Import Firebase functions
      const { login: firebaseLogin, auth } = await import("../firebase");
      const axios = (await import("axios")).default;
      
      // Login with Firebase
      await firebaseLogin(email, password);
      
      // Get Firebase ID token
      const token = await auth.currentUser.getIdToken();
      
      // Test protected endpoint to get user registration status
      const response = await axios.get(`${API_BASE_URL}/protected`, {
        headers: { 
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json'
        },
        timeout: 10000,
      });
      
      console.log("Backend Response:", response.data);
      
      // Create user data object - check if response.data.user has registration info
      const userData = {
        email: email,
        uid: auth.currentUser.uid,
        ...response.data.user, // Spread any additional user data from backend
        isRegistered: response.data.user?.isRegistered || false // Backend should provide this
      };
      
      // Use the login function from context
      login(token, userData);
      
      setMessage(`✅ Login successful! Welcome ${userData.email || response.data.user}`);
      
      // Navigation will be handled automatically by ProtectedRoute logic
      
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
      
      // Import Firebase logout
      const { logout: firebaseLogout } = await import("../firebase");
      await firebaseLogout();
      
      // Use context logout to clear local state
      logout();
      
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
    <div className="min-h-screen bg-gray-50 flex items-center justify-center py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <div className="bg-white rounded-2xl shadow-lg border border-gray-200 overflow-hidden">
          
          {/* Header */}
          <div className="bg-white px-8 pt-8 pb-6 text-center">
            <div className="w-16 h-16 bg-blue-500 rounded-2xl flex items-center justify-center mx-auto mb-4">
              <svg className="w-8 h-8 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
            </div>
            <h2 className="text-2xl font-bold text-gray-900 mb-2">
              Next-Step
            </h2>
            <p className="text-gray-500 text-sm">
              Sign in to your account or create a new one
            </p>
          </div>

          {/* Form */}
          <div className="px-8 pb-8">
            <div className="space-y-6">
              {/* Email Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Email Address *
                </label>
                <input
                  type="email"
                  placeholder="Enter your email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  disabled={loading}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 placeholder-gray-400"
                  required
                />
              </div>

              {/* Password Input */}
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Password *
                </label>
                <input
                  type="password"
                  placeholder="Enter your password (min 6 chars)"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  disabled={loading}
                  className="w-full px-3 py-3 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent transition-all duration-200 text-gray-900 placeholder-gray-400"
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
                  className="w-full bg-blue-600 text-white py-3 px-4 rounded-lg font-medium hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
                >
                  {loading && (
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  )}
                  {loading ? "Signing In..." : "Sign In"}
                </button>
                
                <button 
                  onClick={handleRegister}
                  disabled={loading || !isFormValid}
                  className="w-full bg-gray-100 text-gray-700 py-3 px-4 rounded-lg font-medium hover:bg-gray-200 focus:outline-none focus:ring-2 focus:ring-gray-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200 flex items-center justify-center"
                >
                  {loading && (
                    <svg className="animate-spin -ml-1 mr-3 h-5 w-5 text-gray-700" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                      <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                      <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                    </svg>
                  )}
                  {loading ? "Creating Account..." : "Create Account"}
                </button>
                
                <button 
                  onClick={handleLogout}
                  disabled={loading}
                  className="w-full bg-red-50 text-red-700 py-3 px-4 rounded-lg font-medium hover:bg-red-100 focus:outline-none focus:ring-2 focus:ring-red-500 focus:ring-offset-2 disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-200"
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
                <div className={`rounded-lg p-4 border-l-4 ${message.includes("✅") ? "bg-green-50 border-green-400" : "bg-red-50 border-red-400"}`}>
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
                      <p className={`text-sm font-medium ${message.includes("✅") ? "text-green-800" : "text-red-800"}`}>
                        {message}
                      </p>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>

          {/* Footer */}
          <Footer />
        </div>
      </div>
    </div>
  );
}