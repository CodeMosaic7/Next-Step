const Badge = ({ children, variant = 'default' }) => {
  const baseClasses = 'inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium';
  const variants = {
    default: 'bg-gray-100 text-gray-800',
    success: 'bg-green-100 text-green-800',
    blue: 'bg-blue-100 text-blue-800'
  };
  
  return (
    <span className={`${baseClasses} ${variants[variant]}`}>
      {children}
    </span>
  );
};

export default Badge;