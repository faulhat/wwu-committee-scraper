import React from 'react';
import './Committee.css';

function Committee({ committee, showTitle }) {
  return (
    <div className="Committee">
      {showTitle && <h2 className="committee-title">{committee.title}</h2>}
      <p className="committee-description">{committee.description}</p>
      <ul className="committee-bullet-points">
        {committee.bulletPoints.map((point, index) => (
          <li key={index} className="bullet-point">{point}</li>
        ))}
      </ul>
    </div>
  );
}

export default Committee;