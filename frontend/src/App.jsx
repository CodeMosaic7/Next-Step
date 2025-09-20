import { Routes, Route } from 'react-router-dom';

import Home from "./pages/Home";
import Login from "./pages/Login";
import Assessment from "./pages/Assessment";
import CareerDashboard from "./pages/CareerDashboard";
import MentorBoard from "./pages/MentorBoard";
import Resources from './pages/Resources';
import Dashboard from './pages/Dashboard';
import Chatbot from './pages/Chatbot';
import RegistrationForm from './pages/RegistrationForm';

const App = () => {
  return (
    <Routes>
      <Route path="/" element={<Home />} />
      <Route path="/login" element={<Login />} />
      <Route path="/assessment" element={<Assessment />} />
      <Route path="/career-dashboard" element={<CareerDashboard />} />
      <Route path="/mentors" element={<MentorBoard />} />
      <Route path="/resources" element={<Resources />} />
      <Route path="/dashboard" element={<Dashboard />} />
      <Route path="/chatbot" element={<Chatbot />} />
      <Route path="/registration" element={<RegistrationForm />} />

    </Routes>
  )
}


export default App;