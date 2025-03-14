import React from "react";
import { Routes, Route, Navigate, useNavigate } from "react-router-dom";
import { Button, Container, Typography, AppBar, Toolbar } from "@mui/material";
import AppAppBar from './components/AppAppBar';
import LandingPage from "./pages/LandingPage";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Dashboard from "./pages/Dashboard";
import Profile from "./pages/Profile";
import ClubManagement from "./pages/ClubManagement";
import Squad from "./pages/Squad";

import MarketingPage from "./pages/MarketingPage";
import SquadManagement from "./pages/SquadManagement";
import SelectTeamGen from "./pages/SelectTeamGen";
import { getToken, logout } from "./services/auth";

const isAuthenticated = !!getToken(); // Checks if token exists

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

    {!isAuthenticated && <AppAppBar />} {/* Hide AppBar if user is logged in */}

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
          <Route path="/marketingpage" element={<MarketingPage />} />
          <Route path="/SquadManagement" element={<SquadManagement />} />
          <Route path="/SelectTeamGen" element={<SelectTeamGen />} />
        </Routes>
      </Container>
    </>
  );
};

export default App;

{/*        */}{/* ✅ Material UI Navbar */}
{/*       <AppBar position="static"> */}
{/*         <Toolbar> */}
{/*           <Typography variant="h6" sx={{ flexGrow: 1 }}> */}
{/*             MatchGen */}
{/*           </Typography> */}
{/*           <Button color="inherit" onClick={handleLogout}> */}
{/*             Logout */}
{/*           </Button> */}
{/*         </Toolbar> */}
{/*       </AppBar> */}