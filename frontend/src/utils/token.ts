// local storage token management utility functions
// This file provides functions to set, get, and remove a token from local storage.

// It is used to manage user authentication tokens in the application.
export const SET_TOKEN = (token: string) => {
    localStorage.setItem('token', token);
}

// Retrieves the token from local storage
export const GET_TOKEN = () => {
    return localStorage.getItem('token');
}

// Removes the token from local storage
export const REMOVE_TOKEN = () => {
    localStorage.removeItem('token');
}
