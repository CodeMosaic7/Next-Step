import {useState} from 'react';
import Header from '../components/Header';
import ResourceCard from '../components/ResourceCard';
import SearchFilterBar from '../components/SearchFilterBar';

const ResourcesHero = () => {
  return (
    <div className="bg-white py-12">
      <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Resources Library
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Explore our curated collection of essential videos, books, and blogs to accelerate your
          career journey
        </p>
      </div>
    </div>
  );
};
                                                      
const Resources = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All Resources');

  const resources = [
    {
      title: "Introduction to Machine Learning with Python",
      duration: "45 mins",
      students: "2.1k students",
      badges: ["Beginner", "Free"],
      emoji: "🤖"
    },
    {
      title: "Personal Finance for Young Professionals",
      duration: "1h 30mins",
      students: "1.5k students", 
      badges: ["Beginner", "Popular"],
      emoji: "💰"
    },
    {
      title: "Full-Stack Web Development Bootcamp",
      duration: "8 weeks",
      students: "3.2k students",
      badges: ["Intermediate", "Premium"],
      emoji: "💻"
    },
    {
      title: "Mastering Digital Marketing: SEO & SEM",
      duration: "2h 15mins",
      students: "900 students",
      rating: "4.8",
      badges: ["Advanced", "Premium"],
      emoji: "📈"
    },
    {
      title: "Understanding Cognitive Biases",
      duration: "1h 45mins", 
      students: "1.2k students",
      badges: ["Intermediate", "Free"],
      emoji: "🧠"
    },
    {
      title: "Agile Project Management Certification",
      duration: "4 weeks",
      students: "2.8k students",
      badges: ["Advanced", "Premium"],
      emoji: "📋"
    },
    {
      title: "Practical Data Science with R",
      duration: "3h 20mins",
      students: "1.8k students", 
      badges: ["Intermediate", "Free"],
      emoji: "📊"
    },
    {
      title: "Effective Communication Strategies",
      duration: "1h 15mins",
      students: "2.5k students",
      badges: ["Beginner", "Popular"],
      emoji: "💬"
    },
    {
      title: "Fundamentals of Graphic Design",
      duration: "6 weeks",
      students: "1.9k students",
      badges: ["Beginner", "Premium"],
      emoji: "🎨"
    }
  ];

  const filteredResources = resources.filter(resource => 
    resource.title.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      <ResourcesHero />
      <SearchFilterBar 
        searchTerm={searchTerm}
        setSearchTerm={setSearchTerm}
        selectedCategory={selectedCategory}
        setSelectedCategory={setSelectedCategory}
      />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredResources.map((resource, index) => (
            <ResourceCard key={index} resource={resource} />
          ))}
        </div>
        
        {filteredResources.length === 0 && (
          <div className="text-center py-12">
            <p className="text-gray-500">No resources found matching your search.</p>
          </div>
        )}
      </div>
    </div>
  );
};

export default Resources;