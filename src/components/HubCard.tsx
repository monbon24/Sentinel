"use client";

interface HubCardProps {
    title: string;
    description: string;
    icon: string;
    href: string;
}

export function HubCard({ title, description, icon, href }: HubCardProps) {
    return (
        <a
            href={href}
            target="_blank"
            rel="noopener noreferrer"
            className="group card-base glass touch-target p-5 sm:p-6 flex items-center gap-4 cursor-pointer border border-white/30"
            aria-label={`Open ${title} in new tab`}
        >
            {/* Icon Container with special styling */}
            <div className="w-14 h-14 sm:w-16 sm:h-16 rounded-2xl bg-gradient-to-br from-[#FFB5C5] to-[#E6E0FF] flex items-center justify-center text-3xl sm:text-4xl shadow-md flex-shrink-0 transition-all duration-300 group-hover:scale-110 group-hover:shadow-lg group-active:scale-95">
                {icon}
            </div>

            {/* Text Content */}
            <div className="flex-1 min-w-0">
                <h2 className="text-lg sm:text-xl font-bold text-[#5D5A6D] group-hover:text-[#4A475A] transition-colors">
                    {title}
                </h2>
                <p className="text-sm sm:text-base text-[#8E8A9D] flex items-center gap-2">
                    <span className="inline-block w-2 h-2 rounded-full bg-[#4ADE80] animate-pulse" />
                    {description}
                </p>
            </div>

            {/* External Link Indicator */}
            <div className="w-10 h-10 rounded-full bg-gradient-to-br from-[#FFB5C5]/30 to-[#E6E0FF]/30 flex items-center justify-center text-[#5D5A6D] flex-shrink-0 transition-all duration-300 group-hover:from-[#FFB5C5]/50 group-hover:to-[#E6E0FF]/50 group-hover:scale-110">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="18"
                    height="18"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden="true"
                >
                    <path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6" />
                    <polyline points="15 3 21 3 21 9" />
                    <line x1="10" y1="14" x2="21" y2="3" />
                </svg>
            </div>
        </a>
    );
}
