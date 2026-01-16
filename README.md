# Monica's App Launcher (Sentinel)

✨ Your cozy corner of the internet - A beautiful, tablet-first app launcher PWA.

## What This App Does

A personal dashboard/app launcher that provides quick access to all your apps:

- **Homeschool Planner** - Organize learning journeys
- **Command Center** - Mission control for everything
- **Aeon Trespass Tracker** - Track epic adventures
- **Experimental Lab** - Where magic happens
- **OneNote Hub** - Central data source

## Features

- 🌸 **Cozy Pastel Aesthetic** - Soft colors, rounded corners, glassmorphism
- 📱 **Tablet-First Design** - 44px+ touch targets, no hover-dependent features
- ✨ **Floating Shapes Animation** - Beautiful background visual effects
- 🔄 **PWA Support** - Install to home screen on iOS/Android
- 🎨 **Accent Colors** - Pink, Lavender, Mint, Peach themes for cards

## How to Update

### Update App URLs

Edit `src/app/page.tsx` and modify the `apps` array:

```tsx
const apps = [
  {
    title: "Your App Name",
    description: "App description",
    icon: "📚", // Any emoji
    href: "https://your-app-url.vercel.app",
    accentColor: "pink", // pink | lavender | mint | peach
    external: true,
  },
  // ... add more apps
];
```

### Update OneNote Hub Link

Edit the `hubLink` object in the same file.

## Tech Stack

- **Next.js 16** with React 19
- **Tailwind CSS 4** with custom cozy design tokens
- **shadcn/ui** components (customized)
- **Nunito** font from Google Fonts

## Deployment URL

🚀 **Vercel**: [Update with your deployment URL]

## Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev

# Build for production
npm run build
```

## Debug/Settings

The app includes a Status Indicator in the footer showing system status.
For a full reset, clear browser localStorage and refresh.

---

Built with 💕 following the Cozy Productivity principles.
