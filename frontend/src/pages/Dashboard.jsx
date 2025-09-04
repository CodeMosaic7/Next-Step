import Header from "../components/Header";
import Footer from "../components/Footer";
import ProfileCard from "../components/ProfileCard";
import SavedCareers from "../components/SavedCareers";
import CareerGoalTracker from "../components/CareerGoalTracker";
import CompletedAssessment from "../components/CompletedAssessment";
import AchievementsBadges from "../components/AchievementsBadges";

const Dashboard = () => {
  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Left Column */}
          <div className="space-y-6">
            <ProfileCard />
            <SavedCareers />
          </div>

          {/* Middle Column */}
          <div className="space-y-6">
            <CareerGoalTracker />
          </div>
          
          {/* Right Column */}
          <div className="space-y-6">
            <CompletedAssessment />
          </div>
        </div>
        
        {/* Full Width Bottom Section */}
        <div className="mt-8">
          <AchievementsBadges />
        </div>
      </div>
      
      <Footer />
    </div>
  );
};

export default Dashboard;