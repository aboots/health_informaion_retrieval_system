import {useRef, useState} from 'react';
import './InformationRetrieval.css';
import Card from './Card';

// const DOMMY_DATA = [
//   {
//       "title": "دندان عقل و کشیدن آن خوب است یا بد؟",
//       "url": "https://namnak.com/کشیدن-دندان-عقل.p39551"
//   },
//   {
//       title: "پر کردن دندان بدون نیاز به دندانپزشک",
//       url: "https://namnak.com/پر-کردن-دندان.p29166"
//   },
//   {
//       title: "هر چیزی که باید درباره دندان عقل بدانید",
//       url: "https://www.hidoctor.ir/357156_%d9%87%d8%b1-%da%86%db%8c%d8%b2%db%8c-%da%a9%d9%87-%d8%a8%d8%a7%db%8c%d8%af-%d8%af%d8%b1%d8%a8%d8%a7%d8%b1%d9%87-%d8%af%d9%86%d8%af%d8%a7%d9%86-%d8%b9%d9%82%d9%84-%d8%a8%d8%af%d8%a7%d9%86%db%8c%d8%af.html/"
//   },
//   {
//       title: "این افراد بیشتر مراقب پوسیدگی دندان باشند!",
//       url: "https://namnak.com/پوسیدگی-دندان.p143"
//   },
//   {
//       title: "علت اصلی انواع درد و مشکلات دندان و لثه",
//       url: "https://namnak.com/مشکل-دندان.p51702"
//   },
//   {
//       title: "عوارض وحشتناک هر یک دندان پوسیده",
//       url: "https://namnak.com/عوارض-دندان-پوسیده.p17882"
//   },
//   {
//       title: "این درد و حالت در دندان شما یعنی عصب کشی لازم دارید",
//       url: "https://namnak.com/عصب-کشی-دندان.p9578"
//   },
//   {
//       title: "علائم حساسیت عاج دندان و درمان آن",
//       url: "https://namnak.com/حساسیت-عاج-دندان.p41805"
//   },
//   {
//       title: "درمان آسان دندان‌های حساس",
//       url: "https://www.hidoctor.ir/356749_%d8%af%d8%b1%d9%85%d8%a7%d9%86-%d8%a2%d8%b3%d8%a7%d9%86-%d8%af%d9%86%d8%af%d8%a7%d9%86-%d9%87%d8%a7%db%8c-%d8%ad%d8%b3%d8%a7%d8%b3.html/"
//   },
//   {
//       title: "هیولای وحشتناک روی دندان پوسیده را از نزدیک ببینید + تصاویر",
//       url: "https://namnak.com/هیولای-وحشتناک-روی-دندان-پوسیده.p26187"
//   }
// ];

const InformationRetrieval = () => {
    const [isFormSubmitted, setIsFormSubmitted] = useState(false);
    const [data, setData] = useState([]);
    const queryInputRef = useRef();
    const methodInputRef = useRef();
    const numberInputRef = useRef();
    const checkboxInputRef = useRef();

    const formSubmissionHandler = async (event) => {
        event.preventDefault();
        const query = queryInputRef.current.value;
        const method = methodInputRef.current.value;
        const k = numberInputRef.current.value || 10;
        const checkboxIsChecked = checkboxInputRef.current.checked;
        const url = `http://127.0.0.1:8000/api/v1/health/query_retrieval/?method=${method}&query=${query}&k=${k}&query_expansion=${checkboxIsChecked}`;
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
                    <label>Method</label>
                    <select ref={methodInputRef} id="method" name="method">
                        <option value="fasttext">fasttext</option>
                        <option value="transformers">transformers</option>
                        <option value="boolean">boolean</option>
                        <option value="tfidf">tfidf</option>
                        <option value="elastic">elastic</option>
                    </select>
                    <label>Number of results</label>
                    <input ref={numberInputRef} type='number'/>
                    <label className='query-expansion-content'>
                        <input ref={checkboxInputRef} type="checkbox" id="expansion" defaultChecked /> Use query expansion
                    </label>
                    <button type='submit'>search</button>
                </form>
            </div>
            <div className='cards_container'>
                {isFormSubmitted && data.map((item, index) => <Card key={index} title={item.title} url={item.url}/>)}
            </div>
        </>
    )

};

export default InformationRetrieval;
