import './Sidebar.css';

const Sidebar = ({ setItemHandler, isClassificationSelected, isClusteringSelected }) => {
  return (
    <div className='sidebar'>
        <div className='sidebar_item' onClick={() => {setItemHandler(1)}}>
          Information Retrieval
        </div>
        <div className='sidebar_item' onClick={() => {setItemHandler(2)}}>
          Classification
        </div>
        {isClassificationSelected && (
          <>
            <div className='sidebar_subitem' onClick={() => {setItemHandler(2.1)}}>Classification Retrieval</div>
            <div className='sidebar_subitem' onClick={() => {setItemHandler(2.2)}}>Classification Methods Evaluation</div>
          </>
        )}
        <div className='sidebar_item' onClick={() => {setItemHandler(3)}}>
          Clustering
        </div>
        {isClusteringSelected && (
          <>
            <div className='sidebar_subitem' onClick={() => {setItemHandler(3.1)}}>Clustering Retrieval</div>
            <div className='sidebar_subitem' onClick={() => {setItemHandler(3.2)}}>Clustering Evaluation Results</div>
          </>
        )}
        <div className='sidebar_item' onClick={() => {setItemHandler(4)}}>
          Link Analysis
        </div>

      </div>
  )

}
export default Sidebar;
