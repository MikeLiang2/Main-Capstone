import request from "@/utils/request";
import type { AvatarPrompt, URLResponse, ApproveRequest } from "./type";

// Generate a new avatar
export function generateAvatar(data: AvatarPrompt) {
  return request<URLResponse>({
    url: "/avatar/generate",
    method: "post",
    data
  });
}

// Approve the generated avatar (store permanently)
export function approveAvatar(data: ApproveRequest) {
  return request<URLResponse>({
    url: "/avatar/approve",
    method: "post",
    data
  });
}
