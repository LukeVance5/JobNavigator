import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";
// /apps/web/src/middleware.ts

export function middleware(request: NextRequest) {
  const token = request.cookies.get("token")?.value;
  const { pathname } = request.nextUrl;

  const publicRoutes = ["/login", "/register"];
  
  // Check if the current path is one of our public routes
  const isPublicRoute = publicRoutes.includes(pathname);

  // 1. If there is NO token and it's NOT a public route, redirect to login
  if (!token && !isPublicRoute) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // 2. If there IS a token and the user tries to go to login/register, 
  // send them to the dashboard (root)
  if (token && isPublicRoute) {
    return NextResponse.redirect(new URL("/", request.url));
  }

  return NextResponse.next();
}
export const config = {
  matcher: ["/((?!api|_next/static|_next/image|favicon.ico).*)"], // Apply middleware to all routes except API, static files, and images
};
