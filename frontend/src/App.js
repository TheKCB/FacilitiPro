import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Login from "./pages/Login";
import Shop from "./pages/Shop";
import Machines from "./pages/Machines";
import Maintenance from "./pages/Maintenance";
import "./styles.css";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/shop" element={<Shop />} />
        <Route path="/areas/:areaId/machines" element={<Machines />} />
        <Route path="/machines/:machineId/maintenance" element={<Maintenance />} />
      </Routes>
    </Router>
  );
}

export default App;
