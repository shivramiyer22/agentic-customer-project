import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "../styles/globals.css";
import TodayDate from "@/components/Sidebar/TodayDate";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "The Aerospace Company Customer Service Agent",
  description: "Multi-agent AI system for customer service representatives",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body
        className={`${geistSans.variable} ${geistMono.variable} antialiased`}
      >
        <div className="flex min-h-screen">
          {/* Left sidebar pane with golden/saffron color - doubled width */}
          <div className="w-32 bg-gradient-to-b from-amber-400 to-orange-400 flex-shrink-0 fixed left-0 top-0 bottom-0 z-50 flex flex-col items-center">
            {/* Today's Date - at the top */}
            <div className="pt-6">
              <TodayDate />
            </div>
            
            {/* User Training Guide Link - centered vertically in sidebar */}
            <div className="flex-1 flex items-center justify-center">
            <a
              href="/User-Training-Guide.pdf"
              target="_blank"
              rel="noopener noreferrer"
              className="flex flex-col items-center gap-2 px-3 py-4 rounded-lg bg-primary hover:bg-primary-dark transition-colors shadow-md hover:shadow-lg"
              title="User Training Guide"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                viewBox="0 0 24 24"
                fill="none"
                stroke="currentColor"
                strokeWidth="2"
                className="w-10 h-10 text-white"
              >
                <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
                <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
                <path d="M8 7h8" />
                <path d="M8 11h8" />
                <path d="M8 15h6" />
              </svg>
              <span className="text-xs font-bold text-white text-center leading-tight">
                User<br/>Guide
              </span>
            </a>
            </div>
          </div>
          
          {/* Main content area with left margin to account for fixed sidebar (doubled) */}
          <div className="flex-1 ml-32">
            {children}
          </div>
        </div>
      </body>
    </html>
  );
}
