import React, { useState, useEffect, useMemo } from "react";
import { Link } from "react-router-dom";
import {
  Box,
  Button,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  TextField,
  Typography,
  InputAdornment,
  IconButton,
  TableSortLabel,
} from "@mui/material";
import SearchIcon from "@mui/icons-material/Search";
import AddIcon from "@mui/icons-material/Add";
import { Incident, NewIncidentPayload } from "../types/incident";
import { getIncidents, createIncident } from "../services/api";

const IncidentList: React.FC = () => {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState<boolean>(false);
  const [searchTerm, setSearchTerm] = useState<string>("");
  const [sortBy, setSortBy] = useState<keyof Incident>("id");
  const [sortDirection, setSortDirection] = useState<"asc" | "desc">("desc");

  const [newIncident, setNewIncident] = useState<NewIncidentPayload>({
    description: "",
    actions_taken: "",
  });

  const fetchIncidents = async () => {
    try {
      setLoading(true);
      const data = await getIncidents();
      setIncidents(data);
      setError(null);
    } catch (err) {
      setError("Failed to fetch incidents");
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchIncidents();
  }, []);

  const handleCreate = async () => {
    try {
      await createIncident(newIncident);
      setOpenDialog(false);
      setNewIncident({ description: "", actions_taken: "" });
      fetchIncidents();
    } catch (err) {
      setError("Failed to create incident");
      console.error(err);
    }
  };

  const handleSort = (property: keyof Incident) => {
    const isAsc = sortBy === property && sortDirection === "asc";
    setSortDirection(isAsc ? "desc" : "asc");
    setSortBy(property);
  };

  const filteredIncidents = useMemo(() => {
    return incidents
      .filter(
        (incident) =>
          incident.description
            .toLowerCase()
            .includes(searchTerm.toLowerCase()) ||
          incident.id.toString().includes(searchTerm) ||
          incident.status.toLowerCase().includes(searchTerm.toLowerCase()),
      )
      .sort((a, b) => {
        const aValue = a[sortBy];
        const bValue = b[sortBy];

        if (typeof aValue === "string" && typeof bValue === "string") {
          return sortDirection === "asc"
            ? aValue.localeCompare(bValue)
            : bValue.localeCompare(aValue);
        }

        if (aValue !== undefined && bValue !== undefined) {
          return sortDirection === "asc"
            ? aValue < bValue
              ? -1
              : 1
            : bValue < aValue
              ? -1
              : 1;
        }

        return 0;
      });
  }, [incidents, searchTerm, sortBy, sortDirection]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case "OPEN":
        return "#f44336";
      case "IN_PROGRESS":
        return "#ff9800";
      case "CLOSED":
        return "#4caf50";
      default:
        return "inherit";
    }
  };

  if (loading && incidents.length === 0) {
    return <Typography>Loading incidents...</Typography>;
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box
        sx={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          mb: 3,
        }}
      >
        <Typography variant="h4">Incident Management</Typography>
        <Button
          variant="contained"
          color="primary"
          startIcon={<AddIcon />}
          onClick={() => setOpenDialog(true)}
        >
          New Incident
        </Button>
      </Box>

      <TextField
        fullWidth
        margin="normal"
        placeholder="Search incidents..."
        variant="outlined"
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        InputProps={{
          startAdornment: (
            <InputAdornment position="start">
              <SearchIcon />
            </InputAdornment>
          ),
        }}
        sx={{ mb: 3 }}
      />

      <TableContainer component={Paper} sx={{ mb: 3 }}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>
                <TableSortLabel
                  active={sortBy === "id"}
                  direction={sortBy === "id" ? sortDirection : "asc"}
                  onClick={() => handleSort("id")}
                >
                  Incident ID
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={sortBy === "description"}
                  direction={sortBy === "description" ? sortDirection : "asc"}
                  onClick={() => handleSort("description")}
                >
                  Description
                </TableSortLabel>
              </TableCell>
              <TableCell>
                <TableSortLabel
                  active={sortBy === "status"}
                  direction={sortBy === "status" ? sortDirection : "asc"}
                  onClick={() => handleSort("status")}
                >
                  Status
                </TableSortLabel>
              </TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredIncidents.length > 0 ? (
              filteredIncidents.map((incident) => (
                <TableRow key={incident.id}>
                  <TableCell>
                    <Link
                      to={`/incidents/${incident.id}`}
                      style={{ textDecoration: "none", color: "#1976d2" }}
                    >
                      INC-{incident.id.toString().padStart(6, "0")}
                    </Link>
                  </TableCell>
                  <TableCell>{incident.description}</TableCell>
                  <TableCell>
                    <Box
                      sx={{
                        display: "inline-block",
                        px: 1,
                        py: 0.5,
                        borderRadius: "4px",
                        bgcolor: getStatusColor(incident.status),
                        color: "white",
                        fontWeight: "bold",
                      }}
                    >
                      {incident.status}
                    </Box>
                  </TableCell>
                </TableRow>
              ))
            ) : (
              <TableRow>
                <TableCell colSpan={3} align="center">
                  {error ? `Error: ${error}` : "No incidents found"}
                </TableCell>
              </TableRow>
            )}
          </TableBody>
        </Table>
      </TableContainer>

      <Dialog
        open={openDialog}
        onClose={() => setOpenDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Create New Incident</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Description"
            fullWidth
            variant="outlined"
            value={newIncident.description}
            onChange={(e) =>
              setNewIncident({ ...newIncident, description: e.target.value })
            }
            required
          />
          <TextField
            margin="dense"
            label="Actions Taken"
            fullWidth
            variant="outlined"
            multiline
            rows={4}
            value={newIncident.actions_taken}
            onChange={(e) =>
              setNewIncident({ ...newIncident, actions_taken: e.target.value })
            }
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button
            onClick={handleCreate}
            variant="contained"
            color="primary"
            disabled={!newIncident.description || !newIncident.actions_taken}
          >
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default IncidentList;
