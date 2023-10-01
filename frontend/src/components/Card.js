import './Card.css';

const Card = ({ title, url }) => (
    <div className='card_container'>
      <a href={url}>{title}</a>
    </div>
);

export default Card;