/**
 * TodayDate component displays today's date in the sidebar
 */

'use client';

export default function TodayDate() {
  const today = new Date();
  const weekday = today
    .toLocaleDateString('en-US', { weekday: 'short' })
    .slice(0, 3);
  const month = today
    .toLocaleDateString('en-US', { month: 'short' })
    .slice(0, 3);
  const day = today
    .toLocaleDateString('en-US', { day: '2-digit' });
  const year = today.getFullYear();
  const formattedDate = `${weekday}, ${month} ${day} ${year}`;

  return (
    <div className="text-center px-3 py-4">
      <p className="text-xs font-bold text-black mb-1">Today:</p>
      <p className="text-sm font-bold text-black leading-tight">
        {formattedDate}
      </p>
    </div>
  );
}

