import React from 'react';
import './CommitteeList.css'; // Updated CSS file
import Committee from '../Committee/Committee'; // Updated component

function CommitteeList({ committees }) {
  return (
    <div className="CommitteeList">
      {committees.map((committee, index) => (
        <Committee key={index} committee={committee} />
      ))}
    </div>
  );
}

export default CommitteeList;