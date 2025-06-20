import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./TrainersWidget.css";

export default function TrainersWidget() {
  const [trainers, setTrainers] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/trainers/")
      .then((response) => response.json())
      .then((data) => {
        // Show 3 random trainers
        const trainersData = data.results || [];
        const shuffled = trainersData.sort(() => 0.5 - Math.random());
        setTrainers(shuffled.slice(0, 3));
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching trainers:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="trainers-widget">
      <div className="widget-title-container">
        <h2 className="widget-title">Наши тренеры</h2>
      </div>
      {loading ? (
        <div>Загрузка тренеров...</div>
      ) : (
        <>
          <div className="trainers-list">
            {trainers.map((trainer) => (
              <div key={trainer.id} className="trainer-card">
                <img src={trainer.photo} alt={trainer.last_name} className="trainer-photo" />
                <div className="trainer-info">
                  <h3>{trainer.full_name}</h3>
                  <p>Опыт: {trainer.experience_years} лет</p>
                </div>
              </div>
            ))}
          </div>
          <div className="all-trainers-link-container">
            <Link to="/trainers" className="button">Вся команда</Link>
          </div>
        </>
      )}
    </div>
  );
} 