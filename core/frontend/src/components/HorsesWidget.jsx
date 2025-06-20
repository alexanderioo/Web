import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import "./HorsesWidget.css";

export default function HorsesWidget() {
  const [horses, setHorses] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetch("http://localhost:8000/api/horses/")
      .then((response) => response.json())
      .then((data) => {
        // Show 4 random horses
        const horsesData = data.results || [];
        const shuffled = horsesData.sort(() => 0.5 - Math.random());
        setHorses(shuffled.slice(0, 4));
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching horses:", error);
        setLoading(false);
      });
  }, []);

  return (
    <div className="horses-widget">
        <div className="widget-title-container">
            <h2 className="widget-title">Наши лошади</h2>
        </div>
      {loading ? (
        <div>Загрузка лошадей...</div>
      ) : (
        <>
            <div className="horses-list">
                {horses.map((horse) => (
                <div key={horse.id} className="horse-card">
                    <img src={horse.photo} alt={horse.name} className="horse-photo" />
                    <div className="horse-info">
                        <h3>{horse.name}</h3>
                        <p>{horse.gender === 'male' ? 'Жеребец' : 'Кобыла'}</p>
                    </div>
                </div>
                ))}
            </div>
            <div className="all-horses-link-container">
                <Link to="/horses" className="button">Все лошади</Link>
            </div>
        </>
      )}
    </div>
  );
} 