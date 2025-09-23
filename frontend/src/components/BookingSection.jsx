import {useState} from 'react';
import { Calendar, Clock, MessageSquare, Video } from 'lucide-react';
import MiniCalendar from './MiniCalendar';
import TimeSlot from './TimeSlot';
const BookingSection = () => {
  const [selectedDate, setSelectedDate] = useState(15);
  const [selectedTime, setSelectedTime] = useState('09:00 AM');
  
  const timeSlots = [
    '09:00 AM',
    '11:00 AM',
    '01:00 PM',
    '03:00 PM'
  ];
  
  return (
    <div className="bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <h2 className="text-2xl font-bold text-gray-900 mb-8">Schedule Your Session</h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Book a Mentorship Session</h3>
            <p className="text-sm text-gray-600 mb-6">
              Select your preferred date and time to schedule a call at your convenient for the free
            </p>
            
            <MiniCalendar 
              selectedDate={selectedDate}
              onDateSelect={setSelectedDate}
            />
          </div>
          
          <div>
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Available Time Slots</h3>
            <div className="space-y-3">
              {timeSlots.map((time) => (
                <TimeSlot
                  key={time}
                  time={time}
                  isSelected={selectedTime === time}
                  onSelect={() => setSelectedTime(time)}
                />
              ))}
            </div>
          </div>
          
          <div className="bg-white rounded-lg p-6 shadow-sm border">
            <div className="flex items-center mb-4">
              <MessageSquare className="w-5 h-5 text-blue-600 mr-2" />
              <span className="font-medium text-gray-900">Next Step AI</span>
            </div>
            
            <div className="text-sm text-gray-600 mb-4">
              I would love to connect with you!
              Feel free to book a session at your convenience. Looking forward to our conversation!
            </div>
            
            <div className="space-y-3">
              <div className="flex items-center text-sm">
                <Calendar className="w-4 h-4 text-gray-500 mr-2" />
                <span>November {selectedDate}, 2024</span>
              </div>
              <div className="flex items-center text-sm">
                <Clock className="w-4 h-4 text-gray-500 mr-2" />
                <span>{selectedTime} (30 min)</span>
              </div>
              <div className="flex items-center text-sm">
                <Video className="w-4 h-4 text-gray-500 mr-2" />
                <span>Video Call</span>
              </div>
            </div>
            
            <button className="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-3 px-4 rounded-md mt-6 transition-colors">
              Confirm Booking
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default BookingSection;