﻿import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

function Shop() {
  return (
    <div className="page">
      <h1>Shop Page</h1>
      <Link to="/machines">View Machines</Link>
    </div>
  );
}

export default Shop;
