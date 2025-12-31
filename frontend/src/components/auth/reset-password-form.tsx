"use client";

import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
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
import { useState } from "react";
import { resetPassword } from "@/actions/auth";
import { siteConfig } from "@/config/site";
import { useRouter } from "next/navigation";

const formSchema = z
    .object({
        password: z.string().min(8, "Password must be at least 8 characters"),
        confirmPassword: z.string(),
    })
    .refine((data) => data.password === data.confirmPassword, {
        message: "Passwords don't match",
        path: ["confirmPassword"],
    });

interface ResetPasswordFormProps {
    token: string;
}

export function ResetPasswordForm({ token }: ResetPasswordFormProps) {
    const router = useRouter();
    const [error, setError] = useState<string | undefined>("");
    const [success, setSuccess] = useState<boolean>(false);

    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            password: "",
            confirmPassword: "",
        },
    });

    async function onSubmit(values: z.infer<typeof formSchema>) {
        setError("");

        const res = await resetPassword({
            token,
            new_password: values.password,
        });

        if (res.error) {
            setError(res.error);
        } else {
            setSuccess(true);
            setTimeout(() => {
                router.push("/login");
            }, 3000);
        }
    }

    if (success) {
        return (
            <div className="rounded-md bg-green-50 p-4 text-sm font-medium text-green-600">
                Password reset successfully! Redirecting to login...
            </div>
        );
    }

    return (
        <div className="w-full">
            {error && (
                <div className="bg-destructive/15 text-destructive mb-4 rounded-md p-4 text-sm font-medium">
                    {error}
                </div>
            )}
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                    <FormField
                        control={form.control}
                        name="password"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>{siteConfig.auth.resetPassword.passwordLabel}</FormLabel>
                                <FormControl>
                                    <Input type="password" {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <FormField
                        control={form.control}
                        name="confirmPassword"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>{siteConfig.auth.resetPassword.confirmPasswordLabel}</FormLabel>
                                <FormControl>
                                    <Input type="password" {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <Button type="submit" className="w-full" disabled={form.formState.isSubmitting}>
                        {form.formState.isSubmitting
                            ? siteConfig.auth.resetPassword.submittingButton
                            : siteConfig.auth.resetPassword.submitButton}
                    </Button>
                </form>
            </Form>
        </div>
    );
}
