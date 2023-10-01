import './Evaluations.css';
import Images from '../Images';

const Evaluations = () => (
  <div className='evaluations_container'>
    <div className='evaluation-card'>
      <span className='evaluation-item'>Naive Bayes Method Evaluation</span>
      <img src={Images.naiveBayes} alt="naive bayes"></img>
    </div>
    <div className='evaluation-card'>
      <span className='evaluation-item'>Logistic Regression Method Evaluation</span>
      <img src={Images.logisticRegression} alt="logistic regression"></img>
    </div>
    <div className='evaluation-card'>
      <span className='evaluation-item'>Transformers Method Evaluation</span>
      <img src={Images.transformers} alt="transformers"></img>
    </div>
  </div>

);

export default Evaluations;
