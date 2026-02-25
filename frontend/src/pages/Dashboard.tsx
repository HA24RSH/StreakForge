import { useEffect, useState } from "react";
import { Habit } from "../types/habit";
import { getHabits, logHabit, deleteHabit } from "../api/habits";
import HabitForm from "../components/HabitForm";

const Dashboard = () => {
  const [habits, setHabits] = useState<Habit[]>([]);
  const [loading, setLoading] = useState(true);
  const [loggingIds, setLoggingIds] = useState<Set<string>>(new Set());
  const [loggedTodayIds, setLoggedTodayIds] = useState<Set<string>>(new Set());

  const fetchHabits = async () => {
    try {
      const data = await getHabits();
      setHabits(data);
    } catch (error) {
      console.error("Error fetching habits:", error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHabits();
  }, []);

  const handleLogToday = async (habitId: string) => {
    try {
      setLoggingIds((prev) => new Set(prev).add(habitId));

      await logHabit(habitId);

      // Update streak locally without full refetch
      setHabits((prev) =>
        prev.map((h) =>
          h.id === habitId ? { ...h, current_streak: h.current_streak + 1 } : h,
        ),
      );

      setLoggedTodayIds((prev) => new Set(prev).add(habitId));
    } catch (error) {
      // Duplicate log
      setLoggedTodayIds((prev) => new Set(prev).add(habitId));
    } finally {
      setLoggingIds((prev) => {
        const updated = new Set(prev);
        updated.delete(habitId);
        return updated;
      });
    }
  };

  const handleDelete = async (habitId: string) => {
    try {
      await deleteHabit(habitId);
      setHabits((prev) => prev.filter((h) => h.id !== habitId));
    } catch (error) {
      console.error("Error deleting habit:", error);
    }
  };

  if (loading) return <p>Loading...</p>;
  if (!habits) return <p>Something went wrong.</p>;

  return (
    <div className="container">
      <h1 className="title">Habit Dashboard</h1>

      <HabitForm onHabitCreated={fetchHabits} />

      {habits.length === 0 ? (
        <p>No habits yet.</p>
      ) : (
        habits.map((habit) => {
          const isLogging = loggingIds.has(habit.id);
          const loggedToday = loggedTodayIds.has(habit.id);

          const streakClass =
            habit.current_streak === 0
              ? "low"
              : habit.current_streak < 7
                ? "medium"
                : "high";

          return (
            <div key={habit.id} className="card">
              <h3>{habit.name}</h3>
              {habit.description && <p>{habit.description}</p>}

              <div className={`streak ${streakClass}`}>
                🔥 Streak: {habit.current_streak}
              </div>

              <div style={{ marginTop: "12px" }}>
                <button
                  className="button primary"
                  onClick={() => handleLogToday(habit.id)}
                  disabled={isLogging || loggedToday}
                >
                  {loggedToday
                    ? "Logged Today ✅"
                    : isLogging
                      ? "Logging..."
                      : "Log Today"}
                </button>

                <button
                  className="button danger"
                  onClick={() => handleDelete(habit.id)}
                >
                  Delete
                </button>
              </div>
            </div>
          );
        })
      )}
    </div>
  );
};

export default Dashboard;
