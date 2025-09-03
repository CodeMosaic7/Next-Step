
import Badge from './Badge';
const MentorCard = ({ mentor }) => {
  return (
    <div className="bg-white rounded-lg shadow-md p-6 hover:shadow-lg transition-shadow">
      <div className="flex flex-col items-center text-center">
        <div className="w-16 h-16 bg-gray-300 rounded-full mb-4 flex items-center justify-center">
          <span className="text-xl font-semibold">{mentor.initials}</span>
        </div>
        <h3 className="text-lg font-semibold text-gray-900 mb-1">{mentor.name}</h3>
        <p className="text-sm text-gray-600 mb-2">{mentor.title}</p>
        <p className="text-xs text-gray-500 mb-4 text-center leading-relaxed">{mentor.description}</p>
        
        <div className="flex flex-wrap gap-1 justify-center mb-4">
          {mentor.badges.map((badge, index) => (
            <Badge key={index} variant={badge.variant}>
              {badge.text}
            </Badge>
          ))}
        </div>
        
        <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-md transition-colors">
          Book Now
        </button>
      </div>
    </div>
  );
};

export default MentorCard;  