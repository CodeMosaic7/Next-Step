const AchievementsBadges = () => {
  const badges = [
    { type: 'Explorer', description: 'Completed your career assessment' },
    { type: 'Strategist', description: 'Set up your first goal' },
    { type: 'Achiever', description: 'Achieved goal for a month' },
    { type: 'Learner', description: 'Love to learn Badge' },
    { type: 'Networker', description: 'Connected to mentor' },
    { type: 'Portfolio', description: 'Portfolio Badge' }
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-6">Achievements & Badges</h2>
      
      <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
        {badges.map((badge, index) => (
          <BadgeCard key={index} badge={badge} />
        ))}
      </div>
    </div>
  );
};

export default AchievementsBadges;