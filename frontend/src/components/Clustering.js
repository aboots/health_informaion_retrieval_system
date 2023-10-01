import {useRef, useState} from 'react';
import './InformationRetrieval.css';
import Card from './Card';

// const DOMMY_DATA = [
//     {
//         title: "روزهایی که زنان متاهل و مجرد میل جنسی بیشتری دارند",
//         url: "https://namnak.com/میل-جنسی-زنان.p30848"
//     },
//     {
//         title: "وظیفه ی مهم مردان در بهبود رابطه جنسی",
//         url: "https://namnak.com/وظیفه-مردان-در-رابطه-جنسی.p29854"
//     },
//     {
//         title: "انواع زود انزالی مردان و راههای درمان انزال زودرس",
//         url: "https://namnak.com/زود-انزالی.p65437"
//     },
//     {
//         title: "عکس العمل های متفاوت زن و مرد بعد از رابطه جنسی",
//         url: "https://namnak.com/عکس-العمل-بعد-از-رابطه-جنسی.p35728"
//     }
// ];

const Clustering = () => {
    const [isFormSubmitted, setIsFormSubmitted] = useState(false);
    const [data, setData] = useState([]);
    const queryInputRef = useRef();
    const numberInputRef = useRef();

    const formSubmissionHandler = async (event) => {
        event.preventDefault();
        const query = queryInputRef.current.value;
        const k = numberInputRef.current.value || 10;
        const url = `http://127.0.0.1:8000/api/v1/health/clustering/?query=${query}&k=${k}`;
        setIsFormSubmitted(true);
        const resultData = await fetchData(url);
        setData(resultData);
    };

    const fetchData = async (url) => {
        const response = await fetch(url);
        return await response.json();
    };

    return (
        <>
            <div className="form_container">
                <form onSubmit={formSubmissionHandler}>
                    <input ref={queryInputRef} type='text' id='fquery' name='fquery' placeholder='Enter query here'/>
                    <label>Number of results</label>
                    <input ref={numberInputRef} type='number'/>
                    <button type='submit'>search</button>
                </form>
            </div>
            <div className="cards_container">
                {isFormSubmitted && data.map((item, index) => <Card key={index} title={item.title} url={item.url}/>)}
            </div>
        </>
    )

};

export default Clustering;
