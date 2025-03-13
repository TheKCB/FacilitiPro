﻿import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

function Machines() {
  return (
    <div className="page">
      <h1>Machines Page</h1>
      <Link to="/maintenance">Go to Maintenance</Link>
    </div>
  );
}

export default Machines;
