;
import Header from "../components/Header";
import MentorCard from "../components/MentorCard";
import BookingSection from "../components/BookingSection";
const MentorHeroSection = () => {
  return (
    <div className="bg-gradient-to-r from-blue-50 to-indigo-100 py-16">
      <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
        <h1 className="text-4xl font-bold text-gray-900 mb-4">
          Connect with Expert Mentors
        </h1>
        <p className="text-lg text-gray-600 max-w-2xl mx-auto">
          Get personalized insights and personalized guidance from industry leaders who are ready to
          support your career journey.
        </p>
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
