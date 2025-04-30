import React from 'react';
import './Committee.css';

const committeeLinks = {
  'The Academic Coordinating Commission (ACC)': 'https://as.wwu.edu/committees/academic-coordinating-commission/',
  'The Presidents Council': 'https://as.wwu.edu/committees/as-ethnic-student-center-executive-board/',
  'Student Parking Committee': '#'
};

function Committee({ committee, showTitle }) {
  return (
    <div className="Committee">
      {showTitle && <h2 className="committee-title">{committee.title}</h2>}
      <p className="committee-description">{committee.description}</p>
      <ul className="committee-bullet-points">
        {committee.bulletPoints.map((point, index) => {
          const pointText = typeof point === 'string' ? point : point.text || '';
          const isBlaBla = pointText.includes('Bla bla bla foobar');
          const hasLink = committeeLinks[pointText] && !isBlaBla;
          
          return (
            <li key={index} className="bullet-point">
              {pointText}
              {hasLink && (
                <>
                  {' - '}
                  <a 
                    href={committeeLinks[pointText]} 
                    target="_blank" 
                    rel="noopener noreferrer"
                    className="committee-link"
                  >
                    Here
                  </a>
                </>
              )}
            </li>
          );
        })}
      </ul>
    </div>
  );
}

export default Committee;