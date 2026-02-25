import { useState } from "react";
import { createHabit } from "../api/habits";

interface Props {
  onHabitCreated: () => void;
}

const HabitForm = ({ onHabitCreated }: Props) => {
  const [name, setName] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

    if (!name.trim()) return;

    try {
      await createHabit(name);
      setName("");
      onHabitCreated();
    } catch (error) {
      console.error("Error creating habit:", error);
    }
  };

  return (
    <form
      onSubmit={handleSubmit}
      style={{
        display: "flex",
        gap: "12px",
        marginBottom: "25px",
        alignItems: "center",
      }}
    >
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="Enter habit name..."
        className="input"
        style={{ flex: 1 }}
      />

      <button type="submit" className="button primary">
        Add Habit
      </button>
    </form>
  );
};

export default HabitForm;
