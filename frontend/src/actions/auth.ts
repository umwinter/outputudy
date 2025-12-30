"use server";

import { signIn } from "@/auth";
import { AuthError } from "next-auth";

export async function login(values: { email: string; password: string }) {
  try {
    // "credentials" is the provider id we defined in auth.ts
    // redirect: false prevents NextAuth from throwing immediately on success, allows us to handle it
    await signIn("credentials", {
      email: values.email,
      password: values.password,
      redirect: false,
    });
    return { success: true };
  } catch (error) {
    if (error instanceof AuthError) {
      switch (error.type) {
        case "CredentialsSignin":
          return { error: "Invalid credentials!" };
        default:
          return { error: "Something went wrong!" };
      }
    }
    // next-auth throws a redirect error on success if redirect: true,
    // but we set redirect: false.
    // However, if we change strategy later, we must rethrow error if it's not AuthError
    throw error;
  }
}
