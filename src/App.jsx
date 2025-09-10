
import './App.css';
import Header from './components/Header';
import MainContent from './components/MainContent';
import Footer from './components/Footer';
import TextAnalyzer from './components/TextAnalyzer';

function App() {
  return (
    <div className="app-container">
      <Header />
      <main className="main-content">
        <MainContent />
        <TextAnalyzer />
      </main>
      <Footer />
    </div>
  );
}

export default App;
