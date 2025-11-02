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
        : 'bg-white/70 text-gray-700 hover:bg-white border-white/60'
    }`;

  return (
    <header className="bg-white/80 backdrop-blur-lg border-b border-white/50 shadow-lg">
      <div className="container mx-auto px-4 py-4 flex items-center justify-between gap-3">
        <div className="flex items-center gap-3">
          {/* Airplane Logo */}
          <div className="flex-shrink-0">
            <Image
              src="/airplane.svg"
              alt="Airplane icon"
              width={44}
              height={44}
              priority
              className="w-11 h-11"
            />
          </div>
          
          {/* Title */}
          <h1 className="text-2xl font-bold text-gray-900 drop-shadow-sm">
            The Aerospace Company Customer Service Agent
          </h1>
        </div>

        <nav className="flex items-center gap-3">
          <Link href="/" className={navLinkClasses(pathname === '/')}>Chat</Link>
          <Link href="/upload" className={navLinkClasses(pathname?.startsWith('/upload') ?? false)}>
            Upload Documents
          </Link>
        </nav>
      </div>
    </header>
  );
}

