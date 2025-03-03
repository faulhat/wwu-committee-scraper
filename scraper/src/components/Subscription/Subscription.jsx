import React from "react";

function Subscription() {
  return (
    <div className="mx-auto">
      <div className="relative isolate overflow-hidden px-3 py-2 shadow bg-[#007AC8]"> {/* Smaller padding */}
        <div className="mx-auto max-w-2xl text-center">
          <a
            href="https://as.wwu.edu/gov/" // Replace with actual URL
            className="!text-white text-xs font-bold tracking-tight hover:underline inline-block mr-4" // Smaller font size
            target="_blank" // Open in new tab
            rel="noopener noreferrer" // Security best practice
          >
            ASWWU Government
          </a>
          <a
            href="https://as.wwu.edu/oce/" // Replace with actual URL
            className="!text-white text-xs font-bold tracking-tight hover:underline inline-block" // Smaller font size
            target="_blank" // Open in new tab
            rel="noopener noreferrer" // Security best practice
          >
            Office of Civic Engagement
          </a>
        </div>
      </div>
    </div>
  );
}

export default Subscription;


