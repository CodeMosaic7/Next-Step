import { useState, useEffect } from "react";
import { Sparkles, ArrowRight } from 'lucide-react';
import Header from "../components/Header";
import MentorCard from "../components/MentorCard";
import BookingSection from "../components/BookingSection";
const MentorHeroSection = () => {
  const [isVisible, setIsVisible] = useState(false);
  
  useEffect(() => {
    setIsVisible(true);
  }, []);

  return (
    <div className="relative overflow-hidden bg-gradient-to-r from-blue-50 to-indigo-100 py-20 sm:py-24">
      {/* Subtle Background Decoration */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute top-0 right-0 w-72 h-72 bg-indigo-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
        <div className="absolute bottom-0 left-0 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-3xl opacity-30 animate-pulse"></div>
      </div>

      <div className="relative max-w-5xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        {/* Badge */}
        <div className={`inline-flex items-center gap-2 px-4 py-2 rounded-full bg-white/80 backdrop-blur-sm border border-indigo-200 mb-6 transition-all duration-700 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 -translate-y-4'}`}>
          <Sparkles className="w-4 h-4 text-indigo-600" />
          <span className="text-sm font-medium text-indigo-900">Trusted by 10,000+ professionals</span>
        </div>

        {/* Main Heading */}
        <h1 className={`text-5xl sm:text-6xl font-bold text-gray-900 mb-6 transition-all duration-700 delay-150 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          Connect with{' '}
          <span className="bg-gradient-to-r from-blue-600 to-indigo-600 bg-clip-text text-transparent">
            Expert Mentors
          </span>
        </h1>

        {/* Description */}
        <p className={`text-xl text-gray-600 max-w-3xl mx-auto mb-10 leading-relaxed transition-all duration-700 delay-300 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          Get personalized insights and guidance from industry leaders who are ready to support your career journey.
        </p>

        {/* CTA Buttons */}
        <div className={`flex flex-col sm:flex-row gap-4 justify-center mb-12 transition-all duration-700 delay-450 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <button className="group inline-flex items-center justify-center gap-2 px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 text-white font-semibold rounded-xl transition-all duration-300 hover:scale-105 hover:shadow-xl hover:shadow-indigo-500/30">
            Find Your Mentor
            <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform duration-300" />
          </button>
          <button className="px-8 py-4 bg-white text-gray-900 font-semibold rounded-xl border-2 border-gray-300 transition-all duration-300 hover:border-indigo-300 hover:bg-gray-50 hover:scale-105">
            Become a Mentor
          </button>
        </div>

        {/* Stats */}
        <div className={`grid grid-cols-1 sm:grid-cols-3 gap-6 max-w-3xl mx-auto transition-all duration-700 delay-600 ${isVisible ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-4'}`}>
          <div className="p-6 rounded-xl bg-white/60 backdrop-blur-sm border border-gray-200 hover:border-indigo-300 hover:bg-white/80 transition-all duration-300 hover:scale-105 hover:shadow-lg">
            <div className="text-3xl font-bold text-indigo-600 mb-1">500+</div>
            <div className="text-sm text-gray-600">Expert Mentors</div>
          </div>
          <div className="p-6 rounded-xl bg-white/60 backdrop-blur-sm border border-gray-200 hover:border-indigo-300 hover:bg-white/80 transition-all duration-300 hover:scale-105 hover:shadow-lg">
            <div className="text-3xl font-bold text-indigo-600 mb-1">10k+</div>
            <div className="text-sm text-gray-600">Sessions Done</div>
          </div>
          <div className="p-6 rounded-xl bg-white/60 backdrop-blur-sm border border-gray-200 hover:border-indigo-300 hover:bg-white/80 transition-all duration-300 hover:scale-105 hover:shadow-lg">
            <div className="text-3xl font-bold text-indigo-600 mb-1">95%</div>
            <div className="text-sm text-gray-600">Success Rate</div>
          </div>
        </div>
      </div>
    </div>
  );
};



const MentorBoard = () => {
  const mentors = [
    {
      name: "Dr. Evelyn Reed",
      title: "Lead Data Scientist at Google",
      description: "Expertise in machine learning and AI applications in healthcare and finance",
      initials: "ER",
      badges: [
        { text: "Machine Learning", variant: "blue" },
        { text: "Available", variant: "success" }
      ]
    },
    {
      name: "Mr. Alex Thompson",
      title: "Senior Software Engineer at Microsoft",
      description: "Full-stack development, cloud architecture, and team leadership experience",
      initials: "AT",
      badges: [
        { text: "Full Stack", variant: "blue" },
        { text: "Available", variant: "success" }
      ]
    },
    {
      name: "Ms. Sarah Kim",
      title: "Product Manager at Apple",
      description: "Product strategy, user experience design, and cross-functional team management",
      initials: "SK",
      badges: [
        { text: "Product", variant: "blue" },
        { text: "Available", variant: "success" }
      ]
    },
    {
      name: "Dr. Ben Carter",
      title: "Principal Research Scientist at Amazon",
      description: "Artificial intelligence research, natural language processing, and publications",
      initials: "BC",
      badges: [
        { text: "Research", variant: "blue" },
        { text: "Available", variant: "success" }
      ]
    },
    {
      name: "Ms. Olivia Grace",
      title: "UX Designer at Netflix",
      description: "User interface design, user research, and accessibility-focused design solutions",
      initials: "OG",
      badges: [
        { text: "UX Design", variant: "blue" },
        { text: "Available", variant: "success" }
      ]
    },
    {
      name: "Mr. Ryan Chang",
      title: "Engineering Manager at Tesla",
      description: "Engineering leadership, autonomous systems development, and team building",
      initials: "RC",
      badges: [
        { text: "Engineering", variant: "blue" },
        { text: "Available", variant: "success" }
      ]
    }
  ];

  return (
    <div className="min-h-screen bg-white">
      <Header />
      <MentorHeroSection />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <h2 className="text-2xl font-bold text-gray-900 mb-8">Our Mentors</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-12">
          {mentors.map((mentor, index) => (
            <MentorCard key={index} mentor={mentor} />
          ))}
        </div>
      </div>
      
      <BookingSection />
    </div>
  );
};

export default MentorBoard;
