import React from 'react';
import './CommitteeList.css';
import Committee from '../Committee/Committee';

const committeeLinks = {
  'The Academic Coordinating Commission (ACC)': '#',
  'The Presidents Council': '#',
  'Student Parking Committee': '#'
};

function CommitteeList({ committees }) {
  return (
    <div className="CommitteeList">
      {committees.map((committee, index) => (
        <Committee 
          key={index} 
          committee={{
            ...committee,
            bulletPoints: committee.bulletPoints.map(point => ({
              text: point,
              link: !point.includes('Bla bla bla foobar') 
                ? committeeLinks[point] 
                : null
            }))
          }} 
        />
      ))}
    </div>
  );
}

export default CommitteeList;