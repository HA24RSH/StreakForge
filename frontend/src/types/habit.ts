export interface Habit {
  id: string;
  name: string;
  description?: string;
  current_streak: number;
}