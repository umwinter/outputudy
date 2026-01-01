import { login } from "@/actions/auth";
import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import { useRouter } from "next/navigation";
import { type Mock, beforeEach, describe, expect, it, vi } from "vitest";
import { LoginForm } from "./login-form";

// Mock the external dependencies
vi.mock("next/navigation", () => ({
  useRouter: vi.fn(),
}));

vi.mock("@/actions/auth", () => ({
  login: vi.fn(),
}));

describe("LoginForm", () => {
  const mockPush = vi.fn();
  const mockRefresh = vi.fn();

  beforeEach(() => {
    vi.clearAllMocks();
    (useRouter as Mock).mockReturnValue({
      push: mockPush,
      refresh: mockRefresh,
    });
  });

  it("renders login form correctly", () => {
    render(<LoginForm />);
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole("button", { name: /sign in/i })).toBeInTheDocument();
  });

  it("shows error messages for empty fields", async () => {
    render(<LoginForm />);
    const submitButton = screen.getByRole("button", { name: /sign in/i });

    fireEvent.click(submitButton);

    await waitFor(() => {
      expect(screen.getByText(/please enter a valid email address/i)).toBeInTheDocument();
      expect(screen.getByText(/password is required/i)).toBeInTheDocument();
    });
  });

  it("calls login action with correct values and redirects on success", async () => {
    (login as Mock).mockResolvedValue({ success: true });

    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "test@example.com" } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: "password123" } });

    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(login).toHaveBeenCalledWith({
        email: "test@example.com",
        password: "password123",
      });
      expect(mockPush).toHaveBeenCalledWith("/home");
    });
  });

  it("displays error message on login failure", async () => {
    (login as Mock).mockResolvedValue({ error: "Invalid credentials" });

    render(<LoginForm />);

    fireEvent.change(screen.getByLabelText(/email/i), { target: { value: "test@example.com" } });
    fireEvent.change(screen.getByLabelText(/password/i), { target: { value: "wrongpassword" } });

    fireEvent.click(screen.getByRole("button", { name: /sign in/i }));

    await waitFor(() => {
      expect(screen.getByText(/invalid credentials/i)).toBeInTheDocument();
    });
  });
});
