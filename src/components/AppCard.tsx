"use client";

import { cn } from "@/lib/utils";
import Link from "next/link";

type AccentColor = "pink" | "lavender" | "mint" | "peach";

interface AppCardProps {
    title: string;
    description: string;
    icon: string;
    href: string;
    accentColor?: AccentColor;
    external?: boolean;
}

const accentClasses: Record<AccentColor, string> = {
    pink: "accent-pink",
    lavender: "accent-lavender",
    mint: "accent-mint",
    peach: "accent-peach",
};

export function AppCard({
    title,
    description,
    icon,
    href,
    accentColor = "pink",
    external = false,
}: AppCardProps) {
    const CardContent = (
        <>
            {/* Icon Container */}
            <div className="w-12 h-12 sm:w-14 sm:h-14 rounded-2xl bg-white/80 flex items-center justify-center text-2xl sm:text-3xl shadow-sm flex-shrink-0 transition-transform duration-300 group-hover:scale-110 group-active:scale-95">
                {icon}
            </div>

            {/* Text Content */}
            <div className="flex-1 min-w-0">
                <h2 className="text-base sm:text-lg font-bold text-[#5D5A6D] truncate group-hover:text-[#4A475A] transition-colors">
                    {title}
                </h2>
                <p className="text-sm text-[#8E8A9D] truncate">
                    {description}
                </p>
            </div>

            {/* Arrow Indicator */}
            <div className="w-8 h-8 rounded-full bg-white/60 flex items-center justify-center text-[#8E8A9D] flex-shrink-0 transition-all duration-300 group-hover:bg-white group-hover:text-[#5D5A6D] group-hover:translate-x-1">
                <svg
                    xmlns="http://www.w3.org/2000/svg"
                    width="16"
                    height="16"
                    viewBox="0 0 24 24"
                    fill="none"
                    stroke="currentColor"
                    strokeWidth="2"
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    aria-hidden="true"
                >
                    <path d="M5 12h14" />
                    <path d="m12 5 7 7-7 7" />
                </svg>
            </div>
        </>
    );

    const cardClassName = cn(
        "group card-base touch-target p-4 sm:p-5 flex items-center gap-4 cursor-pointer",
        accentClasses[accentColor]
    );

    if (external) {
        return (
            <a
                href={href}
                target="_blank"
                rel="noopener noreferrer"
                className={cardClassName}
                aria-label={`Open ${title} in new tab`}
            >
                {CardContent}
            </a>
        );
    }

    return (
        <Link href={href} className={cardClassName} aria-label={`Navigate to ${title}`}>
            {CardContent}
        </Link>
    );
}
