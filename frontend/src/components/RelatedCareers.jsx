const RelatedCareers = () => (
  <div className="bg-gray-50 py-12">
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <h2 className="text-2xl font-bold text-gray-900 mb-8 text-center">Explore Related Careers</h2>
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {[
          "Machine Learning Engineer",
          "Data Analyst", 
          "Business Intelligence Analyst",
          "Research Scientist"
        ].map((career, index) => (
          <div key={index} className="bg-white rounded-lg border border-gray-200 p-6 text-center hover:shadow-md transition-shadow cursor-pointer">
            <h3 className="font-semibold text-gray-900 mb-2">{career}</h3>
            <p className="text-sm text-gray-600">Explore this career path</p>
          </div>
        ))}
      </div>
    </div>
  </div>
);