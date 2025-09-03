const ListItem = ({ title, description, showChevron = false }) => {
  return (
    <div className="flex items-center justify-between py-3 border-b border-gray-100 last:border-b-0">
      <div>
        <h4 className="text-sm font-medium text-gray-900">{title}</h4>
        <p className="text-xs text-gray-600 mt-1">{description}</p>
      </div>
      {showChevron && (
        <ChevronRight className="w-4 h-4 text-gray-400" />
      )}
    </div>
  );
};

export default ListItem;