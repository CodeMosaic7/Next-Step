import TestimonialCard from "./TestimonialCard";
const TestimonialsSection = () => {
  const testimonials = [
    {
      name: "Sarah J.",
      role: "University Student",
      content: "Next Step helped me discover a career path I never knew existed. The personalized recommendations were spot-on and incredibly helpful!",
      avatar: "SJ"
    },
    {
      name: "Dr. Alex Chen",
      role: "Software Engineer & Mentor",
      content: "As a mentor, I've seen countless students benefit from Next Step's structured guidance. It's a game-changer for career exploration.",
      avatar: "AC"
    },
    {
      name: "Michael R.",
      role: "Young Professional",
      content: "The resources library is fantastic! I found so many useful courses and articles that directly relate to my chosen career field.",
      avatar: "MR"
    }
  ];

  return (
    <section className="py-16 bg-gradient-to-b from-white to-gray-100">
  <div className="max-w-7xl mx-auto px-4">
    <h2 className="text-3xl font-bold text-center text-gray-900 mb-12">
      Hear From Our Community
    </h2>
    
    <div className="grid grid-cols-1 md:grid-cols-3 gap-6 shadow-lg">
      {testimonials.map((testimonial, index) => (
        <TestimonialCard key={index} {...testimonial} />
      ))}
    </div>
  </div>
</section>
  );
};

export default TestimonialsSection;