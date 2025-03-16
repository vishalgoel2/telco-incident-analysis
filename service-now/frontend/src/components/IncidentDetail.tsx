import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Paper,
  Typography,
  Grid,
  Divider,
  TextField,
  CircularProgress,
  Card,
  CardContent,
} from "@mui/material";
import ArrowBackIcon from "@mui/icons-material/ArrowBack";
import EditIcon from "@mui/icons-material/Edit";
import {
  Incident,
  IncidentStatus,
  UpdateIncidentPayload,
} from "../types/incident";
import { getIncidentById, updateIncident } from "../services/api";

const IncidentDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();

  const [incident, setIncident] = useState<Incident | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [isEditing, setIsEditing] = useState<boolean>(false);
  const [updates, setUpdates] = useState<UpdateIncidentPayload>({});

  useEffect(() => {
    const fetchIncident = async () => {
      if (!id) return;
      try {
        setLoading(true);
        const data = await getIncidentById(parseInt(id));
        setIncident(data);
        setUpdates({
          rca: data.rca || "",
          resolution: data.resolution || "",
        });
      } catch (err) {
        setError("Failed to fetch incident details");
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchIncident();
  }, [id]);

  const handleSave = async () => {
    if (!incident || !id) return;

    try {
      const updatedIncident = await updateIncident(parseInt(id), updates);
      setIncident(updatedIncident);
      setIsEditing(false);
    } catch (err) {
      setError("Failed to update incident");
      console.error(err);
    }
  };

  const handleAccept = async () => {
    if (!incident || !id) return;

    try {
      const updatedIncident = await updateIncident(parseInt(id), {
        status: IncidentStatus.CLOSED,
      });
      setIncident(updatedIncident);
    } catch (err) {
      setError("Failed to close incident");
      console.error(err);
    }
  };

  const handleStatusUpdate = async (status: IncidentStatus) => {
    if (!incident || !id) return;

    try {
      const updatedIncident = await updateIncident(parseInt(id), { status });
      setIncident(updatedIncident);
    } catch (err) {
      setError(`Failed to update status to ${status}`);
      console.error(err);
    }
  };

  if (loading) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <CircularProgress />
      </Box>
    );
  }

  if (error || !incident) {
    return (
      <Box
        display="flex"
        justifyContent="center"
        alignItems="center"
        minHeight="80vh"
      >
        <Typography color="error">{error || "Incident not found"}</Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Box
        sx={{
          mb: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
        }}
      >
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate("/")}>
          Back to List
        </Button>
        <Typography variant="h5">
          Incident INC-{incident.id.toString().padStart(6, "0")}
        </Typography>
        <Box>
          {incident.status === IncidentStatus.OPEN && (
            <Button
              variant="contained"
              color="primary"
              onClick={() => handleStatusUpdate(IncidentStatus.IN_PROGRESS)}
              sx={{ mr: 1 }}
            >
              Move to In Progress
            </Button>
          )}
        </Box>
      </Box>

      <Paper sx={{ p: 3, mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Incident Details
        </Typography>
        <Divider sx={{ mb: 2 }} />

        <Grid container spacing={2}>
          <Grid item xs={12} md={6}>
            <Typography variant="subtitle2">Status</Typography>
            <Box
              sx={{
                display: "inline-block",
                px: 1,
                py: 0.5,
                borderRadius: "4px",
                bgcolor:
                  incident.status === IncidentStatus.OPEN
                    ? "#f44336"
                    : incident.status === IncidentStatus.IN_PROGRESS
                      ? "#ff9800"
                      : "#4caf50",
                color: "white",
                fontWeight: "bold",
                mt: 1,
                mb: 2,
              }}
            >
              {incident.status}
            </Box>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle2">Description</Typography>
            <Card variant="outlined" sx={{ mt: 1, mb: 2 }}>
              <CardContent>
                <Typography variant="body1">{incident.description}</Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12}>
            <Typography variant="subtitle2">Actions Taken</Typography>
            <Card variant="outlined" sx={{ mt: 1, mb: 2 }}>
              <CardContent>
                <Typography variant="body1" sx={{ whiteSpace: "pre-line" }}>
                  {incident.actions_taken}
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          {(incident.status === IncidentStatus.IN_PROGRESS ||
            incident.status === IncidentStatus.CLOSED) && (
            <>
              <Grid item xs={12}>
                <Typography variant="subtitle2">Root Cause Analysis</Typography>
                {isEditing ? (
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    variant="outlined"
                    value={updates.rca || ""}
                    onChange={(e) =>
                      setUpdates({ ...updates, rca: e.target.value })
                    }
                    sx={{ mt: 1, mb: 2 }}
                  />
                ) : (
                  <Card variant="outlined" sx={{ mt: 1, mb: 2 }}>
                    <CardContent>
                      <Typography
                        variant="body1"
                        sx={{ whiteSpace: "pre-line" }}
                      >
                        {incident.rca || "No RCA provided yet."}
                      </Typography>
                    </CardContent>
                  </Card>
                )}
              </Grid>

              <Grid item xs={12}>
                <Typography variant="subtitle2">Resolution</Typography>
                {isEditing ? (
                  <TextField
                    fullWidth
                    multiline
                    rows={4}
                    variant="outlined"
                    value={updates.resolution || ""}
                    onChange={(e) =>
                      setUpdates({ ...updates, resolution: e.target.value })
                    }
                    sx={{ mt: 1, mb: 2 }}
                  />
                ) : (
                  <Card variant="outlined" sx={{ mt: 1, mb: 2 }}>
                    <CardContent>
                      <Typography
                        variant="body1"
                        sx={{ whiteSpace: "pre-line" }}
                      >
                        {incident.resolution || "No resolution provided yet."}
                      </Typography>
                    </CardContent>
                  </Card>
                )}
              </Grid>
            </>
          )}
        </Grid>
      </Paper>

      {incident.status === IncidentStatus.IN_PROGRESS && (
        <Box sx={{ display: "flex", justifyContent: "flex-end", gap: 2 }}>
          {isEditing ? (
            <>
              <Button variant="outlined" onClick={() => setIsEditing(false)}>
                Cancel
              </Button>
              <Button variant="contained" color="primary" onClick={handleSave}>
                Save Changes
              </Button>
            </>
          ) : (
            <>
              <Button
                variant="outlined"
                startIcon={<EditIcon />}
                onClick={() => setIsEditing(true)}
              >
                Edit
              </Button>
              <Button
                variant="contained"
                color="success"
                onClick={handleAccept}
                disabled={!incident.rca || !incident.resolution}
              >
                Accept & Close
              </Button>
            </>
          )}
        </Box>
      )}
    </Box>
  );
};

export default IncidentDetail;
