import type { Metadata, Viewport } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";

const nunito = Nunito({
    subsets: ["latin"],
    weight: ["400", "600", "700", "800"],
    variable: "--font-nunito",
});

export const metadata: Metadata = {
    title: "✨ Monica's App Launcher",
    description: "Your cozy corner of the internet - Access all your apps in one place",
    manifest: "/manifest.json",
    appleWebApp: {
        capable: true,
        statusBarStyle: "default",
        title: "App Launcher",
    },
    formatDetection: {
        telephone: false,
    },
    icons: {
        icon: "/icons/icon-192.png",
        apple: "/icons/icon-192.png",
    },
};

export const viewport: Viewport = {
    themeColor: "#FFB5C5",
    width: "device-width",
    initialScale: 1,
    maximumScale: 1,
    userScalable: false,
    viewportFit: "cover",
};

export default function RootLayout({
    children,
}: Readonly<{
    children: React.ReactNode;
}>) {
    return (
        <html lang="en">
            <head>
                {/* iOS PWA Meta Tags */}
                <meta name="apple-mobile-web-app-capable" content="yes" />
                <meta name="apple-mobile-web-app-status-bar-style" content="default" />
                <meta name="apple-mobile-web-app-title" content="App Launcher" />
                <link rel="apple-touch-icon" href="/icons/icon-192.png" />
            </head>
            <body className={`${nunito.variable} font-sans antialiased`}>
                {children}
            </body>
        </html>
    );
}
