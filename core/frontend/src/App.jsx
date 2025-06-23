import { BrowserRouter, Routes, Route } from "react-router-dom";
import Header from "./components/Header";
import Footer from "./components/Footer";
import HomePage from "./pages/HomePage";
import NewsListPage from "./pages/NewsListPage";
import FilterDemo from "./components/FilterDemo";
import AfExamPage from "./pages/AfExamPage";
import "./App.css";

function App() {
  return (
    <div className="app-wrapper">
      <BrowserRouter>
        <Header />
        <main className="main-content">
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/news" element={<NewsListPage />} />
            <Route path="/filters" element={<FilterDemo />} />
            <Route path="/afexam" element={<AfExamPage />} />
          </Routes>
        </main>
        <Footer />
      </BrowserRouter>
    </div>
  );
}

export default App;
