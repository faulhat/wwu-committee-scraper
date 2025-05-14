import React from 'react';
import './Committee.css';

function Committee({ committee }) {
  const formatTitle = (title, url) => {
    if (title) return title;
    const parts = url.split('/').filter(part => part);
    return parts[parts.length - 1]
      .replace(/-/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  return (
    <div className="Committee">
      <div className="committee-content">
        <h2 className="committee-title">
          {formatTitle(committee.title, committee.url)}
        </h2>
        <p className="committee-description">{committee.summary}</p>
        <div className="committee-actions">

          -<a
            href={committee.url}
            target="_blank"
            rel="noopener noreferrer"
            className="committee-link"
          >
           Here
          </a>
        </div>
      </div>
    </div>
  );
}

export default Committee;
