import NextAuth from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { z } from "zod";

export const { handlers, signIn, signOut, auth } = NextAuth({
  providers: [
    Credentials({
      // You can specify which fields should be submitted, by adding keys to the `credentials` object.
      // e.g. domain, username, password, 2FA token, etc.
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
  pages: {
    signIn: "/login",
  },
});
