# RPS.py - Rock Paper Scissors Bot

def player(prev_play, opponent_history=[]):
    """
    Rock Paper Scissors player function that adapts to different opponent strategies.
    Uses multiple approaches to defeat various bots.
    """
    
    # Store opponent's move history
    if prev_play != "":
        opponent_history.append(prev_play)
    
    # For the first move, play Rock
    if len(opponent_history) == 0:
        return "R"
    
    # Counter moves: what beats what
    counter_moves = {"R": "P", "P": "S", "S": "R"}
    
    # Strategy 1: Frequency Analysis
    # Count frequency of opponent moves
    if len(opponent_history) >= 3:
        r_count = opponent_history.count("R")
        p_count = opponent_history.count("P")
        s_count = opponent_history.count("S")
        
        # Predict most frequent move
        if r_count > p_count and r_count > s_count:
            freq_prediction = "R"
        elif p_count > s_count:
            freq_prediction = "P"
        else:
            freq_prediction = "S"
    else:
        freq_prediction = opponent_history[-1]
    
    # Strategy 2: Pattern Matching (look for sequences)
    pattern_prediction = None
    if len(opponent_history) >= 10:
        # Look for patterns of length 3-5
        for pattern_length in range(3, min(6, len(opponent_history))):
            recent_pattern = opponent_history[-pattern_length:]
            
            # Find if this pattern occurred before
            for i in range(len(opponent_history) - pattern_length - 1):
                if opponent_history[i:i+pattern_length] == recent_pattern:
                    # Found pattern, predict next move
                    pattern_prediction = opponent_history[i + pattern_length]
                    break
            
            if pattern_prediction:
                break
    
    # Strategy 3: Anti-frequency (counter their least used move)
    anti_freq_prediction = None
    if len(opponent_history) >= 5:
        r_count = opponent_history[-10:].count("R") if len(opponent_history) >= 10 else opponent_history.count("R")
        p_count = opponent_history[-10:].count("P") if len(opponent_history) >= 10 else opponent_history.count("P")
        s_count = opponent_history[-10:].count("S") if len(opponent_history) >= 10 else opponent_history.count("S")
        
        # Predict they'll use their least used move
        if r_count <= p_count and r_count <= s_count:
            anti_freq_prediction = "R"
        elif p_count <= s_count:
            anti_freq_prediction = "P"
        else:
            anti_freq_prediction = "S"
    
    # Strategy 4: Markov Chain (predict based on last move)
    markov_prediction = None
    if len(opponent_history) >= 2:
        last_move = opponent_history[-1]
        
        # Count what usually follows the last move
        transitions = {"R": {"R": 0, "P": 0, "S": 0},
                      "P": {"R": 0, "P": 0, "S": 0},
                      "S": {"R": 0, "P": 0, "S": 0}}
        
        for i in range(len(opponent_history) - 1):
            current = opponent_history[i]
            next_move = opponent_history[i + 1]
            transitions[current][next_move] += 1
        
        # Predict most likely next move after last_move
        if sum(transitions[last_move].values()) > 0:
            max_count = max(transitions[last_move].values())
            for move, count in transitions[last_move].items():
                if count == max_count:
                    markov_prediction = move
                    break
    
    # Strategy 5: Recent trend analysis
    trend_prediction = None
    if len(opponent_history) >= 5:
        recent_moves = opponent_history[-5:]
        r_recent = recent_moves.count("R")
        p_recent = recent_moves.count("P")
        s_recent = recent_moves.count("S")
        
        if r_recent > p_recent and r_recent > s_recent:
            trend_prediction = "R"
        elif p_recent > s_recent:
            trend_prediction = "P"
        else:
            trend_prediction = "S"
    
    # Combine strategies with voting
    predictions = []
    
    if pattern_prediction:
        predictions.extend([pattern_prediction] * 3)  # Weight pattern matching heavily
    
    if markov_prediction:
        predictions.extend([markov_prediction] * 2)  # Weight Markov chain
    
    predictions.append(freq_prediction)
    
    if anti_freq_prediction:
        predictions.append(anti_freq_prediction)
    
    if trend_prediction:
        predictions.append(trend_prediction)
    
    # Vote for most common prediction
    if predictions:
        r_votes = predictions.count("R")
        p_votes = predictions.count("P")
        s_votes = predictions.count("S")
        
        if r_votes > p_votes and r_votes > s_votes:
            predicted_move = "R"
        elif p_votes > s_votes:
            predicted_move = "P"
        else:
            predicted_move = "S"
    else:
        predicted_move = opponent_history[-1]
    
    # Return the counter to our prediction
    return counter_moves[predicted_move]


# Test function to help debug
def test_player():
    """Simple test function"""
    history = []
    
    # Simulate some moves
    moves = ["R", "P", "S", "R", "P", "S", "R", "R", "P"]
    
    print("Testing player function:")
    prev = ""
    for move in moves:
        response = player(prev, history)
        print(f"Opponent played: {move if move else 'None'}, We play: {response}")
        prev = move

if __name__ == "__main__":
    test_player()