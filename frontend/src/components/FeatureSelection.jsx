import { User, Target, Users, BookOpen } from 'lucide-react';

import FeatureCard from './FeatureCard';
const FeaturesSection = () => {
  const features = [
    {
      icon: Target,
      title: "Personalized Quiz",
      description: "Uncover your strengths and interests with our AI-powered assessment."
    },
    {
      icon: User,
      title: "Tailored Recommendations",
      description: "Receive career paths aligned with your profile and market demand."
    },
    {
      icon: Users,
      title: "Expert Mentorship",
      description: "Connect with industry professionals for guidance and support."
    },
    {
      icon: BookOpen,
      title: "Learning Resources",
      description: "Access curated content to upskill and explore new fields."
    }
  ];

  return (
    <section className="py-16 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4">
        <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
          Discover Your Potential
        </h2>
        
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, index) => (
            <FeatureCard key={index} {...feature} />
          ))}
        </div>
      </div>
    </section>
  );
};
export default FeaturesSection;