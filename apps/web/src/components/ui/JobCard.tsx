import { Job, JobElement } from "@/types/jobs"; // Assuming you have a shared Job type

interface JobCardProps {
  job: JobElement;
  // This defines a function that takes a string and returns nothing
  onDelete: (id: string) => void;
}

export function JobCard({ job, onDelete }: JobCardProps) {
  return (
    <div className="bg-white border rounded-xl p-5 shadow-sm hover:shadow-md flex justify-between">
      <div>
        <h3 className="font-semibold text-lg">{job.title}</h3>
        <p className="text-gray-500">{job.company}</p>
        <span className="mt-2 inline-block px-2 py-1 bg-blue-50 text-blue-700 text-xs rounded">
          {job.status}
        </span>
      </div>

      <button
        onClick={() => onDelete(job.id)}
        className="text-red-500 hover:bg-red-50 p-2 rounded-lg transition-colors"
      >
        Delete
      </button>
    </div>
  );
}
