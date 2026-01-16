import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { cn } from "@/lib/utils";

const buttonVariants = cva(
    "inline-flex items-center justify-center gap-2 whitespace-nowrap rounded-2xl text-sm font-semibold transition-all duration-200 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-[#E6E0FF] focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 [&_svg]:pointer-events-none [&_svg]:size-4 [&_svg]:shrink-0 touch-target",
    {
        variants: {
            variant: {
                default:
                    "bg-gradient-to-r from-[#FFB5C5] to-[#E6E0FF] text-[#5D5A6D] shadow-md hover:shadow-lg active:scale-95",
                destructive:
                    "bg-gradient-to-r from-red-400 to-red-500 text-white shadow-md hover:shadow-lg active:scale-95",
                outline:
                    "border-2 border-[#E6E0FF] bg-white/60 text-[#5D5A6D] hover:bg-[#E6E0FF]/20 active:scale-95",
                secondary:
                    "bg-[#E6E0FF]/30 text-[#5D5A6D] hover:bg-[#E6E0FF]/50 active:scale-95",
                ghost:
                    "text-[#5D5A6D] hover:bg-[#E6E0FF]/20 active:scale-95",
                link:
                    "text-[#5D5A6D] underline-offset-4 hover:underline",
                pause:
                    "bg-gradient-to-r from-amber-300 to-amber-400 text-[#5D5A6D] shadow-md hover:shadow-lg active:scale-95",
                stop:
                    "bg-gradient-to-r from-red-400 to-red-500 text-white shadow-md hover:shadow-lg active:scale-95",
            },
            size: {
                default: "h-11 px-6 py-2",
                sm: "h-10 rounded-xl px-4",
                lg: "h-12 rounded-2xl px-8 text-base",
                icon: "h-11 w-11",
            },
        },
        defaultVariants: {
            variant: "default",
            size: "default",
        },
    }
);

export interface ButtonProps
    extends React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
    asChild?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
    ({ className, variant, size, asChild = false, ...props }, ref) => {
        const Comp = asChild ? Slot : "button";
        return (
            <Comp
                className={cn(buttonVariants({ variant, size, className }))}
                ref={ref}
                {...props}
            />
        );
    }
);
Button.displayName = "Button";

export { Button, buttonVariants };
