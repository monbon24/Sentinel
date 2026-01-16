"use client";

export function FloatingShapes() {
    return (
        <div className="fixed inset-0 overflow-hidden pointer-events-none z-0" aria-hidden="true">
            {/* Floating circles with staggered animations */}
            <div
                className="absolute w-32 h-32 sm:w-48 sm:h-48 rounded-full bg-gradient-to-br from-[#FFB5C5]/30 to-[#E6E0FF]/20 blur-2xl animate-float"
                style={{
                    top: "10%",
                    left: "5%",
                    animationDelay: "0s",
                    animationDuration: "8s",
                }}
            />
            <div
                className="absolute w-24 h-24 sm:w-36 sm:h-36 rounded-full bg-gradient-to-br from-[#B5E8D5]/30 to-[#E6E0FF]/20 blur-2xl animate-float"
                style={{
                    top: "60%",
                    right: "5%",
                    animationDelay: "2s",
                    animationDuration: "10s",
                }}
            />
            <div
                className="absolute w-20 h-20 sm:w-28 sm:h-28 rounded-full bg-gradient-to-br from-[#FFDAB9]/30 to-[#FFB5C5]/20 blur-2xl animate-float"
                style={{
                    bottom: "15%",
                    left: "15%",
                    animationDelay: "4s",
                    animationDuration: "7s",
                }}
            />
            <div
                className="absolute w-16 h-16 sm:w-24 sm:h-24 rounded-full bg-gradient-to-br from-[#E6E0FF]/40 to-[#B5E8D5]/20 blur-xl animate-float"
                style={{
                    top: "30%",
                    right: "20%",
                    animationDelay: "1s",
                    animationDuration: "9s",
                }}
            />
            <div
                className="absolute w-28 h-28 sm:w-40 sm:h-40 rounded-full bg-gradient-to-br from-[#FFB5C5]/20 to-[#FFDAB9]/20 blur-2xl animate-float"
                style={{
                    bottom: "40%",
                    right: "30%",
                    animationDelay: "3s",
                    animationDuration: "11s",
                }}
            />
        </div>
    );
}
