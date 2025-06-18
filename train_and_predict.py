import csv

def load_csv(file):
    with open(file, 'r') as f:
        reader = csv.reader(f)
        next(reader)
        return [row[1] for row in reader]

def match_pattern(history, target_pattern, min_matches=18):
    for i in range(len(history) - 20):
        segment = history[i:i+20]
        matches = sum(1 for a, b in zip(segment, target_pattern) if a == b)
        if matches >= min_matches:
            return segment[-1]  # Next prediction
    return None

if __name__ == "__main__":
    history = load_csv("10000_data.csv")  # Your full history
    target_pattern = load_csv("wingo_live_data.csv")[-20:]  # Last 20 real-time
    prediction = match_pattern(history, target_pattern)
    print("🧠 Prediction:", prediction or "No strong match found")
