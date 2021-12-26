import React, {useState, useEffect}  from 'react';
import './WelcomeSection.css';
import '../App.css';
import Input from '@reactmaker/react-autocorrect-input';

var POTENTIALQUERIES = ['machine learning', 'cloud computing', 'computer architecture', 'natural language']

const renderResult = (item, i) => {
    let info = item.split(' ');
    let size = info.length;

    if(info[0] === 'error'){
        return(
            <fieldset>
                <li>
                    <p>{info.slice(1,size).join(' ')}</p>
                    </li>
            </fieldset>
                );
    }

    let course = JSON.parse(item);

    return(
        <fieldset>
        <legend><a href={'https://courses.sci.pitt.edu/courses/view/'+ String(course.department) + '-' + String(course.courseNumber)} > { String(course.department)+ ' ' + String(course.courseNumber)}</a></legend>
       <li key={i}> 
           <p>Course Title: {course.courseTitle}</p>
           <p>Description: </p>
           <p>{course.courseDescription}</p>
           </li>
       </fieldset>)
};

function WelcomeSection() {
    const [keywords, setKeywords] = useState("");
    const [results, setResult] = useState([]);
    const [querySearch, setQuerySearch] = useState(true);
    const [exactSearch, setExactSearch] = useState(false);

    const handleQuerySearch = async () => {
        try {
            const apiResponseObj = await fetch(
              "http://localhost:3001/query", {method:'POST', headers: {
                "Content-Type": "application/json",},
                body: JSON.stringify({terms: keywords})}
            );
            const apiResponse = await apiResponseObj.json();
            setResult(apiResponse.data);
          } catch (err) {
            console.log(err);
          }
    };

    const handleExactSearch = async() => {
        setResult([]);
        try {
            const apiResponseObj = await fetch(
              "http://localhost:3001/exact-search", {method:'POST', headers: {
                "Content-Type": "application/json",},
                body: JSON.stringify({terms: keywords})}
            );
            const apiResponse = await apiResponseObj.json();
            setResult(apiResponse.data);
          } catch (err) {
            console.log(err);
          }
    };

    return (
        <div className='welcome-container'>
            <video src='/videos/video-2.mp4' autoPlay loop muted/>
            <h1>Welcome!</h1>
            
            <div className='search-container' tabIndex='0' 
            onKeyDown={(event)=>{
                if(event.key === 'Enter'){
                    if(keywords.length > 0){
                        if(querySearch){
                            handleQuerySearch();
                        }else{
                            handleExactSearch();
                        }
                    }else{
                        setResult([]);
                    };
                }
            }}>

                <Input className="search-bar"
                onChange={value =>{setKeywords(value)}}
                value = {keywords}
                style={{width:'100%'}}
                dataSource = {POTENTIALQUERIES}
                />
            </div>

            <div className="options-container">
                <span class={ querySearch ? "dot-selected":"dot-unselected"} 
                onClick={()=>{setQuerySearch(true); setExactSearch(false)}} > </span>
                <p>Query Search</p>
                <span class={ exactSearch ? "dot-selected":"dot-unselected"} 
                onClick={()=>{setExactSearch(true); setQuerySearch(false)}}></span>
                <p>Exact Search</p>
            </div>

            <div className='display-window'>
                <ul className='result-container'>
                    {results.map((item, i) => renderResult(item, i))}
                </ul>
                
                {results.length === 0 && 
                <div className="default-message">
                    <p>
                    Thank you for using our course search system! 
                    </p>

                    <p>
                    Please select one of the search type before you start the search!
                    </p>

                </div>
                }
            </div>
        </div>

        
    )
}

export default WelcomeSection
