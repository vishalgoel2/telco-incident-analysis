import React from "react";
import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import {
  ThemeProvider,
  createTheme,
  CssBaseline,
  Container,
  Box,
} from "@mui/material";
import IncidentList from "./components/IncidentList";
import IncidentDetail from "./components/IncidentDetail";

const theme = createTheme({
  palette: {
    mode: "light",
    primary: {
      main: "#1976d2",
    },
    secondary: {
      main: "#dc004e",
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 700,
    },
  },
  components: {
    MuiButton: {
      styleOverrides: {
        root: {
          textTransform: "none",
        },
      },
    },
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box sx={{ my: 4 }}>
          <BrowserRouter>
            <Routes>
              <Route path="/" element={<IncidentList />} />
              <Route path="/incidents/:id" element={<IncidentDetail />} />
              <Route path="*" element={<Navigate to="/" />} />
            </Routes>
          </BrowserRouter>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
