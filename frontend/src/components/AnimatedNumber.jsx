import { useState, useEffect, useRef } from 'react';

/**
 * AnimatedNumber - Displays a value and briefly flashes green (up) or red (down)
 * when the value changes between polling cycles.
 *
 * Props:
 *   value      - The raw number or string to display
 *   formatted  - Optional: pre-formatted string to display (e.g. "0.452")
 *   className  - Optional extra CSS classes for the wrapper span
 */
export default function AnimatedNumber({ value, formatted, className = '' }) {
  const prevValueRef = useRef(null);
  const [flashClass, setFlashClass] = useState('');

  useEffect(() => {
    const prev = prevValueRef.current;
    const curr = parseFloat(value);

    if (prev !== null && !isNaN(curr) && !isNaN(prev)) {
      if (curr > prev) {
        setFlashClass('num-flash-up');
      } else if (curr < prev) {
        setFlashClass('num-flash-down');
      }

      // Remove the flash class after the animation finishes (700ms)
      const timer = setTimeout(() => setFlashClass(''), 700);
      return () => clearTimeout(timer);
    }

    prevValueRef.current = curr;
  }, [value]);

  // Also update the ref after each render
  useEffect(() => {
    prevValueRef.current = parseFloat(value);
  }, [value]);

  return (
    <>
      <style>{`
        @keyframes flashUp {
          0%   { color: inherit; text-shadow: none; }
          30%  { color: #10b981; text-shadow: 0 0 16px rgba(16, 185, 129, 0.7); }
          100% { color: inherit; text-shadow: none; }
        }
        @keyframes flashDown {
          0%   { color: inherit; text-shadow: none; }
          30%  { color: #ef4444; text-shadow: 0 0 16px rgba(239, 68, 68, 0.7); }
          100% { color: inherit; text-shadow: none; }
        }
        .num-flash-up   { animation: flashUp   0.7s ease-out; }
        .num-flash-down { animation: flashDown 0.7s ease-out; }
      `}</style>
      <span className={`${flashClass} ${className}`} style={{ transition: 'color 0.3s' }}>
        {formatted !== undefined ? formatted : value}
      </span>
    </>
  );
}
