/**
 * Utility function for combining class names (cn utility)
 * Used with TailwindCSS and shadcn/ui
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

