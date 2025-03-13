﻿import React from "react";
import { Link } from "react-router-dom";
import "../styles.css";

function Login() {
  return (
    <div className="page">
      <h1>Login Page</h1>
      <Link to="/shop">Go to Shop</Link>
    </div>
  );
}

export default Login;
