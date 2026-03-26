import { cookies } from "next/headers";
import { redirect } from "next/navigation";
import JobManager from "@/components/ui/JobManager";

async function getJobs() {
  const cookieStore = await cookies();
  const token = cookieStore.get("token")?.value;
  console.log(token)
  // 1. Protection: If no token, redirect to login immediately
  if (!token) {
    redirect("/login");
  }

  // 2. Data Fetching: Fetch from your Python API
  const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/api/v1/jobs`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
    next: { revalidate: 3600 }, // Optional: Cache data for 1 hour
  });

  if (!response.ok) {
    // Handle unauthorized or server errors
    if (response.status === 401) redirect("/login");
    throw new Error("Failed to fetch jobs");
  }

  return response.json();
}

export default async function DashboardPage() {
  const initialJobsStruct = await getJobs();
  const initialJobs = initialJobsStruct.jobs;

  return (
    <div className="flex min-h-screen bg-gray-50">
      {/* Navigation Shell */}

      <main className="flex-1 p-8">
        <header className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-500">Track and manage your job applications</p>
          </div>
          
          {/* Example Stats Widget */}
          <div className="flex gap-4">
            <div className="bg-white p-4 rounded-lg shadow-sm border">
              <span className="text-sm text-gray-500">Total Applied</span>
              <p className="text-2xl font-bold">{initialJobs.length}</p>
            </div>
          </div>
        </header>

        {/* The Interactive Logic Layer */}
        <JobManager initialJobs={initialJobs} />
      </main>
    </div>
  );
}