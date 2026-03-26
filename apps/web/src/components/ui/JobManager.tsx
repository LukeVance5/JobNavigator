// /components/jobs/JobManager.tsx
"use client";
import { JobElement } from "@/types/jobs";
import { JobCard } from "@/components/ui/JobCard";
import { useState, useEffect } from "react";
import { JobCreateForm } from "@/components/ui/JobCreateForm";

interface JobManagerProps {
  initialJobs: JobElement[];
}

export default function JobManager({ initialJobs }: JobManagerProps) {
  const [jobs, setJobs] = useState<JobElement[]>(initialJobs);
  const [showCreateForm, setShowCreateForm] = useState(false);

  useEffect(() => {
    setJobs(initialJobs);
  }, [initialJobs]);

  const handleJobCreated = (newJob: JobElement) => {
    setJobs((prevJobs) => [...prevJobs, newJob]);
    setShowCreateForm(false);
  };

  const deleteJob = async (id: string) => {
    const token = document.cookie
      .split("; ")
      .find((row) => row.startsWith("token="))
      ?.split("=")[1];
    if (!token) {
      console.error("Authentication token not found. Cannot delete job.");
      return;
    }

    try {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/jobs/${id}`,
        {
          method: "DELETE",
          headers: {
            Authorization: `Bearer ${token}`,
          },
        },
      );

      if (!response.ok) {
        throw new Error("Failed to delete job");
      }

      setJobs((prevJobs) => prevJobs.filter((j) => j.id !== id));
      console.log(`Job with ID ${id} deleted successfully.`);
    } catch (error) {
      console.error("Error deleting job:", error);
    }
  };

  return (
    <div>
      <button
        onClick={() => setShowCreateForm(true)}
        className="mb-4 px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
      >
        Add New Job
      </button>

      {showCreateForm && (
        <JobCreateForm
          onClose={() => setShowCreateForm(false)}
          onJobCreated={handleJobCreated} // Pass the handler
        />
      )}

      {jobs.map((job) => (
        <JobCard
          key={job.id}
          job={job}
          onDelete={deleteJob} // Pass the function reference here
        />
      ))}
    </div>
  );
}
