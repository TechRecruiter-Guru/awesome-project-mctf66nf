import React, { useState } from 'react';

function CustomSchedulingPanel({ visible, onScheduleChange }) {
  const [schedule, setSchedule] = useState({
    frequency: 'daily',
    time: '09:00',
    timezone: 'UTC',
    daysOfWeek: [],
  });

  const frequencies = ['daily', 'weekly', 'monthly', 'custom'];
  const daysOfWeek = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
  const timezones = [
    'UTC',
    'America/New_York',
    'America/Chicago',
    'America/Los_Angeles',
    'Europe/London',
    'Europe/Paris',
    'Asia/Tokyo',
    'Asia/Shanghai',
  ];

  const handleChange = (field, value) => {
    const newSchedule = { ...schedule, [field]: value };
    setSchedule(newSchedule);
    onScheduleChange(newSchedule);
  };

  const toggleDay = (day) => {
    const newDays = schedule.daysOfWeek.includes(day)
      ? schedule.daysOfWeek.filter(d => d !== day)
      : [...schedule.daysOfWeek, day];
    handleChange('daysOfWeek', newDays);
  };

  if (!visible) return null;

  return (
    <div className="bg-light-gray rounded-2xl shadow-md p-6 transition-all duration-300">
      <h3 className="text-xl font-semibold mb-4 text-gray-800">Custom Scheduling</h3>

      <div className="space-y-4">
        {/* Frequency */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Frequency
          </label>
          <select
            value={schedule.frequency}
            onChange={(e) => handleChange('frequency', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          >
            {frequencies.map(freq => (
              <option key={freq} value={freq}>
                {freq.charAt(0).toUpperCase() + freq.slice(1)}
              </option>
            ))}
          </select>
        </div>

        {/* Days of Week (for weekly/custom) */}
        {(schedule.frequency === 'weekly' || schedule.frequency === 'custom') && (
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Days of Week
            </label>
            <div className="flex flex-wrap gap-2">
              {daysOfWeek.map(day => (
                <button
                  key={day}
                  onClick={() => toggleDay(day)}
                  className={`px-4 py-2 rounded-lg font-medium transition-colors ${
                    schedule.daysOfWeek.includes(day)
                      ? 'bg-primary text-white'
                      : 'bg-white text-gray-700 hover:bg-gray-100'
                  }`}
                >
                  {day}
                </button>
              ))}
            </div>
          </div>
        )}

        {/* Time */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Time
          </label>
          <input
            type="time"
            value={schedule.time}
            onChange={(e) => handleChange('time', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          />
        </div>

        {/* Timezone */}
        <div>
          <label className="block text-sm font-medium text-gray-700 mb-2">
            Timezone
          </label>
          <select
            value={schedule.timezone}
            onChange={(e) => handleChange('timezone', e.target.value)}
            className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
          >
            {timezones.map(tz => (
              <option key={tz} value={tz}>
                {tz}
              </option>
            ))}
          </select>
        </div>

        {/* Summary */}
        <div className="mt-4 p-4 bg-white rounded-lg border border-gray-200">
          <h4 className="text-sm font-semibold text-gray-700 mb-2">Schedule Summary</h4>
          <p className="text-sm text-gray-600">
            Runs <strong>{schedule.frequency}</strong>
            {schedule.frequency === 'weekly' && schedule.daysOfWeek.length > 0 && (
              <> on <strong>{schedule.daysOfWeek.join(', ')}</strong></>
            )}
            {' '}at <strong>{schedule.time}</strong> ({schedule.timezone})
          </p>
        </div>
      </div>
    </div>
  );
}

export default CustomSchedulingPanel;
