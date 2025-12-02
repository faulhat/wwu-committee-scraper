import React, { useState } from 'react';
import './Committee.css';

function Committee({ committee, onDelete }) {
  const [isHidden, setIsHidden] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  /* -------------------- helpers -------------------- */

  const toTitleCase = (str) =>
    str
      ?.toLowerCase()
      .replace(/\b\w/g, (l) => l.toUpperCase());

  const formatTitle = (title, url) => {
    if (title) return toTitleCase(title);

    const parts = url.split('/').filter(Boolean);
    return toTitleCase(
      parts[parts.length - 1].replace(/-/g, ' ')
    );
  };

    const extractSubdomain = (url) => {
    try {
      const urlObject = new URL(url);
      const hostname = urlObject.hostname;

      const parts = hostname.split('.');
      if (parts.length < 3) return null;

      return parts.slice(0, -2).join('.').toUpperCase();
    } catch {
      return null;
    }
  };


  /* -------------------- actions -------------------- */

  const handleDelete = async (e) => {
    e.preventDefault();
    e.stopPropagation();

    if (!window.confirm('Delete this committee permanently?')) return;

    try {
      const res = await fetch(
        `/delete/pages/url?url=${encodeURIComponent(committee.url)}`,
        { method: 'DELETE' }
      );

      if (res.ok) {
        setIsHidden(true);
        onDelete && onDelete(committee.url);
      } else {
        alert('Delete failed.');
      }
    } catch {
      alert('Error deleting page.');
    }
  };

  const handleHide = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsHidden(true);
  };

  if (isHidden) return null;

  /* -------------------- render -------------------- */

  return (
    <div className={`Committee ${isExpanded ? 'expanded' : ''}`}>
      {/* Title bar (click to expand) */}
      <div
        className="committee-title-container"
        onClick={() => setIsExpanded((prev) => !prev)}
      >
        <h2 className="committee-title">
          {formatTitle(committee.title, committee.url)}
        </h2>
      </div>

      {isExpanded && (
        <div className="committee-content">
          {/* Info sections */}
          <div className="committee-description">
            <div className="committee-section">
              <h3>Subdomain</h3>
              <p>{extractSubdomain(committee.url) || 'Not Available'}</p>
            </div>

            <div className="committee-section">
              <h3>Committee Summary</h3>
              <p>
                {committee.summary_before}{' '}
                <strong>{committee.summary_keyword}</strong>{' '}
                {committee.summary_after}
              </p>
            </div>

            <div className="committee-section">
              <h3>Key Term / Contact</h3>
              <p>{committee.summary_keyword || 'Not Available'}</p>
            </div>
          </div>

          {/* Actions */}
          <div className="committee-actions">
            <button onClick={handleHide} className="hide-button">
              Hide
            </button>

            <button onClick={handleDelete} className="remove-button">
              Delete
            </button>

            <a
              href={committee.url}
              target="_blank"
              rel="noopener noreferrer"
              className="link-button"
              onClick={(e) => e.stopPropagation()}
            >
              Visit Website
            </a>
          </div>
        </div>
      )}
    </div>
  );
}

export default Committee;
