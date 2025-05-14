import React from 'react';
import Committee from '../Committee/Committee';
import './CommitteeList.css';

function CommitteeList({ committees }) {
  return (
    <div className="CommitteeList">
      {committees.length > 0 ? (
        committees.map((committee, index) => (
          <Committee key={index} committee={committee} />
        ))
      ) : (
        <div className="no-committees">No committees found in this category</div>
      )}
    </div>
  );
}

export default CommitteeList;