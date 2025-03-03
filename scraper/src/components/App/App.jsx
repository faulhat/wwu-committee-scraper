import React from 'react';
import CommitteeList from '../CommitteeList/CommitteeList';
import Footer from '../Footer/Footer';
import Subscription from '../Subscription/Subscription';
import { Toaster } from "react-hot-toast";
import './App.css';
import gif from '../../assets/oldmain.gif'; // Import the GIF
import img2 from '../../assets/img2.png'; // Import the left image
import img3 from '../../assets/aa.png'; // Import the first right image
import img4 from '../../assets/a.png'; // Import the second right image
import img5 from '../../assets/aaa.png'; // Import the third right image
import img6 from '../../assets/aaaa.png'; // Import the fourth right image

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
];

function App() {
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
      <Subscription />
      {/* Add the GIF here */}
      <div className="gif-container">
        <a rel="noopener noreferrer">
          <img src={gif} alt="Animation" className="gif" />
        </a>
      </div>
      <h2 className="committee-main-title">STUDENT COMMITTEES</h2>
      <CommitteeList committees={committees} />
      <Toaster position="top-center" reverseOrder={false} />
      <Footer />
    </div>
  );
}

export default App;