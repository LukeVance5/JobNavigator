// /apps/web/app/components/login/LoginForm.tsx
"use client";
import { useRouter } from "next/navigation";
import React, { useState } from "react";
import { Input } from "@/components/ui/Input";
import Link from "next/link";
export default function LoginForm() {
  const router = useRouter();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      const formData = new URLSearchParams();
      formData.append("username", email);
      formData.append("password", password);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/auth/login`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/x-www-form-urlencoded",
          },
          body: formData.toString(),
        },
      );

      if (!response.ok) {
        throw new Error("Failed to login");
      }

      const data = await response.json();
      console.log("Login successful:", data);

      // Assuming the API returns an access_token upon successful login
      const accessToken = data.access_token;

      if (accessToken) {
        // Set the token as an HTTP-only cookie
        // Using `fetch` for this from a client component requires a server action or API route
        // For simplicity and immediate fix, we'll use `document.cookie` but acknowledge it's not HTTP-only.
        // A better approach would be a server action or Next.js API route to set an HTTP-only cookie.
        // For middleware to read, a regular cookie is sufficient, but HTTP-only is best practice.
        document.cookie = `token=${accessToken}; path=/; max-age=3600;`; // Set for 1 hour
        console.log("Cookies after login:", document.cookie); // DEBUG LOG

        // Redirect to the home page
        router.push("/");
      } else {
        console.error("Login successful, but no access_token received.");
      }
    } catch (error) {
      console.error("Login error:", error);
      // Handle login error, e.g., show an error message
    }
  };

  return (
    <div className="flex items-center justify-center min-h-screen bg-gray-100">
      <div className="w-full max-w-md p-8 space-y-6 bg-white rounded-lg shadow-md">
        <h2 className="text-2xl font-bold text-center text-gray-900">Login</h2>
        <form className="space-y-6" onSubmit={handleSubmit}>
          <div>
            <Input
              id="email"
              type="email"
              placeholder="Email address"
              required
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </div>
          <div>
            <Input
              id="password"
              type="password"
              placeholder="Password"
              required
              value={password}
              onChange={(e) => setPassword(e.target.value)}
            />
          </div>
          <div>
            <button
              type="submit"
              className="w-full px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Sign in
            </button>
          </div>
          <div>
            <Link
              href="/register"
              className="w-full px-4 py-2 text-blue-600 border border-blue-600 rounded-md hover:bg-blue-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
            >
              Register
            </Link>
          </div>
        </form>
      </div>
    </div>
  );
}
