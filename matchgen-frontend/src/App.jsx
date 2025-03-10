import React from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { Button, Container, Typography, AppBar, Toolbar } from "@mui/material";
import LandingPage from "./pages/LandingPage";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import ClubManagement from "./pages/ClubManagement";
import Squad from "./pages/Squad";
import StartingXIPage from "./pages/StartingXI";
import { getToken, logout } from "./services/auth";

// Protect routes by checking authentication
const PrivateRoute = ({ element }) => {
  const isAuthenticated = !!getToken();
  return isAuthenticated ? element : <Navigate to="/login" />;
};

const App = () => {
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate("/login"); // Redirect to login after logout
  };

  return (
    <>
      {/* ✅ Material UI Navbar */}
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            MatchGen
          </Typography>
          <Button color="inherit" onClick={handleLogout}>
            Logout
          </Button>
        </Toolbar>
      </AppBar>

      {/* ✅ Main App Content */}
      <Container>
        <Routes>
          <Route path="/" element={<LandingPage />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<Signup />} />
          <Route path="/dashboard" element={<PrivateRoute element={<Dashboard />} />} />
          <Route path="/" element={<Navigate to="/login" />} />
          <Route path="/profile" element={<PrivateRoute element={<Profile />} />} />
          <Route path="/club" element={<PrivateRoute element={<ClubManagement />} />} />
          <Route path="/squad" element={<PrivateRoute element={<Squad />} />} />
          <Route path="/starting-xi" element={<PrivateRoute element={<StartingXIPage />} />} />
        </Routes>
      </Container>
    </>
  );
};

export default App;
