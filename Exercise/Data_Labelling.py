import re
import pandas as pd


# Function to extract exercise details from a block of text
def extract_exercise_details(data_block):
    exercise_name = re.search(r"Exercise Name:\s*(.*)", data_block).group(1)

    main_muscle_group = ", ".join(
        re.findall(
            r"Shoulders|Back|Chest|Biceps|Abs|Triceps|Forearms|Glutes|Upper Legs|Lower Legs|Cardio|Core",
            data_block,
        )
    )

    exercise_types_block = (
        re.search(r"Exercise Types:\s*(.*)", data_block, re.DOTALL).group(1).strip()
    )
    experience_level = re.search(
        r"(Beginner|Intermediate|Advanced)", exercise_types_block
    ).group(1)
    focus_type = ", ".join(
        re.findall(r"Strength|Endurance|Compound|Isolation", exercise_types_block)
    )

    equipment = re.search(r"Equipment:\s*(.*)", data_block).group(1).strip()

    description_full = (
        re.search(r"How-to Instructions:\s*(.*)", data_block, re.DOTALL)
        .group(1)
        .strip()
    )

    description = re.split(r"\.|here's a step", description_full, flags=re.IGNORECASE)[
        0
    ].strip()
    if "Steps" in description:
        description = "No Description"

    if "Steps" in description_full:
        tutorial = re.findall(r"\d+\.\)\s*(.*)", description_full)
    else:
        tutorial = re.findall(
            r":\s*([^:]*?)\s*\.", description_full.replace("\n", " ").replace("\r", " ")
        )

    return {
        "Exercise Name": exercise_name,
        "Main Muscle Groups": main_muscle_group,
        "Experience Level": experience_level,
        "Focus Type": focus_type,
        "Equipment": equipment,
        "Description": description,
        "Tutorial": tutorial,
    }


# Function to process the entire text file and extract all exercises
def process_scraped_data(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        lines = file.readlines()

    filtered_lines = [line for line in lines if not re.search(r"http[s]?://\S+", line)]

    # Join the filtered lines back into a single string
    data = "".join(filtered_lines)
    # Split the data based on "Data for___"
    exercise_blocks = re.split(
        r"Exercise Name", data[1:]
    )  # Skip the first split if it doesn't contain exercise data

    exercises = []

    for block in exercise_blocks:
        block = (
            "Exercise Name" + block
        )  # Add back the "Data for" to each block to maintain consistency
        # print(block)
        try:
            exercise_details = extract_exercise_details(block)
            exercises.append(exercise_details)
        except Exception as e:
            print(f"Error processing exercise block: {e}")

    return exercises


file_path = "scraped_data.txt"
extracted_data = process_scraped_data(file_path)
df = pd.DataFrame(extracted_data)
df = df.map(lambda x: tuple(x) if isinstance(x, list) else x)

df = df.drop_duplicates()
df.to_csv("fitness_exercises.csv", index=False)
print("Data has been successfully saved to fitness_exercises.csv")
