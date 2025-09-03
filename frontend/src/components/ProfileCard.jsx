const ProfileCard = () => {
  return (
    <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <h2 className="text-lg font-semibold text-gray-900 mb-6">My Profile</h2>
      
      <div className="flex flex-col items-center text-center">
        <div className="w-20 h-20 rounded-full overflow-hidden mb-4">
          <img 
            src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80" 
            alt="Alex Johnson" 
            className="w-full h-full object-cover"
          />
        </div>
        
        <h3 className="text-xl font-semibold text-gray-900 mb-1">Alex Johnson</h3>
        <p className="text-sm text-gray-600 mb-6">Computer Science, Senior</p>
        
        <button className="flex items-center gap-2 text-blue-600 hover:text-blue-700 text-sm font-medium">
          <Edit3 className="w-4 h-4" />
          Edit Profile
        </button>
      </div>
    </div>
  );
};
export default ProfileCard;