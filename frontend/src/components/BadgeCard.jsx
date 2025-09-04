const BadgeCard = ({ badge }) => {
  const getBadgeIcon = (type) => {
    const icons = {
      'Explorer': '🗺️',
      'Strategist': '🏆',
      'Achiever': '🎯',
      'Learner': '📚',
      'Networker': '🤝',
      'Portfolio': '📁'
    };
    return icons[type] || '🏅';
  };

  return (
    <div className="bg-gray-100 rounded-lg p-4 text-center">
      <div className="text-2xl mb-2">{getBadgeIcon(badge.type)}</div>
      <h4 className="text-sm font-semibold text-gray-900 mb-1">{badge.type} Badge</h4>
      <p className="text-xs text-gray-600">{badge.description}</p>
    </div>
  );
};

export default BadgeCard;