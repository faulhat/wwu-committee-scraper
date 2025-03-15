import React, { useState } from 'react';
import CommitteeList from '../CommitteeList/CommitteeList';
import Footer from '../Footer/Footer';
import Subheader from '../Subheader/Subheader';
import { Toaster } from "react-hot-toast";
import './App.css';
import gif from '../../assets/oldmain.gif';
import img2 from '../../assets/img2.png';
import img3 from '../../assets/aa.png';
import img4 from '../../assets/a.png';
import img5 from '../../assets/aaa.png';
import img6 from '../../assets/aaaa.png';

const committees = [
  {
    title: 'Academic Committees',
    bulletPoints: [
      'Bla bla bla foobar',
      'Bla bla bla foobar',
      'Bla bla bla foobar',
    ],
  },
  {
    title: 'Faculty Committees',
    bulletPoints: [
      'Bla bla bla foobar',
      'Bla bla bla foobar',
      'Bla bla bla foobar',
    ],
  },
  {
    title: 'Student Committees',
    bulletPoints: [
      'Bla bla bla foobar',
      'Bla bla bla foobar',
      'Bla bla bla foobar',
    ],
  },
  {
    title: 'Uncategorized Committees',
    bulletPoints: [
      'Bla bla bla foobar',
      'Bla bla bla foobar',
      'Bla bla bla foobar',
    ],
    isUncategorized: true,
  },
];

function App() {
  // All sections as expanded (open) by default
  const [expandedSections, setExpandedSections] = useState({
    academic_committees: true,
    faculty_committees: true,
    student_committees: true,
    uncategorized_committees: true,
  });

  const toggleSection = (section) => {
    setExpandedSections((prev) => ({
      ...prev,
      [section]: !prev[section],
    }));
  };

  return (
    <div className="App">
      <h1>
        <a href="https://www.wwu.edu/" target="_blank" rel="noopener noreferrer">
          <img src={img2} alt="Logo" className="header-logo" />
        </a>
        <div className="header-right-images">
          <a href="https://admissions.wwu.edu/apply" target="_blank" rel="noopener noreferrer">
            <img src={img5} alt="Icon 3" className="header-icon" />
          </a>
          <a href="https://alumniq.wwu.edu/giving/make-a-gift" target="_blank" rel="noopener noreferrer">
            <img src={img6} alt="Icon 4" className="header-icon" />
          </a>
          <a href="https://mywestern.wwu.edu/" target="_blank" rel="noopener noreferrer">
            <img src={img3} alt="Icon 1" className="header-icon" />
          </a>
          <a href="https://search.wwu.edu/?q=%20site%3Amywestern.wwu.edu" target="_blank" rel="noopener noreferrer">
            <img src={img4} alt="Icon 2" className="header-icon" />
          </a>
        </div>
      </h1>
      <Subheader />
      <div className="gif-container">
        <a rel="noopener noreferrer">
          <img src={gif} alt="Animation" className="gif" />
        </a>
      </div>
      <h2 className="committee-main-title">STUDENT COMMITTEES</h2>
      {committees.map((committee, index) => {
        const sectionKey = committee.title.toLowerCase().replace(' ', '_');
        return (
          <div key={index}>
            <div
              className="committee-header"
              onClick={() => toggleSection(sectionKey)}
            >
              <h2 className={`committee-title ${committee.isUncategorized ? 'uncategorized-title' : ''}`}>
                {committee.title}
                <span className="toggle-icon">
                  {expandedSections[sectionKey] ? '▼' : '▶'}
                </span>
              </h2>
            </div>
            {expandedSections[sectionKey] && (
              <CommitteeList committees={[committee]} showTitle={false} />
            )}
          </div>
        );
      })}
      <Toaster position="top-center" reverseOrder={false} />
      <Footer />
    </div>
  );
}

export default App;