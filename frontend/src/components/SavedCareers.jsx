const SavedCareers = () => {
  const careers = [
    {
      title: "Software Engineer",
      description: "Development experience in software applications."
    },
    {
      title: "UI/UX Designer", 
      description: "Create user-friendly and aesthetically pleasing front."
    },
    {
      title: "Product Manager",
      description: "Define product vision and coordinate development teams."
    }
  ];

  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-lg font-semibold text-gray-900">Saved Careers</h2>
      </div>
      
      <div className="space-y-0">
        {careers.map((career, index) => (
          <ListItem 
            key={index}
            title={career.title}
            description={career.description}
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
