/**
 * SatisfactionFeedback component with thumbs up/down buttons,
 * optional feedback text box, and submit functionality
 */

"use client";

import { useMemo, useState, useEffect, useRef } from 'react';
import { useChatContext } from '@/context/ChatContext';
import { feedbackApi } from '@/services/api-client';
import { cn } from '@/utils/cn';
import { CLAUDE_HAIKU_PRICING, computeCost } from '@/constants/pricing';
import { HelpCircle } from 'lucide-react';

interface SatisfactionFeedbackProps {
  onSubmitted?: () => void;
}

export default function SatisfactionFeedback({ onSubmitted }: SatisfactionFeedbackProps) {
  const { sessionId, messages, tokenUsage } = useChatContext();
  const [rating, setRating] = useState<'thumbs_up' | 'thumbs_down' | null>(null);
  const [comment, setComment] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [showTokenTooltip, setShowTokenTooltip] = useState(false);
  const [showCostTooltip, setShowCostTooltip] = useState(false);
  const prevSessionIdRef = useRef<string | null>(null);
  const tooltipTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const costTooltipTimeoutRef = useRef<NodeJS.Timeout | null>(null);

  const hasUserInput = useMemo(
    () => messages.some((msg) => msg.role === 'user' && msg.content && msg.content.trim().length > 0),
    [messages]
  );
  const buttonsDisabled = !hasUserInput || isSubmitting;

  // Reset feedback state when session changes (New Chat clicked)
  useEffect(() => {
    if (prevSessionIdRef.current !== null && prevSessionIdRef.current !== sessionId) {
      // Session changed - reset feedback
      setRating(null);
      setComment('');
      setIsSubmitting(false);
    }
    prevSessionIdRef.current = sessionId;
  }, [sessionId]);

  // Reset feedback state when messages are cleared (New Chat clicked)
  useEffect(() => {
    if (messages.length === 0) {
      // Messages cleared - reset feedback
      setRating(null);
      setComment('');
      setIsSubmitting(false);
    }
  }, [messages.length]);

  // Cleanup tooltip timeouts on unmount
  useEffect(() => {
    return () => {
      if (tooltipTimeoutRef.current) {
        clearTimeout(tooltipTimeoutRef.current);
      }
      if (costTooltipTimeoutRef.current) {
        clearTimeout(costTooltipTimeoutRef.current);
      }
    };
  }, []);

  const totalTokens = tokenUsage.inputTokens + tokenUsage.outputTokens;
  const inputCost = computeCost(tokenUsage.inputTokens, CLAUDE_HAIKU_PRICING.INPUT_PER_1K);
  const outputCost = computeCost(tokenUsage.outputTokens, CLAUDE_HAIKU_PRICING.OUTPUT_PER_1K);
  const totalCost = inputCost + outputCost;

  const formatTokens = (value: number) => value.toLocaleString();
  const formatCost = (value: number) =>
    value.toLocaleString(undefined, { minimumFractionDigits: 6, maximumFractionDigits: 6 });

  const handleSubmit = async () => {
    if (!rating || !sessionId) return;

    setIsSubmitting(true);
    try {
      await feedbackApi.submitFeedback(sessionId, rating, comment || undefined);
      // Reset feedback state after successful submission
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
      <div className="w-full max-w-[90%] mx-auto py-4" style={{ paddingLeft: '144px', paddingRight: '16px' }}>
        <div className="flex flex-col items-end gap-3 w-full">
          <div className="flex w-full items-center gap-3 flex-wrap">
            <p className="text-sm font-semibold text-gray-700 whitespace-nowrap">Was this response helpful?</p>
            <div className="flex items-center gap-2">
              <button
                onClick={() => setRating('thumbs_up')}
                className={cn(
                  'p-2 rounded-lg border-2 transition-colors',
                  !buttonsDisabled && 'hover:bg-primary-dark hover:border-primary-dark',
                  rating === 'thumbs_up'
                    ? 'bg-primary border-primary text-white'
                    : 'bg-white border-gray-300',
                  buttonsDisabled && 'opacity-60 cursor-not-allowed'
                )}
                aria-label="Thumbs up - helpful"
                disabled={buttonsDisabled}
              >
                <span className="text-2xl">👍</span>
              </button>
              <button
                onClick={() => setRating('thumbs_down')}
                className={cn(
                  'p-2 rounded-lg border-2 transition-colors',
                  !buttonsDisabled && 'hover:bg-primary-dark hover:border-primary-dark',
                  rating === 'thumbs_down'
                    ? 'bg-primary border-primary text-white'
                    : 'bg-white border-gray-300',
                  buttonsDisabled && 'opacity-60 cursor-not-allowed'
                )}
                aria-label="Thumbs down - not helpful"
                disabled={buttonsDisabled}
              >
                <span className="text-2xl">👎</span>
              </button>
            </div>
            {rating && (
              <>
                <input
                  type="text"
                  value={comment}
                  onChange={(e) => setComment(e.target.value)}
                  placeholder="Optional: Add your feedback..."
                  className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-primary flex-1 min-w-[200px]"
                  disabled={isSubmitting}
                />
                <button
                  onClick={handleSubmit}
                  disabled={isSubmitting}
                  className={cn(
                    'px-4 py-2 rounded-lg font-semibold transition-colors whitespace-nowrap',
                    'bg-primary text-white hover:bg-primary-dark',
                    'disabled:bg-gray-300 disabled:cursor-not-allowed'
                  )}
                >
                  {isSubmitting ? 'Submitting...' : 'Submit'}
                </button>
              </>
            )}
          </div>
          <div className="flex justify-end w-full pb-1" style={{ paddingRight: '0px' }}>
            <div className="text-xs font-semibold text-slate-800 leading-tight flex flex-col items-end gap-1">
              <div className="flex items-baseline gap-2 relative">
                <span className="inline-block text-right" style={{ width: '215px' }}>Token count for this chat:</span>
                <span className="whitespace-nowrap">{formatTokens(totalTokens)}</span>
                <span className="text-slate-500 font-normal whitespace-nowrap">
                  (<span className="font-bold">in:</span> {formatTokens(tokenUsage.inputTokens)}, <span className="font-bold">out:</span> {formatTokens(tokenUsage.outputTokens)})
                </span>
                <div className="relative inline-block ml-1">
                  <button
                    type="button"
                    className="inline-flex items-center justify-center text-slate-500 hover:text-slate-700 transition-colors cursor-help"
                    onMouseEnter={() => {
                      if (tooltipTimeoutRef.current) {
                        clearTimeout(tooltipTimeoutRef.current);
                      }
                      setShowTokenTooltip(true);
                    }}
                    onMouseLeave={() => {
                      if (tooltipTimeoutRef.current) {
                        clearTimeout(tooltipTimeoutRef.current);
                      }
                      tooltipTimeoutRef.current = setTimeout(() => {
                        setShowTokenTooltip(false);
                      }, 150);
                    }}
                    aria-label="Token count information"
                  >
                    <HelpCircle size={14} />
                  </button>
                  {showTokenTooltip && (
                    <div
                      className="absolute bottom-full right-0 mb-2 w-48 p-2.5 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-50"
                      style={{ 
                        transform: 'translateX(calc(100% - 20px))',
                        willChange: 'opacity',
                        pointerEvents: 'auto'
                      }}
                      onMouseEnter={() => {
                        if (tooltipTimeoutRef.current) {
                          clearTimeout(tooltipTimeoutRef.current);
                          tooltipTimeoutRef.current = null;
                        }
                        setShowTokenTooltip(true);
                      }}
                      onMouseLeave={() => {
                        if (tooltipTimeoutRef.current) {
                          clearTimeout(tooltipTimeoutRef.current);
                        }
                        tooltipTimeoutRef.current = setTimeout(() => {
                          setShowTokenTooltip(false);
                        }, 150);
                      }}
                    >
                      <div className="space-y-2 text-[11px]">
                        <div>
                          <div className="text-slate-300">
                            Input token count <span className="font-semibold text-white">{formatTokens(tokenUsage.inputTokens)}</span> includes:
                          </div>
                          <div className="text-slate-300 mt-1 ml-2 space-y-0.5">
                            <div>- System Prompt,</div>
                            <div>- Input User query,</div>
                            <div>- all previous chat history messages (user/assistant/tool)</div>
                          </div>
                        </div>
                        <div className="pt-2 border-t border-slate-600">
                          <div className="text-slate-300">
                            Output token count <span className="font-semibold text-white">{formatTokens(tokenUsage.outputTokens)}</span> includes:
                          </div>
                          <div className="text-slate-300 mt-1 ml-2">
                            Tokens in the AI's responses generated for you
                          </div>
                        </div>
                      </div>
                      <div className="absolute bottom-0 right-4 transform translate-y-full">
                        <div className="w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-800"></div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
              <div className="flex items-baseline gap-2 relative" style={{ paddingLeft: '130px' }}>
                <span className="inline-block text-right" style={{ width: '215px' }}>Total cost for this chat:</span>
                <span className="whitespace-nowrap">${formatCost(totalCost)}</span>
                <span className="text-slate-500 font-normal whitespace-nowrap">
                  (<span className="font-bold">in:</span> ${formatCost(inputCost)}, <span className="font-bold">out:</span> ${formatCost(outputCost)})
                </span>
                <div className="relative inline-block ml-1">
                  <button
                    type="button"
                    className="inline-flex items-center justify-center text-slate-500 hover:text-slate-700 transition-colors cursor-help"
                    onMouseEnter={() => {
                      if (costTooltipTimeoutRef.current) {
                        clearTimeout(costTooltipTimeoutRef.current);
                      }
                      setShowCostTooltip(true);
                    }}
                    onMouseLeave={() => {
                      if (costTooltipTimeoutRef.current) {
                        clearTimeout(costTooltipTimeoutRef.current);
                      }
                      costTooltipTimeoutRef.current = setTimeout(() => {
                        setShowCostTooltip(false);
                      }, 150);
                    }}
                    aria-label="Total cost information"
                  >
                    <HelpCircle size={14} />
                  </button>
                  {showCostTooltip && (
                    <div
                      className="absolute bottom-full right-0 mb-2 w-48 p-2.5 bg-slate-800 text-white text-xs rounded-lg shadow-lg z-50"
                      style={{ 
                        transform: 'translateX(calc(100% - 20px))',
                        willChange: 'opacity',
                        pointerEvents: 'auto'
                      }}
                      onMouseEnter={() => {
                        if (costTooltipTimeoutRef.current) {
                          clearTimeout(costTooltipTimeoutRef.current);
                          costTooltipTimeoutRef.current = null;
                        }
                        setShowCostTooltip(true);
                      }}
                      onMouseLeave={() => {
                        if (costTooltipTimeoutRef.current) {
                          clearTimeout(costTooltipTimeoutRef.current);
                        }
                        costTooltipTimeoutRef.current = setTimeout(() => {
                          setShowCostTooltip(false);
                        }, 150);
                      }}
                    >
                      <div className="space-y-2">
                        <div className="font-semibold mb-1">Costs estimation details:</div>
                        <div className="text-slate-300 text-[11px]">
                          Pricing rates based on:
                        </div>
                        <div className="text-slate-300 text-[11px] font-semibold text-white mb-2">
                          Claude 3 Haiku (AWS Bedrock)
                        </div>
                        <div className="pt-2 border-t border-slate-600">
                          <div className="font-semibold mb-1 text-[11px]">Unit Prices:</div>
                          <div className="space-y-1 text-[11px]">
                            <div className="text-slate-300">
                              <span className="font-semibold text-white">Input:</span> ${CLAUDE_HAIKU_PRICING.INPUT_PER_1K.toFixed(5)} per 1K
                            </div>
                            <div className="text-slate-300">
                              <span className="font-semibold text-white">Output:</span> ${CLAUDE_HAIKU_PRICING.OUTPUT_PER_1K.toFixed(5)} per 1K
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="absolute bottom-0 right-4 transform translate-y-full">
                        <div className="w-0 h-0 border-l-4 border-r-4 border-t-4 border-transparent border-t-slate-800"></div>
                      </div>
                    </div>
                  )}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

