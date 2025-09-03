import { useState } from 'react';
import { Heart, DollarSign, GraduationCap, TrendingUp} from 'lucide-react';
import Dropdown from './Dropdown';
const CareerCard = ({ career, onFavorite }) => {
  const [isFavorited, setIsFavorited] = useState(false);

  const handleFavorite = () => {
    setIsFavorited(!isFavorited);
    onFavorite?.(career.title, !isFavorited);
  };

  const getDemandColor = (level) => {
    switch (level.toLowerCase()) {
      case 'high': return 'bg-green-100 text-green-800';
      case 'medium': return 'bg-yellow-100 text-yellow-800';
      case 'low': return 'bg-red-100 text-red-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  return (
    <div className="bg-white rounded-lg border border-gray-200 p-6 hover:shadow-md transition-shadow">
      {/* Header with title and favorite button */}
      <div className="flex items-start justify-between mb-4">
        <h3 className="text-lg font-semibold text-gray-900">{career.title}</h3>
        <button
          onClick={handleFavorite}
          className={`p-1 rounded-full hover:bg-gray-100 transition-colors ${
            isFavorited ? 'text-red-500' : 'text-gray-400'
          }`}
        >
          <Heart className={`w-5 h-5 ${isFavorited ? 'fill-current' : ''}`} />
        </button>
      </div>

      {/* Description */}
      <p className="text-sm text-gray-600 mb-4 line-clamp-3">{career.description}</p>

      {/* Stats Grid */}
      <div className="space-y-3">
        {/* Salary */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <DollarSign className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">Salary</span>
          </div>
          <span className="text-sm font-medium text-gray-900">{career.salary}</span>
        </div>

        {/* Education */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <GraduationCap className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">Education</span>
          </div>
          <span className="text-sm font-medium text-gray-900">{career.education}</span>
        </div>

        {/* Demand */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <TrendingUp className="w-4 h-4 text-gray-500" />
            <span className="text-sm text-gray-600">Demand</span>
          </div>
          <span className={`text-xs px-2 py-1 rounded-full font-medium ${getDemandColor(career.demand)}`}>
            {career.demand}
          </span>
        </div>
      </div>
    </div>
  );
};

// Filter Bar Component
const FilterBar = ({ filters, onFilterChange }) => (
  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-8">
    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
      <Dropdown
        label="All Locations"
        value={filters.location}
        options={['All Locations', 'New York', 'San Francisco', 'Remote', 'Boston']}
        onChange={(value) => onFilterChange('location', value)}
      />
      <Dropdown
        label="Any Salary"
        value={filters.salary}
        options={['Any Salary', '$50K - $70K', '$70K - $100K', '$100K - $150K', '$150K+']}
        onChange={(value) => onFilterChange('salary', value)}
      />
      <Dropdown
        label="Any Demand"
        value={filters.demand}
        options={['Any Demand', 'High', 'Medium', 'Low']}
        onChange={(value) => onFilterChange('demand', value)}
      />
      <Dropdown
        label="Recommended"
        value={filters.recommendation}
        options={['Recommended', 'Best Match', 'High Salary', 'High Demand']}
        onChange={(value) => onFilterChange('recommendation', value)}
      />
    </div>
  </div>
);
export default CareerCard;