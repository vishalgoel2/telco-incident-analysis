import axios from "axios";
import {
  Incident,
  NewIncidentPayload,
  UpdateIncidentPayload,
} from "../types/incident";

const API_URL = "http://localhost:8000";

const api = axios.create({
  baseURL: API_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

export const getIncidents = async (): Promise<Incident[]> => {
  const response = await api.get<Incident[]>("/incidents");
  return response.data;
};

export const getIncidentById = async (id: number): Promise<Incident> => {
  const response = await api.get<Incident>(`/incidents/${id}`);
  return response.data;
};

export const createIncident = async (
  incident: NewIncidentPayload,
): Promise<Incident> => {
  const response = await api.post<Incident>("/incidents", incident);
  return response.data;
};

export const updateIncident = async (
  id: number,
  data: UpdateIncidentPayload,
): Promise<Incident> => {
  const response = await api.put<Incident>(`/incidents/${id}`, data);
  return response.data;
};
