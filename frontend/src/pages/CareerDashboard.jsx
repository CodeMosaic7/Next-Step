import { useState } from "react";
import { Home, User } from "lucide-react";
import CareerCard from "../components/CareerCard";
import Dropdown from "../components/Dropdown";
import Header from "../components/Header";
import Footer from "../components/Footer";
import FilterBar from "../components/FilterBar";
const CareerDashboard = () => {
  const [filters, setFilters] = useState({
    location: '',
    salary: '',
    demand: '',
    recommendation: ''
  });

  const handleFilterChange = (filterType, value) => {
    setFilters(prev => ({
      ...prev,
      [filterType]: value
    }));
  };

  const handleFavorite = (careerTitle, isFavorited) => {
    console.log(`${careerTitle} ${isFavorited ? 'added to' : 'removed from'} favorites`);
  };

  // Mock data - in real app this would come from API
  const careers = [
    {
      title: "AI Ethicist",
      description: "Ensure responsible development and implementation of artificial intelligence systems and applications for responsible AI development.",
      salary: "$105,000 - $190,000 per year",
      education: "Master's Degree or Higher in Philosophy, Ethics, Computer Science",
      demand: "High"
    },
    {
      title: "Data Scientist",
      description: "Uses advanced analytics and machine learning algorithms to help organizations make data-driven business and strategic decisions.",
      salary: "$90,000 - $160,000 per year",
      education: "Master's Degree in Statistics, Mathematics, Computer Science",
      demand: "High"
    },
    {
      title: "UX/UI Designer",
      description: "Design user experiences and user planning interfaces for software applications and websites, focusing on user satisfaction and usability.",
      salary: "$75,000 - $130,000 per year",
      education: "Bachelor's Degree in Graphic Design, Human-Computer Interaction, or related field",
      demand: "Medium"
    },
    {
      title: "Renewable Energy Engineer",
      description: "Design, develop, and maintain renewable energy systems, working with solar, wind, and hydro systems for clean energy solutions.",
      salary: "$85,000 - $135,000 per year",
      education: "Bachelor's Degree in Engineering (Electrical, Mechanical, Environmental)",
      demand: "High"
    },
    {
      title: "Digital Marketing Specialist",
      description: "Develop and implement online marketing strategies using digital channels, including social media, SEO, PPC, and content marketing.",
      salary: "$50,000 - $85,000 per year",
      education: "Bachelor's Degree in Marketing, Communications, or related field",
      demand: "Medium"
    },
    {
      title: "Environmental Consultant",
      description: "Advise businesses and government agencies on environmental risks, sustainable practices to minimize environmental impact.",
      salary: "$70,000 - $95,000 per year",
      education: "Bachelor's or Master's Degree in Environmental Science or Engineering",
      demand: "Medium"
    },
    {
      title: "Cybersecurity Analyst",
      description: "Protects computer systems and networks from cyber threats, detecting and preventing attacks and security incidents.",
      salary: "$80,000 - $130,000 per year",
      education: "Bachelor's Degree in Cybersecurity, Computer Science, or Information Technology",
      demand: "High"
    },
    {
      title: "Content Creator",
      description: "Produces engaging and creative content for various channels like video, blogs, social media, targeting specific audiences.",
      salary: "$40,000 - $80,000 per year",
      education: "Bachelor's Degree in Communications, Marketing, or self-taught/freelance",
      demand: "Medium"
    },
    {
      title: "Biomedical Scientist",
      description: "Conduct research to understand diseases, develop treatments, and improve knowledge through work in laboratories and research facilities.",
      salary: "$70,000 - $130,000 per year",
      education: "Bachelor's or Master's Degree in Biomedical Science, Biology, or related field",
      demand: "Medium"
    },
    {
      title: "Financial Advisor",
      description: "Help individuals and investment guidance to individuals and businesses on investment strategies and wealth management.",
      salary: "$60,000 - $120,000 per year",
      education: "Bachelor's Degree in Finance, Economics, or Business, plus certification",
      demand: "Medium"
    },
    {
      title: "Urban Planner",
      description: "Design and manage the development of cities and regions, balancing economic, social, and environmental factors in city development.",
      salary: "$65,000 - $95,000 per year",
      education: "Master's Degree in Urban Planning or related field",
      demand: "Low"
    },
    {
      title: "Game Developer",
      description: "Create video games, from concept and design to programming and testing, for various platforms and audiences.",
      salary: "$70,000 - $140,000 per year",
      education: "Bachelor's Degree in Computer Science, Game Development, or related field",
      demand: "Medium"
    }
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Page Title */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">Your Personalized Career Journey</h1>
        </div>

        {/* Filter Bar */}
        <FilterBar filters={filters} onFilterChange={handleFilterChange} />

        {/* Career Cards Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          {careers.map((career, index) => (
            <CareerCard
              key={index}
              career={career}
              onFavorite={handleFavorite}
            />
          ))}
        </div>
      </main>
      <Footer />
    </div>
  );
};

export default CareerDashboard;