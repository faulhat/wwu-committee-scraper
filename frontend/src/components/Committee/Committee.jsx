import React, { useState } from 'react';
import './Committee.css';

function Committee({ committee, onDelete }) {
  const [isHidden, setIsHidden] = useState(false);
  const [isExpanded, setIsExpanded] = useState(false);

  const formatTitle = (title, url) => {
    if (title) return title;
    const parts = url.split('/').filter(part => part);
    return parts[parts.length - 1]
      .replace(/-/g, ' ')
      .replace(/\b\w/g, l => l.toUpperCase());
  };

  function extractSubdomain(url) {
    try {
      const urlObject = new URL(url);
      const hostname = urlObject.hostname;
      if (/^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$/.test(hostname)) {
        return null;
      }
      const parts = hostname.split('.');
      if (parts.length < 3) {
        return null;
      }
      const domainAndTld = parts.slice(-2).join('.');
      const potentialSubdomainParts = parts.slice(0, -2);
      if (potentialSubdomainParts.length > 0) {
        return potentialSubdomainParts.join('.');
      } else {
        return null;
      }
    } catch (error) {
      console.error("Invalid URL:", error);
      return null;
    }
  }

  const handleDelete = async (e) => {
    e.preventDefault();
    e.stopPropagation();
    if (!window.confirm('Confirm you want to permantly delete this committee?')) {
      return;
    }
    try {
      const response = await fetch(`/delete/pages/url?url=${encodeURIComponent(committee.url)}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        console.log('Page deleted successfully');
        setIsHidden(true);
        if (onDelete) {
          setTimeout(() => onDelete(committee.url), 300);
        }
      } else {
        console.error('Failed to delete page');
        alert('Failed to delete page. Please try again.');
      }
    } catch (error) {
      console.error('Error deleting page:', error);
      alert('Error deleting page. Please try again.');
    }
  };

  const handleHide = (e) => {
    e.preventDefault();
    e.stopPropagation();
    setIsHidden(true);
  };

  const toggleExpand = (e) => {
    e.preventDefault();
    setIsExpanded(!isExpanded);
  };

  // If hidden, dont render.
  if (isHidden) {
    return null;
  }

  return (
    <div className="Committee">
      <div className="committee-content">
        <div className="committee-header" onClick={toggleExpand}>
          <h2 className="committee-title">
            {formatTitle(committee.title, committee.url)}
          </h2>
        </div>
        
        {isExpanded && (
          <div className="committee-details">
            <a href={committee.url} target="_blank" rel="noopener noreferrer" className='committee-url'>
              <p className="committee-description">
                <h2 className='p-5 text-xl'><b>{extractSubdomain(committee.url)}</b> - WWU Subdomain</h2>
                <h2 className='p-5 text-xl'><b>Committee Summary</b></h2>
                {committee.summary_before}
                <b>{committee.summary_keyword}</b>
                <h2 className='p-5 text-xl'><b>Committee Position Keywords</b></h2>
                {committee.summary_after}
                <h2 className='p-5 text-xl'><b>Committee Contact</b></h2>
                {committee.summary_keyword}
              </p>
            </a>
            <div className="committee-actions">
              <button
                onClick={handleHide}
                className="hide-button">
                HIDE
              </button>
              <button
                onClick={handleDelete}
                className="remove-button">
                DELETE
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default Committee;
