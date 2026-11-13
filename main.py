
from dataclasses import dataclass
from drafter import *


# OPTIONS
DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday",
        "Friday", "Saturday", "Sunday"]

GOALS = ["Build Muscle", "Lose Weight",
         "Improve Endurance", "Stay Fit"]

MUSCLE_GROUPS = ["Arms", "Legs", "Chest",
                 "Back", "Abs", "Full Body"]


@dataclass
class Workout:
    name: str
    muscle_group: str
    duration: int
    day: str
    completed: bool = False


@dataclass
class State:
    user_name: str
    fitness_goal: str
    available_days: list[str]
    weekly_goal: int
    workouts: list[Workout]


@route
def index(state: State) -> Page:
    return Page(state, [
        Header("Workout Planner"),
        "Plan. Track. Improve.",
        "Welcome to your personal workout planner!",
        Button("Set Up Profile", "profile"),
        Button("View Workouts", "view_workouts"),
        Button("View Progress", "progress")
    ])


@route
def profile(state: State) -> Page:
    return Page(state, [
        Header("Create Your Profile"),
        "Enter your name:",
        TextBox("user_name"),
        "Choose your fitness goal:",
        SelectBox("fitness_goal", GOALS),
        "Choose an available workout day:",
        SelectBox("available_day", DAYS),
        "Weekly workout goal (1-7):",
        TextBox("weekly_goal"),
        Button("Save Profile", "save_profile"),
        Button("Home", "index")
    ])


@route
def save_profile(state: State, user_name: str,
                 fitness_goal: str, available_day: str,
                 weekly_goal: int) -> Page:

    if user_name.strip() == "":
        return Page(state, [
            Header("Name Required"),
            "Please enter your name.",
            Button("Back to Profile", "profile")
        ])

    if weekly_goal < 1 or weekly_goal > 7:
        return Page(state, [
            Header("Invalid Goal"),
            "Enter a weekly goal between 1 and 7.",
            Button("Back to Profile", "profile")
        ])

    state.user_name = user_name
    state.fitness_goal = fitness_goal
    state.available_days = [available_day]
    state.weekly_goal = weekly_goal

    return Page(state, [
        Header("Profile Saved!"),
        "Your profile has been saved.",
        Button("Home", "index"),
        Button("Create Workout", "new_workout")
    ])


@route
def new_workout(state: State) -> Page:
    return Page(state, [
        Header("Create a Workout"),
        "Workout name:",
        TextBox("name"),
        "Choose a muscle group:",
        SelectBox("muscle_group", MUSCLE_GROUPS),
        "Workout duration in minutes:",
        TextBox("duration"),
        "Choose a workout day:",
        SelectBox("day", DAYS),
        Button("Add Workout", "add_workout"),
        Button("Back to Workouts", "view_workouts")
    ])


@route
def add_workout(state: State, name: str,
                muscle_group: str, duration: int,
                day: str) -> Page:

    if name.strip() == "":
        return Page(state, [
            Header("Workout Name Required"),
            "Please enter a workout name.",
            Button("Try Again", "new_workout")
        ])

    if duration <= 0:
        return Page(state, [
            Header("Invalid Duration"),
            "Enter a duration greater than zero.",
            Button("Try Again", "new_workout")
        ])

    workout = Workout(
        name,
        muscle_group,
        duration,
        day,
        False
    )

    state.workouts.append(workout)

    return view_workouts(state)


@route
def view_workouts(state: State) -> Page:

    content = [Header("Your Workouts")]

    if len(state.workouts) == 0:
        content.append("You have no workouts yet!")

    else:
        for index, workout in enumerate(state.workouts):

            if workout.completed:
                status = "Completed"
            else:
                status = "Not Completed"

            content.append(
                workout.name + " | "
                + workout.muscle_group + " | "
                + str(workout.duration) + " minutes | "
                + workout.day + " | " + status
            )

            if not workout.completed:
                content.append(
                    Button(
                        "Mark Complete",
                        "complete_workout",
                        [Argument("workout_index", index)]
                    )
                )

            content.append(
                Button(
                    "Delete Workout",
                    "delete_workout",
                    [Argument("workout_index", index)]
                )
            )

    content.extend([
        Button("Add New Workout", "new_workout"),
        Button("View Progress", "progress"),
        Button("Home", "index")
    ])

    return Page(state, content)


@route
def complete_workout(state: State,
                     workout_index: int) -> Page:

    if 0 <= workout_index < len(state.workouts):
        state.workouts[workout_index].completed = True

    return view_workouts(state)


@route
def progress(state: State) -> Page:

    completed_count = 0
    total_minutes = 0

    for workout in state.workouts:
        if workout.completed:
            completed_count += 1
            total_minutes += workout.duration

    if completed_count >= state.weekly_goal:
        message = "Congratulations! You reached your weekly goal!"
    else:
        remaining = state.weekly_goal - completed_count
        message = (
            "You need " + str(remaining)
            + " more workouts to reach your goal."
        )

    return Page(state, [
        Header("Your Fitness Progress"),
        "Name: " + state.user_name,
        "Fitness Goal: " + state.fitness_goal,
        "Completed Workouts: " + str(completed_count),
        "Total Workout Time: " + str(total_minutes) + " minutes",
        "Weekly Goal: " + str(state.weekly_goal),
        message,
        Button("View Workouts", "view_workouts"),
        Button("Home", "index")
    ])


@route
def delete_workout(state: State,
                   workout_index: int) -> Page:

    if 0 <= workout_index < len(state.workouts):
        state.workouts.pop(workout_index)

    return view_workouts(state)


if __name__ == "__main__":
    start_server(State("", "", [], 3, []))
