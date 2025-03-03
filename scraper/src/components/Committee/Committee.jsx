import React from 'react';
import './Committee.css'; // Updated CSS file

function Committee({ committee }) {
  return (
    <div className="Committee">
      <h2 className="committee-title">{committee.title}</h2>
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