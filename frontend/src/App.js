import { useEffect, useState } from "react";
import "./App.css";
import Sidebar from "./components/Sidebar";
import InformationRetrieval from "./components/InformationRetrieval";
import Classification from "./components/Classification";
import Evaluations from "./components/Evaluations";
import Clustering from "./components/Clustering";
import ClusteringEvaluation from "./components/ClusteringEvaluation";
import LinkAnalysis from "./components/LinkAnalysis";

function App() {
  const [item, setItem] = useState(0);
  const [isClassificationSelected, setIsClassificationSelected] =
    useState(false);
  const [isClusteringSelected, setIsClusteringSelected] = useState(false);

  const setSideBarItemHandler = (item) => {
    setItem(item);
  };

  const renderSwitch = (param) => {
    switch (param) {
      case 1:
        return <InformationRetrieval />;
      case 2.1:
        return <Classification />;
      case 2.2:
        return <Evaluations />;
      case 3.1:
        return <Clustering />;
      case 3.2:
        return <ClusteringEvaluation />;
      case 4:
        return <LinkAnalysis />;
      default:
        return <></>;
    }
  };

  useEffect(() => {
    if (item === 2 || item === 2.1 || item === 2.2) {
      setIsClassificationSelected(true);
      setIsClusteringSelected(false)
    }
    else if (item === 3 || item === 3.1 || item === 3.2) {
      setIsClassificationSelected(false)
      setIsClusteringSelected(true)
    }
    else {
      setIsClassificationSelected(false)
      setIsClusteringSelected(false)
    }
  }, [item]);

  return (
    <div className="page_container">
      <Sidebar
        setItemHandler={setSideBarItemHandler}
        isClassificationSelected={isClassificationSelected}
        isClusteringSelected={isClusteringSelected}
      />
      <div className="main_container">{renderSwitch(item)}</div>
    </div>
  );
}

export default App;
