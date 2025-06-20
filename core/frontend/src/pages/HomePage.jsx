import "./HomePage.css";
import NewsWidget from "../components/NewsWidget";
import TrainersWidget from "../components/TrainersWidget";
import HorsesWidget from "../components/HorsesWidget";

export default function HomePage() {
  return (
    <>
      <div className="hero-section">
        <div className="container">
            <h1 className="main-title">Добро пожаловать в конный клуб "Аллюр"</h1>
            <p className="intro-text">
              Место, где любовь к лошадям и страсть к верховой езде становятся одним целым.
            </p>
            <button className="cta-button">Узнать больше</button>
        </div>
      </div>

      <div className="container page-section">
        <NewsWidget />
      </div>

      <div className="container page-section">
        <TrainersWidget />
      </div>

      <div className="container page-section">
        <HorsesWidget />
      </div>
    </>
  );
}
