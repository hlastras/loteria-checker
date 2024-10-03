import sys
import re

def parse_input_file(input_file):
    """
    Parse the input.txt file to extract predictions per column for each match.
    """
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    # Remove empty lines and strip whitespace
    lines = [line.strip() for line in lines if line.strip()]

    if not lines:
        print("Error: The input.txt file is empty.")
        sys.exit(1)

    # The first line contains the column headers (bets)
    header = lines[0]
    # Extract column numbers using regex
    columns = re.findall(r'\d+', header)
    num_columns = len(columns)

    predictions = {}  # key: match number, value: list of predictions per column

    for line in lines[1:]:
        # Split the line by tabs
        parts = line.split('\t')
        if not parts:
            continue

        # Extract the match number
        match_num_str = parts[0]
        match_num_match = re.match(r'^(?:P-)?(\d+)\.', match_num_str)
        if not match_num_match:
            continue  # Skip lines that do not correspond to matches

        match_num = int(match_num_match.group(1))

        # Extract the teams
        if len(parts) < 2:
            print(f"Warning: Match {match_num} lacks team information.")
            continue
        teams = parts[1].strip()

        # Extract the predictions
        if match_num == 15:
            # Special case: single prediction shared across all bets
            if len(parts) < 3:
                print(f"Warning: Match {match_num} lacks a prediction.")
                continue
            shared_pred = parts[2].strip()
            predictions[match_num] = [shared_pred] * num_columns
        else:
            # Predictions per column
            preds = parts[2:2+num_columns]
            if len(preds) < num_columns:
                print(f"Warning: Match {match_num} has {len(preds)} predictions, expected {num_columns}.")
            # Fill missing predictions with empty strings
            while len(preds) < num_columns:
                preds.append('')
            predictions[match_num] = preds[:num_columns]

    return columns, predictions

def parse_result_file(result_file):
    """
    Parse the result.txt file to extract actual results per match.
    Returns a dictionary with match number as key and actual outcome as value.
    """
    with open(result_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    actual_results = {}

    # Determine the format based on the content
    # If lines alternate between match info and result, it's double line format
    # Otherwise, it's single line format
    if len(lines) >= 2 and re.match(r'^(?:P-)?\d+\.', lines[0]):
        # Double line format
        i = 0
        while i < len(lines):
            match_line = lines[i]
            result_line = lines[i+1] if i+1 < len(lines) else ''
            # Extract match number
            match_num_match = re.match(r'^(?:P-)?(\d+)\.', match_line)
            if not match_num_match:
                i += 1
                continue
            match_num = int(match_num_match.group(1))
            # Extract the result
            result = result_line.strip()
            # Validate if the result is valid or if the match hasn't been played yet
            if re.match(r'^[1X2Mm\-]+$', result, re.IGNORECASE) or '-' in result:
                actual_results[match_num] = result
            else:
                # Match has not been played yet
                actual_results[match_num] = None
            i += 2
    else:
        # Single line format
        # This format is not well-defined in the examples, so it may need extension if necessary
        print("Warning: The result.txt format is not fully recognized. Attempting to process available data.")
        for line in lines[1:]:
            # Match lines like "1.	Barcelona - Young Boys	5 - 0	1"
            match = re.match(r'^(?:P-)?(\d+)\.\s+[^\t]+\t+[\d\-:]+\t+([1X2Mm\-]+)', line)
            if not match:
                # Could be an unplayed match with date and time
                continue
            match_num = int(match.group(1))
            result = match.group(2).strip()
            actual_results[match_num] = result

    return actual_results

def calculate_aciertos(columns, predictions, actual_results):
    """
    Compare predictions with actual results and calculate hits per column.
    Returns:
        - counts: list with number of hits per column
        - table: list of tuples (match_num, list indicating 'x' or '')
    """
    num_columns = len(columns)
    counts = [0] * num_columns
    table = []  # Each element is (match_num, [x or ''])

    for match_num in sorted(predictions.keys()):
        pred_list = predictions[match_num]
        actual = actual_results.get(match_num, None)
        row = []
        for i in range(num_columns):
            if actual is None:
                # Match has not been played yet
                row.append('')
                continue
            pred = pred_list[i].upper()
            actual_upper = actual.upper()
            if '-' in actual:
                # For match 15 with exact result prediction
                # The prediction must match exactly
                if pred == actual_upper:
                    counts[i] += 1
                    row.append('x')
                else:
                    row.append('')
            else:
                # For matches 1-14, compare 1, X, 2, M
                if pred == actual_upper:
                    counts[i] += 1
                    row.append('x')
                else:
                    row.append('')
        table.append((match_num, row))

    return counts, table

def format_output(columns, counts, table, input_file):
    """
    Format and print the output as specified.
    """
    # Print hit counts
    for i, count in enumerate(counts):
        print(f"Bet {columns[i]}: {count} hits")
    print()

    # Prepare the table
    # Retrieve match information from input.txt
    with open(input_file, 'r', encoding='utf-8') as f:
        lines = f.readlines()

    lines = [line.strip() for line in lines if line.strip()]
    match_info = {}
    for line in lines[1:]:
        parts = line.split('\t')
        if not parts:
            continue
        match_num_str = parts[0]
        match_num_match = re.match(r'^(?:P-)?(\d+)\.', match_num_str)
        if not match_num_match:
            continue
        match_num = int(match_num_match.group(1))
        if len(parts) < 2:
            teams = 'Unknown Teams'
        else:
            teams = parts[1].strip()
        match_info[match_num] = teams

    # Determine column widths for formatting
    match_num_width = max(len(str(m)) for m in match_info.keys()) + 1
    team_width = max(len(team) for team in match_info.values()) + 2
    column_width = 3  # Fixed width for bet columns

    # Table header
    header = f"{'No.':<{match_num_width}} {'Teams':<{team_width}} " + " ".join([f"{col:<{column_width}}" for col in columns])
    print(header)
    print('-' * len(header))

    # Table rows
    for match_num, preds in table:
        teams = match_info.get(match_num, 'Unknown Teams')
        row = f"{match_num:<{match_num_width}} {teams:<{team_width}} " + " ".join([f"{p:<{column_width}}" for p in preds])
        print(row)

def main():
    if len(sys.argv) != 3:
        print("Usage: python quiniela.py input.txt result.txt")
        sys.exit(1)

    input_file = sys.argv[1]
    result_file = sys.argv[2]

    columns, predictions = parse_input_file(input_file)
    actual_results = parse_result_file(result_file)
    counts, table = calculate_aciertos(columns, predictions, actual_results)
    format_output(columns, counts, table, input_file)

if __name__ == "__main__":
    main()
