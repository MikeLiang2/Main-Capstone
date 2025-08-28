export interface AvatarPrompt {
  prompt: string;
  style: "natural" | "vivid";
}

export interface URLResponse {
  url: string;
}

export interface ApproveRequest {
  temp_url: string;
}
