import { createTheme } from "@mui/material/styles";

const theme = createTheme({
  palette: {
    primary: {
      main: "#1976d2", // Change this to your brand color
    },
    secondary: {
      main: "#ff4081",
    },
  },
  typography: {
    fontFamily: "Arial, sans-serif",
  },
});

export default theme;
