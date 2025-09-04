import { Clock, Users, Star } from "lucide-react";
import Badge from "../components/Badge";
const ResourceCard = ({ resource }) => {
  const getBadgeVariant = (type) => {
    const variants = {
      'Beginner': 'success',
      'Intermediate': 'yellow',
      'Advanced': 'red',
      'Free': 'success',
      'Premium': 'purple',
      'Popular': 'blue',
      'New': 'indigo'
    };
    return variants[type] || 'default';
  };

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 overflow-hidden hover:shadow-md transition-shadow">
      <div className="aspect-video bg-gradient-to-br from-blue-100 to-purple-100 relative overflow-hidden">
        {resource.image ? (
          <img src={resource.image} alt={resource.title} className="w-full h-full object-cover" />
        ) : (
          <div className="w-full h-full flex items-center justify-center">
            <div className="text-4xl">{resource.emoji}</div>
          </div>
        )}
      </div>
      
      <div className="p-4">
        <h3 className="font-semibold text-gray-900 mb-2 line-clamp-2">{resource.title}</h3>
        
        <div className="flex items-center gap-4 text-sm text-gray-500 mb-3">
          <div className="flex items-center gap-1">
            <Clock className="w-4 h-4" />
            <span>{resource.duration}</span>
          </div>
          <div className="flex items-center gap-1">
            <Users className="w-4 h-4" />
            <span>{resource.students}</span>
          </div>
          {resource.rating && (
            <div className="flex items-center gap-1">
              <Star className="w-4 h-4 fill-yellow-400 text-yellow-400" />
              <span>{resource.rating}</span>
            </div>
          )}
        </div>
        
        <div className="flex flex-wrap gap-1 mb-4">
          {resource.badges.map((badge, index) => (
            <Badge key={index} variant={getBadgeVariant(badge)}>
              {badge}
            </Badge>
          ))}
        </div>
        
        <div className="flex justify-between items-center">
          <button className="text-blue-600 hover:text-blue-700 text-sm font-medium">
            View Resource
          </button>
          <button className="text-gray-400 hover:text-gray-600 text-sm">
            View Resource
          </button>
        </div>
      </div>
    </div>
  );
};
export default ResourceCard;