"use server";

import { signIn } from "@/auth";
import { ApiError, AuthService } from "@/lib/api";
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
    await AuthService.register({
      name: values.name,
      email: values.email,
      password: values.password,
    });

    // After registration, log the user in
    return await login({ email: values.email, password: values.password });
  } catch (error) {
    if (error instanceof ApiError) {
      return { error: error.body?.detail || "Registration failed" };
    }
    console.error(error);
    return { error: "Something went wrong!" };
  }
}

export async function forgotPassword(values: { email: string }) {
  try {
    await AuthService.forgotPassword({ email: values.email });

    return { success: true };
  } catch (error) {
    if (error instanceof ApiError) {
      return { error: error.body?.detail || "Request failed" };
    }
    console.error(error);
    return { error: "Something went wrong!" };
  }
}

export async function resetPassword(values: { token: string; new_password: string }) {
  try {
    await AuthService.resetPassword({
      token: values.token,
      new_password: values.new_password,
    });

    return { success: true };
  } catch (error) {
    if (error instanceof ApiError) {
      return { error: error.body?.detail || "Reset failed" };
    }
    console.error(error);
    return { error: "Something went wrong!" };
  }
}
