// /apps/web/app/components/Input.tsx
import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  id: string;
}

export const Input = React.forwardRef<HTMLInputElement, InputProps>(
  ({ id, ...props }, ref) => {
    return (
      <div>
        <label htmlFor={id} className="sr-only">
          {props.placeholder}
        </label>
        <input
          id={id}
          ref={ref}
          className="relative block w-full px-3 py-2 text-gray-900 placeholder-gray-500 border border-gray-300 rounded-md appearance-none focus:outline-none focus:ring-blue-500 focus:border-blue-500 focus:z-10 sm:text-sm"
          {...props}
        />
      </div>
    );
  },
);

Input.displayName = "Input";
