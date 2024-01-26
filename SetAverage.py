try:
    import pyperclip
except ImportError:
    pyperclip = None

from math import isclose


def main():
    # get character and extra loadless time
    splitsCount = getSplitsCount()
    extraLoadlessTime = getExtraLoadlessTime()
    menuingSplits = getMenuingSplits()

    # continually ask user for goal times and calculate timestamps
    while True:
        print()
        goalTime = getGoalTime()
        levelTime = calculateLevelTime(goalTime, splitsCount, extraLoadlessTime)
        splitTimestampsSeconds = generateTimestampsSeconds(
            levelTime, goalTime, extraLoadlessTime, menuingSplits
        )
        splitTimestampsFormatted = formatTimestamps(splitTimestampsSeconds)
        printAndCopyTimestamps(splitTimestampsFormatted)


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


def getExtraLoadlessTime() -> float:
    """
    Asks the user to enter the average extra loadless time per split and returns it as a float.

    Returns:
        float: The average extra loadless time per split.
    """
    while True:
        try:
            extraLoadlessTime = input(
                "Enter average extra loadless time per split (default is 14.5): "
            )
            if extraLoadlessTime == "":
                extraLoadlessTime = 14.5
            else:
                extraLoadlessTime = float(extraLoadlessTime)
            break
        except ValueError:
            print("Invalid input. Please try again.")
    return extraLoadlessTime


def getMenuingSplits() -> bool:
    """
    Asks the user if they want to include menuing splits and returns True if yes, False if no.

    Returns:
        bool: True if the user wants to include menuing splits, False if not.
    """
    while True:
        menuingSplits = input(
            "Do you have separate menuing splits? Press 1 or n for no, press 2 or y for yes: "
        )
        if menuingSplits == "1" or menuingSplits == "n":
            return False
        elif menuingSplits == "2" or menuingSplits == "y":
            return True
        else:
            print("Invalid input. Please try again.")


def getGoalTime() -> float:
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


def calculateLevelTime(
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


def generateTimestampsSeconds(
    levelTime: float,
    goalTime: float,
    extraLoadlessTime: float,
    menuingSplits: bool = False,
) -> list[float]:
    """
    Generates a list of split timestamps in seconds based on the level time, goal time, extra loadless time, and menuing splits.

    Args:
        levelTime (float): The average level time.
        goalTime (float): The goal time in seconds.
        extraLoadlessTime (float): The average extra loadless time per split.
        menuingSplits (bool, optional): Whether to include menuing splits. Defaults to False.

    Returns:
        list[float]: The list of split timestamps in seconds.
    """
    splitTimestampsSeconds = [levelTime]
    time = levelTime
    # use isclose to avoid funny floating point rounding errors
    while not isclose(time, goalTime):
        time += extraLoadlessTime
        if menuingSplits:
            splitTimestampsSeconds.append(time)
        time += levelTime
        splitTimestampsSeconds.append(time)

    return splitTimestampsSeconds


def formatTimestamps(splitTimestampsSeconds: list[float]) -> list[str]:
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


def printAndCopyTimestamps(splitTimestampsFormatted: list[str]):
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
