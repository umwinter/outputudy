import { auth } from "@/auth"

export default auth((req) => {
    // req.auth
    const isLoggedIn = !!req.auth
    console.log("Middleware: isLoggedIn:", isLoggedIn, "Path:", req.nextUrl.pathname)
})

// Optionally, don't invoke Middleware on some paths
export const config = {
    matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
}
