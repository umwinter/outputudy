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
export async function register(values: { name: string; email: string; password: string }) {
  try {
    const res = await fetch("http://backend:8000/api/auth/register", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });

    if (!res.ok) {
      const errorData = await res.json();
      return { error: errorData.detail || "Registration failed" };
    }

    // After registration, log the user in
    return await login({ email: values.email, password: values.password });
  } catch (error) {
    console.error(error);
    return { error: "Something went wrong!" };
  }
}

export async function forgotPassword(values: { email: string }) {
  try {
    const res = await fetch("http://backend:8000/api/auth/forgot-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });

    if (!res.ok) {
      const errorData = await res.json();
      return { error: errorData.detail || "Request failed" };
    }

    return { success: true };
  } catch (error) {
    console.error(error);
    return { error: "Something went wrong!" };
  }
}

export async function resetPassword(values: { token: string; new_password: string }) {
  try {
    const res = await fetch("http://backend:8000/api/auth/reset-password", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(values),
    });

    if (!res.ok) {
      const errorData = await res.json();
      return { error: errorData.detail || "Reset failed" };
    }

    return { success: true };
  } catch (error) {
    console.error(error);
    return { error: "Something went wrong!" };
  }
}
