
const HeroSection = () => {
  return (
    <section className="relative bg-gradient-to-br from-blue-50 to-white pt-40 pb-40 overflow-hidden ">
      {/* Background decorative elements */}
      <div className="absolute top-10 left-10 w-32 h-32 bg-blue-500 rounded-full opacity-20 blur-xl"></div>
      <div className="absolute top-20 right-20 w-20 h-20 bg-blue-600 rounded-full opacity-30"></div>
      <div className="absolute bottom-10 right-10 w-40 h-40 bg-blue-400 rounded-full opacity-15 blur-2xl"></div>
      
      <div className="relative max-w-4xl mx-auto text-center px-4">
        <h1 className="text-5xl md:text-6xl font-bold text-gray-900 mb-8">
          Find Your Perfect Career Path
          <br />
          <span className="text-gray-800">with Next Step</span>
          <span className="text-4xl ml-2">🚀</span>
        </h1>
        
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button className="bg-blue-600 hover:bg-blue-700 text-white px-8 py-3 rounded-full font-semibold transition-colors">
            Start Assessment
          </button>
          <button className="border-2 border-blue-600 text-blue-600 hover:bg-blue-50 px-8 py-3 rounded-full font-semibold transition-colors">
            Explore Careers
          </button>
        </div>
      </div>
    </section>
  );
};
export default HeroSection;