export enum IncidentStatus {
  OPEN = "OPEN",
  IN_PROGRESS = "IN_PROGRESS",
  CLOSED = "CLOSED",
}

export interface Incident {
  id: number;
  description: string;
  actions_taken: string;
  rca?: string;
  resolution?: string;
  status: IncidentStatus;
}

export interface NewIncidentPayload {
  description: string;
  actions_taken: string;
}

export interface UpdateIncidentPayload {
  rca?: string;
  resolution?: string;
  status?: IncidentStatus;
}
