import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="bg-background text-foreground flex min-h-screen flex-col items-center justify-center">
      <main className="flex flex-col items-center gap-8 p-8 text-center">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">Outputudy</h1>
        <p className="text-muted-foreground max-w-md text-lg">
          Output + Study. A learning-focused blog platform.
        </p>
        <div className="flex gap-4">
          <Button asChild>
            <Link href="/login">Sign In</Link>
          </Button>
          <Button asChild variant="secondary">
            <a href="http://localhost:8001" target="_blank" rel="noopener noreferrer">
              Valid Docs
            </a>
          </Button>
        </div>
      </main>
    </div>
  );
}
