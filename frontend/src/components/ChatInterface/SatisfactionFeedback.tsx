/**
 * SatisfactionFeedback component with thumbs up/down buttons,
 * optional feedback text box, and submit functionality
 */

'use client';

import { useState } from 'react';
import { useChatContext } from '@/context/ChatContext';
import { feedbackApi } from '@/services/api-client';
import { cn } from '@/utils/cn';

interface SatisfactionFeedbackProps {
  onSubmitted?: () => void;
}

export default function SatisfactionFeedback({ onSubmitted }: SatisfactionFeedbackProps) {
  const { sessionId, messages } = useChatContext();
  const [rating, setRating] = useState<'thumbs_up' | 'thumbs_down' | null>(null);
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [isSubmitted, setIsSubmitted] = useState(false);

  // Only show feedback if conversation has ended (has messages and not streaming)
  const lastMessage = messages[messages.length - 1];
  const shouldShow = lastMessage && lastMessage.role === 'assistant' && sessionId;

  if (!shouldShow || isSubmitted) {
    return null;
  }

  const handleSubmit = async () => {
    if (!rating || !sessionId) return;

    setIsSubmitting(true);
    try {
      await feedbackApi.submitFeedback(sessionId, rating, comment || undefined);
      setIsSubmitted(true);
      setRating(null);
      setComment('');
      onSubmitted?.();
    } catch (error) {
      console.error('Error submitting feedback:', error);
      alert('Failed to submit feedback. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div className="border-t border-white/40 bg-white/80 backdrop-blur-lg">
      <div className="w-full max-w-[90%] mx-auto px-4 py-4">
        <p className="text-sm font-semibold text-gray-700 mb-3">
          Was this response helpful?
        </p>
        <div className="flex items-center gap-4">
          {/* Thumbs Up/Down Buttons */}
          <div className="flex gap-2">
            <button
              onClick={() => setRating('thumbs_up')}
              className={cn(
                'p-2 rounded-lg border-2 transition-colors',
                'hover:bg-green-50 hover:border-green-400',
                rating === 'thumbs_up'
                  ? 'bg-green-100 border-green-500'
                  : 'bg-white border-gray-300'
              )}
              aria-label="Thumbs up - helpful"
              disabled={isSubmitting}
            >
              <span className="text-2xl">👍</span>
            </button>
            <button
              onClick={() => setRating('thumbs_down')}
              className={cn(
                'p-2 rounded-lg border-2 transition-colors',
                'hover:bg-red-50 hover:border-red-400',
                rating === 'thumbs_down'
                  ? 'bg-red-100 border-red-500'
                  : 'bg-white border-gray-300'
              )}
              aria-label="Thumbs down - not helpful"
              disabled={isSubmitting}
            >
              <span className="text-2xl">👎</span>
            </button>
          </div>

          {/* Optional Comment Box */}
          {rating && (
            <div className="flex-1 flex gap-2">
              <input
                type="text"
                value={comment}
                onChange={(e) => setComment(e.target.value)}
                placeholder="Optional: Add your feedback..."
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary"
                disabled={isSubmitting}
              />
              <button
                onClick={handleSubmit}
                disabled={isSubmitting}
                className={cn(
                  'px-4 py-2 rounded-lg font-semibold transition-colors',
                  'bg-primary text-white hover:bg-primary-dark',
                  'disabled:bg-gray-300 disabled:cursor-not-allowed'
                )}
              >
                {isSubmitting ? 'Submitting...' : 'Submit'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

