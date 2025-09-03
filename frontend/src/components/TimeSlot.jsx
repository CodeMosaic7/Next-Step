const TimeSlot = ({ time, isSelected, onSelect }) => {
  return (
    <button
      onClick={onSelect}
      className={`block w-full text-left p-3 rounded-md border text-sm transition-colors ${
        isSelected
          ? 'border-blue-600 bg-blue-50 text-blue-600'
          : 'border-gray-200 hover:border-gray-300'
      }`}
    >
      {time}
    </button>
  );
};
export default TimeSlot;