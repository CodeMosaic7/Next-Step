import { useState } from "react";
import { User, Facebook, Twitter, Instagram, Linkedin, Github, Car } from 'lucide-react';


export default function CareerDetails() {
    const [tab, setTab] = useState('overview');
    const tabs = [
    { id: 'overview', label: 'Overview' },
    { id: 'skills', label: 'Skills Needed' },
    { id: 'resources', label: 'Resources' },
    { id: 'pathway', label: 'Pathway' }
  ];

  const renderContent=()=>{
    switch(tab){
        case 'overview':
            return <CareerOverview />;
        case 'skills':
            return <SkillsNeeded />;
        case 'resources':
            return <Resources />;
        case 'pathway':
            return <Pathway />;
        default:
            return <CareerOverview />;
    }
  }

    return (
      <div className="min-h-screen bg-white">
      <Header />
      
      <HeroSection
        title="Data Scientist"
        subtitle="Unlock your potential and shape your future."
        illustration={<DataScientistIllustration />}
      />

      <TabNavigation 
        activeTab={activeTab}
        onTabChange={setActiveTab}
        tabs={tabs}
      />

      <ContentSection title="">
        {renderTabContent()}
      </ContentSection>

      <RelatedCareers />
      
      <Footer />
    </div>

    )

}