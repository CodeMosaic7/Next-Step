const CompletedAssessments = () => {
  const assessments = [
    {
      title: "Career Personality Match",
      description: "Jan 15, 2024 • Score: 94/100"
    },
    {
      title: "Logical Reasoning Test",
      description: "Dec 22, 2023 • Score: 89/100"
    },
    {
      title: "Technical Skills Assessment",
      description: "Dec 05, 2023 • Score: 92/100"
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Completed Assessments</h2>
      </div>
      
      <div className="space-y-0">
        {assessments.map((assessment, index) => (
          <ListItem 
            key={index}
            title={assessment.title}
            description={assessment.description}
            showChevron={true}
          />
        ))}
      </div>
      
      <button className="text-blue-600 hover:text-blue-700 text-sm font-medium mt-4">
        View All
      </button>
    </div>
  );
};