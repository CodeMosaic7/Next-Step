import { User } from 'lucide-react';

const Header = () => {
  function openLogin() {
    window.location.href = "/login";
  }
  return (
    
      <header className="bg-white shadow-lg border-b fixed w-full z-10 opacity-90">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">✱ NextStep</span>
            </div>
            
            {/* Navigation */}
            <nav className="hidden md:flex space-x-8">
              <a href="/#" className="text-gray-700 hover:text-blue-600 px-3 py-2">Home</a>
              <a href="/Assessment" className="text-blue-600 font-medium px-3 py-2">Assessment</a>
              <a href="/career-dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2">Careers</a>
              <a href="/mentor-board" className="text-gray-700 hover:text-blue-600 px-3 py-2">Mentors</a>
              <a href="/resources" className="text-gray-700 hover:text-blue-600 px-3 py-2">Resources</a>
              <a href="/dashboard" className="text-gray-700 hover:text-blue-600 px-3 py-2">Profile</a>
              <button
              onClick={openLogin}
              className="flex items-center gap-2 px-4 py-2 bg-blue-600 text-white rounded-xl hover:bg-blue-700 transition"
            >
              <User size={18} />
              Login
            </button>
            </nav>
            {/* Profile Avatar */}
            <div className="flex items-center">
              <div className="w-8 h-8 bg-gray-300 rounded-full flex items-center justify-center">
                <User className="w-5 h-5 text-gray-600" />
              </div>
            </div>
          </div>
        </div>
      </header>
  );
};

export default Header;
