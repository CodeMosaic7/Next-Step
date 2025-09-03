const CareerGoalTracker = () => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-6">Career Goal Tracker</h2>
      
      <div className="space-y-4">
        <h3 className="text-lg font-medium text-gray-900">Become a Data Scientist</h3>
        
        <div className="w-full bg-gray-200 rounded-full h-2">
          <div className="bg-blue-600 h-2 rounded-full" style={{ width: '75%' }}></div>
        </div>
        
        <div className="space-y-2 text-sm">
          <div className="flex justify-between">
            <span className="text-gray-600">Current Stage:</span>
            <span className="font-medium">Learning Data Visualization</span>
          </div>
          
          <div className="space-y-1">
            <div className="font-medium text-gray-900">Next Steps:</div>
            <div className="text-gray-600">Complete Advanced SQL course</div>
            <div className="text-gray-600">Build a portfolio with real projects</div>
            <div className="text-gray-600">Apply to data science internships</div>
            <div className="text-gray-600">Prepare for interviews</div>
          </div>
        </div>
        
        <button className="bg-blue-600 hover:bg-blue-700 text-white text-sm font-medium px-4 py-2 rounded-md transition-colors">
          Update Goal
        </button>
      </div>
    </div>
  );
};