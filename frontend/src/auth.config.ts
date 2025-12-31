import type { NextAuthConfig } from "next-auth";
import Credentials from "next-auth/providers/credentials";
import { z } from "zod";
import { AuthService } from "@/lib/api";

export const authConfig = {
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
                        const user = await AuthService.login({
                            email: parsedCredentials.data.email,
                            password: parsedCredentials.data.password,
                        });
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
    callbacks: {
        async jwt({ token, user }) {
            if (user) {
                token.accessToken = user.access_token;
                // id exists on our backend response
                token.id = user.id.toString();
            }
            return token;
        },
        async session({ session, token }) {
            if (token) {
                session.accessToken = token.accessToken;
                session.user.id = token.id || session.user.id;
            }
            return session;
        },
    },
    session: {
        strategy: "jwt",
        maxAge: 24 * 60 * 60, // 24 hours
    },
} satisfies NextAuthConfig;
