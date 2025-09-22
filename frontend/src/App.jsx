import {Router,Routes,Route} from "react-router-dom"
import { AuthProvider ,Login,ProtectedRoute,PublicRoute} from "./pages/Login";
import Home from "./pages/Home";
import RegistrationForm from "./pages/RegistrationForm"
import Dashboard from "./pages/Dashboard"
import Assessment from "./pages/Assessment"
import CareerDashboard from "./pages/CareerDashboard"
import Chatbot from "./pages/Chatbot"
import MentorBoard from "./pages/MentorBoard"
import Resources from "./pages/Resources"


function App() {
  return (
      <AuthProvider>
        <Routes>
          {/* Public Routes - accessible without authentication */}
          <Route 
            path="/" 
            element={
              <PublicRoute redirectIfAuthenticated={false}>
                <Home/>
              </PublicRoute>
            } 
          />
          
          <Route 
            path="/login" 
            element={
              <PublicRoute>
                <Login />
              </PublicRoute>
            } 
          />

          {/* Protected Routes - require authentication */}
          <Route 
            path="/register" 
            element={
              <ProtectedRoute>
                <RegistrationForm />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/dashboard" 
            element={
              <ProtectedRoute>
                <Dashboard />
              </ProtectedRoute>
            } 
          />
          
          <Route 
            path="/Chatbot" 
            element={
              <ProtectedRoute >
                <Chatbot />
              </ProtectedRoute>
            } 
          />

          <Route 
            path="/Assessment" 
            element={
              <ProtectedRoute >
                <Assessment />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/career-dashboard" 
            element={
              <ProtectedRoute >
                <CareerDashboard />
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/mentor-board" 
            element={
              <ProtectedRoute >
                <MentorBoard/>
              </ProtectedRoute>
            } 
          />
          <Route 
            path="/resources" 
            element={
              <ProtectedRoute >
                <Resources />
              </ProtectedRoute>
            } 
          />
        </Routes>
      </AuthProvider>
    
  );
}
export default App;