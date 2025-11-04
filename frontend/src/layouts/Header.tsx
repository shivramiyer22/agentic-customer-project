'use client';

/**
 * Header component with title "The Aerospace Company Customer Service Agent"
 * and airplane logo icon prominently displayed
 */

import Image from 'next/image';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function Header() {
  const pathname = usePathname();

  const navLinkClasses = (active: boolean) =>
    `px-4 py-2 rounded-lg font-semibold transition-colors border border-transparent shadow-sm ${
      active
        ? 'bg-primary text-white hover:bg-primary-dark'
        : 'bg-primary text-white hover:bg-primary-dark'
    }`;

  return (
    <header className="bg-white/80 backdrop-blur-lg border-b border-white/50 shadow-lg">
      <div className="container mx-auto px-4 py-4">
        {/* Centered Title and Logo */}
        <div className="flex items-center justify-center gap-6 mb-4">
          {/* Airplane Logo - Doubled Size */}
          <div className="flex-shrink-0">
            <Image
              src="/airplane.svg"
              alt="Airplane icon"
              width={88}
              height={88}
              priority
              className="w-22 h-22"
            />
          </div>
          
          {/* Title - Doubled Size */}
          <h1 className="text-4xl font-bold text-gray-900 drop-shadow-sm">
            The Aerospace Company Customer Service Agent
          </h1>
        </div>

        {/* Right-aligned Navigation - uniformly formatted */}
        <nav className="flex items-center justify-end gap-3">
          <Link href="/" className={navLinkClasses(pathname === '/')}>
            Chat
          </Link>
          <Link href="/upload" className={navLinkClasses(pathname?.startsWith('/upload') ?? false)}>
            Upload Documents
          </Link>
        </nav>
      </div>
    </header>
  );
}

