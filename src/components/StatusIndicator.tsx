"use client";

import { cn } from "@/lib/utils";

interface StatusIndicatorProps {
    status: "online" | "offline";
    text?: string;
}

export function StatusIndicator({ status, text }: StatusIndicatorProps) {
    return (
        <div className="flex items-center gap-2 px-4 py-2 rounded-full bg-white/60 backdrop-blur-sm shadow-sm">
            <span
                className={cn(
                    "status-dot",
                    status === "online" ? "status-online" : "status-offline"
                )}
                aria-hidden="true"
            />
            <span className="text-sm font-semibold text-[#5D5A6D]">
                {text || (status === "online" ? "Online" : "Offline")}
            </span>
        </div>
    );
}
