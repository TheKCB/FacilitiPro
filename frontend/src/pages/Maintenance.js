﻿import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

function Maintenance() {
  return (
    <div className="page">
      <h1>Maintenance Page</h1>
      <Link to="/">Back to Login</Link>
    </div>
  );
}

export default Maintenance;
