import React from "react";

interface InputProps extends React.InputHTMLAttributes<HTMLInputElement> {
  id: string;
}

// 1. Define the function
function InputElement(
  { id, ...props }: InputProps, 
  ref: React.ForwardedRef<HTMLInputElement>
) {
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
}

// 2. Wrap it in forwardRef and export it
export const Input = React.forwardRef(InputElement);

Input.displayName = "Input";