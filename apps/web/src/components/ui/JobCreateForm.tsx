// apps/web/src/components/ui/JobCreateForm.tsx
"use client";

import React, { useState } from "react";
import { Input } from "@/components/ui/Input";
import { useRouter } from "next/navigation"; // Import useRouter
import { JobElement } from "@/types/jobs"; // Import JobElement

interface JobCreateFormProps {
  onClose: () => void;
  onJobCreated: (newJob: JobElement) => void; // Callback to refresh job list
}

export function JobCreateForm({ onClose, onJobCreated }: JobCreateFormProps) {
  const router = useRouter(); // Initialize useRouter
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("");
  const [minSalary, setMinSalary] = useState<number | undefined>(undefined);
  const [maxSalary, setMaxSalary] = useState<number | undefined>(undefined);
  const [currency, setCurrency] = useState("");
  const [rate, setRate] = useState<string>("hourly"); // Default to hourly
  const [appliedAt, setAppliedAt] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (event: React.FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    setError(null);
    setLoading(true);

    const jobData = {
      title,
      description,
      company: company || undefined,
      location: location || undefined,
      salary_range:
        minSalary !== undefined && maxSalary !== undefined && currency
          ? {
              min: minSalary,
              max: maxSalary,
              currency,
              rate: rate,
            }
          : undefined,
      applied_at: appliedAt ? new Date(appliedAt).toISOString() : undefined,
    };

    try {
      // Retrieve token from cookie
      const token = document.cookie
        .split("; ")
        .find((row) => row.startsWith("token="))
        ?.split("=")[1];

      if (!token) {
        throw new Error("Authentication token not found. Please log in.");
      }
      console.log("JobCreateForm Token");
      console.log(token);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_API_URL}/api/v1/jobs/`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`, // Include the token in the header
          },
          body: JSON.stringify(jobData),
        },
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Failed to create job");
      }

      const newJob = await response.json();
      console.log("Job created successfully:", newJob);
      onJobCreated(newJob); // Notify parent to refresh list
      onClose(); // Close the form
    } catch (err: any) {
      setError(err.message || "An unexpected error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-gray-600 bg-opacity-50 flex justify-center items-center p-4">
      <div className="bg-white rounded-lg shadow-xl p-6 w-full max-w-lg">
        <h2 className="text-2xl font-bold mb-4">Create New Job</h2>
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label
              htmlFor="title"
              className="block text-sm font-medium text-gray-700"
            >
              Title
            </label>
            <Input
              id="title"
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              required
            />
          </div>
          <div>
            <label
              htmlFor="description"
              className="block text-sm font-medium text-gray-700"
            >
              Description
            </label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              rows={4}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
              required
            ></textarea>
          </div>
          <div>
            <label
              htmlFor="company"
              className="block text-sm font-medium text-gray-700"
            >
              Company
            </label>
            <Input
              id="company"
              type="text"
              value={company}
              onChange={(e) => setCompany(e.target.value)}
            />
          </div>
          <div>
            <label
              htmlFor="location"
              className="block text-sm font-medium text-gray-700"
            >
              Location
            </label>
            <Input
              id="location"
              type="text"
              value={location}
              onChange={(e) => setLocation(e.target.value)}
            />
          </div>
          <div className="grid grid-cols-3 gap-4">
            <div>
              <label
                htmlFor="minSalary"
                className="block text-sm font-medium text-gray-700"
              >
                Min Salary
              </label>
              <Input
                id="minSalary"
                type="number"
                value={minSalary === undefined ? "" : minSalary}
                onChange={(e) =>
                  setMinSalary(
                    e.target.value ? parseFloat(e.target.value) : undefined,
                  )
                }
              />
            </div>
            <div>
              <label
                htmlFor="maxSalary"
                className="block text-sm font-medium text-gray-700"
              >
                Max Salary
              </label>
              <Input
                id="maxSalary"
                type="number"
                value={maxSalary === undefined ? "" : maxSalary}
                onChange={(e) =>
                  setMaxSalary(
                    e.target.value ? parseFloat(e.target.value) : undefined,
                  )
                }
              />
            </div>
            <div>
              <label
                htmlFor="currency"
                className="block text-sm font-medium text-gray-700"
              >
                Currency
              </label>
              <Input
                id="currency"
                type="text"
                value={currency}
                onChange={(e) => setCurrency(e.target.value)}
              />
            </div>
          </div>
          <div>
            <label
              htmlFor="rate"
              className="block text-sm font-medium text-gray-700"
            >
              Rate
            </label>
            <select
              id="rate"
              value={rate}
              onChange={(e) => setRate(e.target.value)}
              className="mt-1 block w-full border border-gray-300 rounded-md shadow-sm p-2"
            >
              <option value="hourly">Hourly</option>
              <option value="daily">Daily</option>
              <option value="weekly">Weekly</option>
              <option value="monthly">Monthly</option>
              <option value="yearly">Yearly</option>
            </select>
          </div>
          <div>
            <label
              htmlFor="appliedAt"
              className="block text-sm font-medium text-gray-700"
            >
              Applied At
            </label>
            <Input
              id="appliedAt"
              type="date"
              value={appliedAt}
              onChange={(e) => setAppliedAt(e.target.value)}
            />
          </div>
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <div className="flex justify-end space-x-2">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={loading}
              className="px-4 py-2 text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? "Creating..." : "Create Job"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
