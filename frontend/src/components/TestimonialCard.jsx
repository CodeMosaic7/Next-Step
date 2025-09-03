const TestimonialCard = ({ name, role, content, avatar }) => {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100">
      <p className="text-gray-700 mb-4 italic">"{content}"</p>
      <div className="flex items-center">
        <div className="w-10 h-10 bg-gray-300 rounded-full flex items-center justify-center mr-3">
          <span className="text-sm font-semibold text-gray-600">{avatar}</span>
        </div>
        <div>
          <p className="font-semibold text-gray-900">{name}</p>
          <p className="text-sm text-gray-600">{role}</p>
        </div>
      </div>
    </div>
  );
};
export default TestimonialCard;