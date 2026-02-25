import axios from "axios";
import { Habit } from "../types/habit";

const API = axios.create({
  baseURL: process.env.REACT_APP_API_URL,
});

export const getHabits = async (): Promise<Habit[]> => {
  const response = await API.get("/habits");
  return response.data;
};

export const createHabit = async (name: string) => {
  const response = await API.post("/habits", { name });
  return response.data;
};

export const logHabit = async (habitId: string) => {
  const today = new Date().toISOString().split("T")[0];

  const response = await API.post(`/habits/${habitId}/log`, {
    date: today,
  });

  return response.data;
};

export const deleteHabit = async (habitId: string) => {
  await API.delete(`/habits/${habitId}`);
};