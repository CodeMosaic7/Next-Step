import React from 'react';
import { User, Target, Users, BookOpen } from 'lucide-react';

const Header = () => {
  return (
    <header className="bg-white shadow-sm">
      <nav className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center py-4">
          <div className="flex items-center">
            <div className="text-2xl font-bold text-blue-600">NextStep</div>
          </div>
          <div className="hidden md:flex space-x-8">
            <a href="/home" className="text-gray-700 hover:text-blue-600">Home</a>
            <a href="/assessment" className="text-gray-700 hover:text-blue-600">Assessment</a>
            <a href="/career-dashboard" className="text-gray-700 hover:text-blue-600">Careers</a>
            <a href="/mentors" className="text-gray-700 hover:text-blue-600">Mentors</a>
            <a href="/resources" className="text-gray-700 hover:text-blue-600">Resources</a>
            <a href="/dashboard" className="text-gray-700 hover:text-blue-600">Profile</a>
          </div>
        </div>
      </nav>
    </header>
  );
};

export default Header;