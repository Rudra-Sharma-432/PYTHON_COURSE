import json
import os

# Forces the file to be saved in the exact same directory as this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
FILE_PATH = os.path.join(SCRIPT_DIR, "data.jsonl")

def addMove(state, action):
    """Appends a new training step instantly to the file."""
    with open(FILE_PATH, "a") as f:
        # Save as a single-line dictionary. Structure is perfectly preserved.
        line = json.dumps({"state": state, "action": action})
        f.write(line + "\n")

def clear_data():
    """Completely wipes the data file to start a fresh batch."""
    with open(FILE_PATH, "w") as f:
        pass  # Opening in 'w' mode instantly empties the file
    print("Training data file cleared successfully!")


def get_training_data():
    """Extracts all data cleanly as Python lists for your Neural Network."""
    states = []
    actions = []
    
    if not os.path.exists(FILE_PATH):
        return states, actions
        
    with open(FILE_PATH, "r") as f:
        for line in f:
            if line.strip(): 
                data = json.loads(line)
                states.append(data["state"])
                actions.append(data["action"])
                
    return states, actions

# --- Example Usage for Verification ---
if __name__ == "__main__":
    # 1. Simulate saving game steps
    state_sample = [1, 0, 0, 0, 4, 0, 0, 0, 2, 0, 1, 0, 8, 1, 1, 0]
    action_sample = [0, 1, 0, 0]
    
    addMove(state_sample, action_sample)
    print(f"Successfully saved move to: {FILE_PATH}")
    
    # 2. Extract data directly for your Neural Network
    X_train, y_train = get_training_data()
    
    print("\n--- Extracted Data for Training ---")
    print("States Array (X_train):", X_train)
    print("Actions Array (y_train):", y_train)
