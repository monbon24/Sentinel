import { AppCard } from "@/components/AppCard";
import { HubCard } from "@/components/HubCard";
import { StatusIndicator } from "@/components/StatusIndicator";
import { FloatingShapes } from "@/components/FloatingShapes";

// App configuration - easy to update URLs here
const apps = [
    {
        title: "Homeschool Planner",
        description: "Organize your learning journey",
        icon: "📚",
        href: "https://your-homeschool-planner.vercel.app",
        accentColor: "pink" as const,
        external: true,
    },
    {
        title: "Command Center",
        description: "Mission control for everything",
        icon: "🎮",
        href: "https://your-command-center.vercel.app",
        accentColor: "lavender" as const,
        external: true,
    },
    {
        title: "Aeon Trespass Tracker",
        description: "Track your epic adventures",
        icon: "🎲",
        href: "https://your-aeon-tracker.vercel.app",
        accentColor: "mint" as const,
        external: true,
    },
    {
        title: "Experimental Lab",
        description: "Where magic happens",
        icon: "🧪",
        href: "https://replit.com/@your-profile",
        accentColor: "peach" as const,
        external: true,
    },
];

const hubLink = {
    title: "OneNote Hub",
    description: "Central Data Source • The Brain Behind It All",
    icon: "📓",
    href: "https://1drv.ms/o/c/d0bb89681bb12b17/IgAF8ISl6L0HS4Dm4N4zIlxTARyeW_oBqSg76rDmgMds85M?e=6GsRCc",
};

export default function Home() {
    return (
        <>
            {/* Floating background shapes */}
            <FloatingShapes />

            <div className="min-h-dvh flex flex-col items-center px-4 py-8 sm:px-6 sm:py-12">
                <div className="w-full max-w-lg flex flex-col flex-1">
                    {/* Header */}
                    <header className="mb-8 sm:mb-12 text-center">
                        {/* Logo/Emoji */}
                        <div
                            className="w-16 h-16 sm:w-20 sm:h-20 bg-white rounded-3xl shadow-sm flex items-center justify-center text-3xl sm:text-4xl mb-6 mx-auto transform hover:rotate-12 transition-transform duration-300 cursor-default"
                            aria-label="Cherry blossom"
                        >
                            🌸
                        </div>

                        {/* Title */}
                        <h1 className="text-2xl sm:text-3xl font-extrabold text-[#5D5A6D] mb-2 tracking-tight">
                            Monica&apos;s App Launcher
                        </h1>

                        {/* Subtitle */}
                        <p className="text-base sm:text-lg font-semibold text-[#8E8A9D]">
                            Your cozy corner of the internet ✨
                        </p>
                    </header>

                    {/* App Grid - Single column on mobile, 2 columns on tablet+ */}
                    <main className="flex-1">
                        <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 sm:gap-5 mb-6">
                            {apps.map((app) => (
                                <AppCard
                                    key={app.title}
                                    title={app.title}
                                    description={app.description}
                                    icon={app.icon}
                                    href={app.href}
                                    accentColor={app.accentColor}
                                    external={app.external}
                                />
                            ))}
                        </div>

                        {/* OneNote Hub Card */}
                        <HubCard
                            title={hubLink.title}
                            description={hubLink.description}
                            icon={hubLink.icon}
                            href={hubLink.href}
                        />
                    </main>

                    {/* Footer */}
                    <footer className="mt-8 sm:mt-12 flex justify-center">
                        <StatusIndicator status="online" text="System Online" />
                    </footer>
                </div>
            </div>
        </>
    );
}
