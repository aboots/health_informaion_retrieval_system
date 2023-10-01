import { useEffect, useState } from "react";
import "./ClusteringEvaluation.css";
import Images from "../Images";

const ClusteringEvaluation = () => {
  const [data, setData] = useState({});

  useEffect(() => {
    const fetchData = async () => {
      const response = await fetch(
        "http://127.0.0.1:8000/api/v1/health/clustering_result/"
      );
      const json = await response.json();
      setData(json);
    };
    fetchData();
  }, []);

  return (
    <div className="clustering_container">
      <div className="clustering-results_container">
        <h3 className="clustering-results_title">
          Clustering evaluation results are as shown below:
        </h3>
        {Object.keys(data).map((item) => (
          <span
            key={item}
            className="clustering-items"
          >{`${item}: ${data[item]}`}</span>
        ))}
      </div>
      <div className="clustering-image_container">
        <span className="clustering-image_title">Kmeans Clustering PCA Result</span>
        <img src={Images.kmeansClustering} alt="kmeans PCA"></img>
      </div>
      <div className="clustering-image_container">
        <span className="clustering-image_title">Real Clustering PCA Result</span>
        <img src={Images.realClustering} alt="real PCA"></img>
      </div>
    </div>
  );
};

export default ClusteringEvaluation;
