import Dropdown from './Dropdown';
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
export default FilterBar;