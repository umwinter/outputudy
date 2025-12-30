import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { z } from "zod";

export const { handlers, signIn, signOut, auth } = NextAuth({
  session: {
    strategy: "jwt",
    maxAge: 24 * 60 * 60, // 24 hours
  },
  providers: [
    Credentials({
      credentials: {
        email: {},
        password: {},
      },
      authorize: async (credentials) => {
        const parsedCredentials = z
          .object({ email: z.string().email(), password: z.string().min(1) })
          .safeParse(credentials);

        if (parsedCredentials.success) {
          try {
            const res = await fetch("http://backend:8000/api/auth/login", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({
                email: parsedCredentials.data.email,
                password: parsedCredentials.data.password,
              }),
            });

            if (!res.ok) return null;

            const user = await res.json();
            // user object now contains access_token from backend
            return user;
          } catch (e) {
            console.error(e);
            return null;
          }
        }
        return null;
      },
    }),
  ],
  callbacks: {
    async jwt({ token, user }) {
      if (user) {
        // access_token exists on our backend response
        token.accessToken = user.access_token;
        // @ts-expect-error - id exists on our backend response
        token.id = user.id;
      }
      return token;
    },
    async session({ session, token }) {
      if (token) {
        // @ts-expect-error - accessToken exists on token
        session.accessToken = token.accessToken;
        // @ts-expect-error - id exists on user
        session.user.id = token.id;
      }
      return session;
    },
  },
  pages: {
    signIn: "/login",
  },
});
