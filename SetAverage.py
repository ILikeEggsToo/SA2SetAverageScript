""" try:
    import pyperclip
except ImportError:
    pyperclip = None """
pyperclip = None


def main():
    # get character and extra loadless time
    splitsCount = getSplitsCount()
    extraLoadlessTime = get_extra_loadless_time()

    # continually ask user for goal times and calculate timestamps
    while True:
        print()
        goalTime = get_goal_time()
        levelTime = calculate_level_time(goalTime, splitsCount, extraLoadlessTime)
        splitTimestampsSeconds = generate_timestamps_seconds(
            levelTime, splitsCount, extraLoadlessTime
        )
        splitTimestampsFormatted = format_timestamps(splitTimestampsSeconds)
        print_and_copy_timestamps(splitTimestampsFormatted)


def getSplitsCount() -> int:
    """
    Asks the user to enter the character (Knuckles or Rouge) and returns the corresponding splits count.

    Returns:
        int: The splits count based on the user's input.
    """
    while True:
        character = input("Enter 1 for Knuckles (x20) or 2 for Rouge (x25): ")
        if character == "1":
            return 20
        elif character == "2":
            return 25
        else:
            print("Invalid input. Please try again.")


def get_extra_loadless_time() -> float:
    """
    Asks the user to enter the average extra loadless time per split and returns it as a float.

    Returns:
        float: The average extra loadless time per split.
    """
    extraLoadlessTime = input(
        "Enter average extra loadless time per split (default is 14.5): "
    )
    if extraLoadlessTime == "":
        extraLoadlessTime = 14.5
    else:
        extraLoadlessTime = float(extraLoadlessTime)
    return extraLoadlessTime


def get_goal_time() -> float:
    """
    Asks the user to enter the goal time in mm:ss format and returns it as a float in seconds.

    Returns:
        float: The goal time in seconds.
    """
    while True:
        goalTimeInput = input("Enter goal time in mm:ss format: ")
        try:
            # convert to float and check if valid
            goalTimeMinutes, goalTimeSeconds = map(float, goalTimeInput.split(":"))
            if 0 <= goalTimeSeconds < 60 and goalTimeMinutes >= 0:
                return goalTimeMinutes * 60 + goalTimeSeconds  # convert to seconds
            else:
                raise ValueError()
        except ValueError:
            print("Invalid input. Please enter time in mm:ss format.")


def calculate_level_time(
    goalTime: float, splitsCount: int, extraLoadlessTime: float
) -> float:
    """
    Calculates the average level time based on the goal time, splits count, and extra loadless time.

    Args:
        goalTime (float): The goal time in seconds.
        splitsCount (int): The number of splits.
        extraLoadlessTime (float): The average extra loadless time per split.

    Returns:
        float: The average level time.
    """
    levelTime = (goalTime - extraLoadlessTime * (splitsCount - 1)) / splitsCount
    print(f"Average level time is {levelTime:.2f} seconds.")
    return levelTime


def generate_timestamps_seconds(
    levelTime: float, splitsCount: int, extraLoadlessTime: float
) -> list[float]:
    """
    Generates a list of split timestamps in seconds based on the level time, splits count, and extra loadless time.

    Args:
        levelTime (float): The average level time.
        splitsCount (int): The number of splits.
        extraLoadlessTime (float): The average extra loadless time per split.

    Returns:
        list[float]: The list of split timestamps in seconds.
    """
    splitTimestampsSeconds = [levelTime]
    for i in range(2, splitsCount + 1):
        splitTimestampsSeconds.append(levelTime * i + extraLoadlessTime * (i - 1))
    return splitTimestampsSeconds


def format_timestamps(splitTimestampsSeconds: list[float]) -> list[str]:
    """
    Formats the split timestamps in seconds to mm:ss format.

    Args:
        splitTimestampsSeconds (list[float]): The list of split timestamps in seconds.

    Returns:
        list[str]: The list of split timestamps formatted as mm:ss.
    """
    splitTimestampsFormatted = []
    for timestamp in splitTimestampsSeconds:
        minutes, seconds = divmod(timestamp, 60)
        splitTimestampsFormatted.append(f"{int(minutes):02d}:{seconds:05.2f}")
    return splitTimestampsFormatted


def print_and_copy_timestamps(splitTimestampsFormatted: list[str]):
    """
    Prints the split timestamps and copies them to the clipboard if pyperclip is installed.

    Args:
        splitTimestampsFormatted (list[str]): The list of split timestamps formatted as mm:ss.
    """
    finalText = "\n".join(splitTimestampsFormatted)
    print(f"\n{finalText}")
    if pyperclip:
        print("\nCopied to clipboard")
        pyperclip.copy(finalText)
    else:
        print("\nmodule pyperclip not installed, text not copied to clipboard")


if __name__ == "__main__":
    main()
