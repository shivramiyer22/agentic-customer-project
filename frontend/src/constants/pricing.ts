/**
 * Pricing constants for model usage cost calculations.
 *
 * Claude 3 Haiku on AWS Bedrock (November 2025 published rates):
 * - Input tokens: $0.00025 per 1,000 tokens
 * - Output tokens: $0.00125 per 1,000 tokens
 */

export const CLAUDE_HAIKU_PRICING = {
  INPUT_PER_1K: 0.00025,
  OUTPUT_PER_1K: 0.00125,
} as const;

/**
 * Utility to compute dollar cost for a token count at a given per-1k rate.
 */
export const computeCost = (tokens: number, pricePerThousand: number): number => {
  if (!tokens || tokens <= 0) {
    return 0;
  }
  return (tokens / 1000) * pricePerThousand;
};




