import Link from "next/link";
import { Button } from "@/components/ui/button";

export default function Home() {
  return (
    <div className="flex min-h-screen flex-col items-center justify-center bg-background text-foreground">
      <main className="flex flex-col items-center gap-8 text-center p-8">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          Outputudy
        </h1>
        <p className="max-w-md text-lg text-muted-foreground">
          Output + Study. A learning-focused blog platform.
        </p>
        <div className="flex gap-4">
          <Button asChild>
            <Link href="/login">Sign In</Link>
          </Button>
          <Button asChild variant="secondary">
            <a
              href="http://localhost:8001"
              target="_blank"
              rel="noopener noreferrer"
            >
              Valid Docs
            </a>
          </Button>
        </div>
      </main>
    </div>
  );
}
