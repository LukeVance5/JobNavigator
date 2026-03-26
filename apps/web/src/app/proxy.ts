import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

export function proxy(request: NextRequest) {
  const token = request.cookies.get("token")?.value;
  const { pathname } = request.nextUrl;

  const isLoginPage = pathname === "/login";
  const isRegisterPage = pathname === "/register";
  const isPublicAuthPage = isLoginPage || isRegisterPage;
  // If there's no token (user is not authenticated)
  if (!token) {
    // If trying to access a public authentication page (login or register), allow it
    if (isPublicAuthPage) {
      return NextResponse.next();
    }
    // Otherwise (trying to access any other page without a token), redirect to login
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // If there's a token (user is authenticated)
  if (token) {
    // If trying to access a public authentication page (login or register), redirect to home
    if (isPublicAuthPage) {
      return NextResponse.redirect(new URL("/", request.url));
    }
  }

  // For any other case (authenticated user accessing a protected route), allow it
  return NextResponse.next();
}

export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"],
};
