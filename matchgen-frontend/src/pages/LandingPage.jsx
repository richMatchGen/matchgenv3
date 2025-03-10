import React from "react";
import { AppBar, Toolbar, Typography, Button, Container, Grid, Card, CardContent, Box,Paper } from "@mui/material";

const LandingPage = () => {
  return (
    <>
      {/* Navbar */}
      <AppBar position="static" sx={{ bgcolor: "#1976d2" }}>
        <Toolbar>

          <Typography variant="h6" sx={{ flexGrow: 1 }}>MatchGen</Typography>
          <Button color="inherit">Login</Button>
        </Toolbar>
      </AppBar>

      {/* Hero Section */}
      <Box
        sx={{
          bgcolor: "#f5f5f5",
          textAlign: "center",
          py: 8,
          px: 2
        }}
      >
        <Typography variant="h3" gutterBottom>
          The Future of Sports Marketing
        </Typography>
        <Typography variant="h6" color="textSecondary" paragraph>
          Connect with fans, grow your brand, and revolutionize sports engagement.
        </Typography>
        <Button variant="contained" color="primary" size="large">
          Get Started
        </Button>
      </Box>

      {/* Features Section */}
      <Container sx={{ py: 6 }}>
        <Typography variant="h4" align="center" gutterBottom>
          Why Choose MatchGen?
        </Typography>
        <Grid container spacing={3}>
          {["AI-Powered Analytics", "Social Media Growth", "Real-Time Engagement"].map((feature, index) => (
            <Grid item xs={12} md={4} key={index}>
              <Paper sx={{ p: 3, textAlign: "center" }} elevation={3}>
                <Typography variant="h6">{feature}</Typography>
                <Typography variant="body2" color="textSecondary">
                  Lorem ipsum dolor sit amet, consectetur adipiscing elit.
                </Typography>
              </Paper>
            </Grid>
          ))}
        </Grid>
      </Container>

      {/* CTA Section */}
      <Box sx={{ bgcolor: "#1976d2", color: "#fff", textAlign: "center", py: 6 }}>
        <Typography variant="h4" gutterBottom>Join Us Today</Typography>
        <Typography variant="body1">
          Take your sports brand to the next level with MatchGen.
        </Typography>
        <Button variant="contained" color="secondary" size="large" sx={{ mt: 2 }}>
          Sign Up Now
        </Button>
      </Box>
    </>
  );
}

export default LandingPage;
