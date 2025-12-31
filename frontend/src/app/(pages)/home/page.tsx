import { auth, signOut } from "@/auth";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { siteConfig } from "@/config/site";

export default async function HomePage() {
  const session = await auth();

  return (
    <div className="bg-background flex min-h-screen items-center justify-center p-4">
      <Card className="w-full max-w-md">
        <CardHeader>
          <CardTitle>
            {siteConfig.home.welcomePrefix}
            {session?.user?.name || siteConfig.home.welcomeDefaultUser}
            {siteConfig.home.welcomeSuffix}
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <p className="text-muted-foreground">
            {siteConfig.home.loggedInAs}
            <span className="text-foreground font-medium">{session?.user?.email}</span>
          </p>
          <form
            action={async () => {
              "use server";
              await signOut({ redirectTo: "/login" });
            }}
          >
            <Button variant="destructive" className="w-full">
              {siteConfig.home.signOutButton}
            </Button>
          </form>
        </CardContent>
      </Card>
    </div>
  );
}
