import React from "react";

function Subheader() {
  return (
    <div className="mx-auto">
      <div className="relative isolate overflow-hidden px-3 py-2 shadow bg-[#007AC8]">
        <div className="mx-auto max-w-2xl text-center">
          <a
            href="https://as.wwu.edu/gov/"
            className="!text-white text-xs font-bold tracking-tight hover:underline inline-block mr-4" 
            target="_blank"
            rel="noopener noreferrer"
          >
            ASWWU Government
          </a>
          <a
            href="https://as.wwu.edu/oce/"
            className="!text-white text-xs font-bold tracking-tight hover:underline inline-block"
            target="_blank"
            rel="noopener noreferrer"
          >
            Office of Civic Engagement
          </a>
        </div>
      </div>
    </div>
  );
}

export default Subheader;


