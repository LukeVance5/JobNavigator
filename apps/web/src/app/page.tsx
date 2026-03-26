'use client'

import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Home() {
  const router = useRouter();

  useEffect(() => {
    // This runs immediately after the component mounts
    router.replace("/dashboard"); 
  }, [router]);

  return <p>Redirecting you now...</p>;
}
