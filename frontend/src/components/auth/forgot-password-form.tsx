"use client";

import { forgotPassword } from "@/actions/auth";
import { Button } from "@/components/ui/button";
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form";
import { Input } from "@/components/ui/input";
import { siteConfig } from "@/config/site";
import { zodResolver } from "@hookform/resolvers/zod";
import { useState } from "react";
import { useForm } from "react-hook-form";
import * as z from "zod";

const formSchema = z.object({
  email: z.string().email(),
});

export function ForgotPasswordForm() {
  const [error, setError] = useState<string | undefined>("");
  const [success, setSuccess] = useState<string | undefined>("");

  const form = useForm<z.infer<typeof formSchema>>({
    resolver: zodResolver(formSchema),
    defaultValues: {
      email: "",
    },
  });

  async function onSubmit(values: z.infer<typeof formSchema>) {
    setError("");
    setSuccess("");

    // Server Action call
    const res = await forgotPassword(values);

    if (res.error) {
      setError(res.error);
    } else {
      setSuccess(siteConfig.auth.forgotPassword.successMessage);
    }
  }

  return (
    <div className="w-full">
      {success && (
        <div className="mb-4 rounded-md bg-green-50 p-4 text-sm font-medium text-green-600">
          {success}
        </div>
      )}
      {error && (
        <div className="bg-destructive/15 text-destructive mb-4 rounded-md p-4 text-sm font-medium">
          {error}
        </div>
      )}
      <Form {...form}>
        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
          <FormField
            control={form.control}
            name="email"
            render={({ field }) => (
              <FormItem>
                <FormLabel>Email</FormLabel>
                <FormControl>
                  <Input placeholder="name@example.com" {...field} />
                </FormControl>
                <FormMessage />
              </FormItem>
            )}
          />
          <Button type="submit" className="w-full" disabled={form.formState.isSubmitting}>
            {form.formState.isSubmitting ? "Sending..." : "Send Reset Link"}
          </Button>
        </form>
      </Form>
    </div>
  );
}
