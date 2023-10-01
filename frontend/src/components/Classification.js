import {useRef, useState} from 'react';
import './Classification.css';

const Classification = () => {
  const [isFormSubmitted, setIsFormSubmitted] = useState(false);
  const [data, setData] = useState('');
  const queryInputRef = useRef();
  const methodInputRef = useRef();

  const formSubmissionHandler = async (event) => {
    event.preventDefault();
    const query = queryInputRef.current.value;
    const method = methodInputRef.current.value;
    const url = `http://127.0.0.1:8000/api/v1/health/classification/?method=${method}&query=${query}`;
    setIsFormSubmitted(true);
    const resultData = await fetchData(url);
    setData(resultData);
  };

  const fetchData = async (url) => {
    const response = await fetch(url);
    return await response.text();
  };

  return (
    <>
      <div className="classification-form_container">
          <form onSubmit={formSubmissionHandler}>
              <input ref={queryInputRef} type='text' id='fquery' name='fquery' placeholder='Enter query here'/>
              <label>Method</label>
              <select ref={methodInputRef} id="classification-method" name="method">
                  <option value="naive_bayes">Naive Bayes</option>
                  <option value="logistic_regression">Logistic Regression</option>
                  <option value="transformers">Transformers</option>
              </select>
              <button type='submit'>search</button>
          </form>
      </div>
      <div className='classificaion-result_container'>
          {isFormSubmitted && <span>{`این مطلب متعلق به دسته‌ی ${data} می‌باشد.`}</span>}
      </div>
    </>
  )
}

export default Classification;
