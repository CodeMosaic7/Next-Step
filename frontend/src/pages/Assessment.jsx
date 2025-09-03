import React, { useState } from 'react';
import { Home, User } from 'lucide-react';
import Footer from '../components/Footer';
export default function Assessment() {
  const [selectedOption, setSelectedOption] = useState('');

  const handleOptionChange = (value) => {
    setSelectedOption(value);
  };

  const handleSubmit = () => {
    if (selectedOption) {
      alert(`Selected: ${selectedOption}`);
      // Handle submission logic here
    } else {
      alert('Please select an option before submitting');
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <header className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            {/* Logo */}
            <div className="flex items-center">
              <span className="text-2xl font-bold text-blue-600">✱ NextStep</span>
            </div>
            
            {/* Navigation */}
            <nav className="hidden md:flex space-x-8">
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2">Home</a>
              <a href="#" className="text-blue-600 font-medium px-3 py-2">Assessment</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2">Careers</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2">Mentors</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2">Resources</a>
              <a href="#" className="text-gray-700 hover:text-blue-600 px-3 py-2">Profile</a>
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

      {/* Main Content */}
      <main className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        {/* Progress Bar */}
        <div className="mb-8">
          <div className="w-full bg-gray-200 rounded-full h-2 mb-4">
            <div className="bg-blue-600 h-2 rounded-full" style={{ width: '20%' }}></div>
          </div>
          <p className="text-center text-gray-600 font-medium">
            You're closer to finding your dream career!
          </p>
        </div>

        {/* Question Section */}
        <div className="bg-white rounded-lg shadow-sm p-8 mb-8">
          <div className="mb-8">
            <h2 className="text-xl font-semibold text-gray-800 mb-4">Question 1 of 5</h2>
            <p className="text-gray-600 text-lg">
              When facing a complex problem, what approach do you typically prefer?
            </p>
          </div>

          {/* Answer Options */}
          <div className="space-y-4">
            <label className="flex items-start space-x-3 p-4 rounded-lg border hover:bg-gray-50 cursor-pointer transition-colors">
              <input
                type="radio"
                name="problem-approach"
                value="analyze-research"
                checked={selectedOption === 'analyze-research'}
                onChange={() => handleOptionChange('analyze-research')}
                className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-gray-700">
                I prefer to analyze data and research extensively before making a decision.
              </span>
            </label>

            <label className="flex items-start space-x-3 p-4 rounded-lg border hover:bg-gray-50 cursor-pointer transition-colors">
              <input
                type="radio"
                name="problem-approach"
                value="creative-brainstorming"
                checked={selectedOption === 'creative-brainstorming'}
                onChange={() => handleOptionChange('creative-brainstorming')}
                className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-gray-700">
                I enjoy brainstorming creative solutions and thinking outside the box.
              </span>
            </label>

            <label className="flex items-start space-x-3 p-4 rounded-lg border hover:bg-gray-50 cursor-pointer transition-colors">
              <input
                type="radio"
                name="problem-approach"
                value="collaborate-consensus"
                checked={selectedOption === 'collaborate-consensus'}
                onChange={() => handleOptionChange('collaborate-consensus')}
                className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-gray-700">
                I like to collaborate with others, discussing ideas to find a consensus.
              </span>
            </label>

            <label className="flex items-start space-x-3 p-4 rounded-lg border hover:bg-gray-50 cursor-pointer transition-colors">
              <input
                type="radio"
                name="problem-approach"
                value="experiment-learn"
                checked={selectedOption === 'experiment-learn'}
                onChange={() => handleOptionChange('experiment-learn')}
                className="mt-1 w-4 h-4 text-blue-600 border-gray-300 focus:ring-blue-500"
              />
              <span className="text-gray-700">
                I prefer to jump in and experiment, learning as I go along.
              </span>
            </label>
          </div>

          {/* Submit Button */}
          <div className="mt-8 text-center">
            <button
              onClick={handleSubmit}
              className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-8 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
            >
              Submit Assessment
            </button>
          </div>
        </div>
      </main>

      {/* Footer */}
      <Footer/>
    </div>
  );
}