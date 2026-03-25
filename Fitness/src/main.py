import numpy as np
import pandas as pd
import questionary

from task import load_tasks,top_10_tasks,find_similar_task


def get_task_by_name(tasks,name):
    for task in tasks:
        if task['task_name'] == name:
            return task
    return None


def show_summary_task(selected_tasks):
    while True:
        print("\n ==== SELECTED TASKS ==== \n")
        for i,task in enumerate(selected_tasks):
            print(f"{i+1}. {task['task_name']} | {task['task_type']} | {task['difficulty']}")
                
        if not questionary.confirm("Do you want to delete any task?").ask():
            break
        
        remove_index = input("Enter task number to reamove: ").strip()
        
        if remove_index.isdigit():
            index = int(remove_index) - 1
            if 0 <= index < len(selected_tasks):
                removed = selected_tasks.pop(index)
                print(f"\n Removed: {removed['task_name']}\n")
            else:
                print("Invalid number\n")
        else:
            print("Please enter a valid number\n")
        
    return selected_tasks

def set_task_target(task):
    print("\n Set your target \n")
    name = task['task_name']
    task_type = task['task_type']
    print(f"\n{name}")

    if task_type == 'timed':
        default = task['avg_time_mins']
        user_input = input(f"How long? (deafult: {default} mins): ").strip()
        task['target_time']=int(user_input) if user_input.isdigit() else int(default)
    

    elif task_type == 'reps':
        default = task['default_amount']
        user_input = input(f"How many reps ? (deafult: {default}): ").strip()
        task['target_reps']=int(user_input) if user_input.isdigit() else int(default)

    elif task_type == 'flexible':
        unit = task['amount_unit']
        default_time = task['avg_time_mins']
        default_amount = task['default_amount']

        choice = questionary.select(
            f" Measured by: ",
            choices = ["Time (mins)",f"Amount ({unit})"]
        ).ask()

        if choice == 'Time (mins)':
            user_input = input(f"How long ? (deafult: {default_time} mins): ").strip()
            task['target_type'] = 'time'
            task['target_reps']=int(user_input) if user_input.isdigit() else int(default)
        else:
            user_input = input(f"How much ? (deafult: {default_amount}): ").strip()
            task['target_type'] = 'amount'
            task['target_amount']=float(user_input) if user_input else float(default)
            task['target_unit'] = unit

    elif task_type in ['completion','daily_habit']:
        print("No need the target")

    return task


def main():
    tasks = load_tasks()
    task_names= [row['task_name'] for row in tasks]
    selected_tasks = []

    print("\n==== Fitness Task =====\n")

    top_10_tasks()
    
    while(True):
        
        choices = task_names + ["[ Done ]"]
        selected_name = questionary.autocomplete(
            "Search task(type to filter) : ",
            choices=choices,
            match_middle = True
        ).ask()

        if not selected_name:
            print("please type")
            continue

        if selected_name is None or selected_name == "[ Done ]":
            break
        
        if selected_name in task_names:
            if selected_name in [t['task_name'] for t in selected_tasks]:
                print(f" Already added: {selected_name}\n")
                continue
            task = get_task_by_name(tasks, selected_name)
            selected_tasks.append(task)
            task = set_task_target(task)
            print(f"\n Added: {selected_name}\n")

        
        # Not found in dataset
        elif selected_name not in task_names:
            
            similar = find_similar_task(selected_name,tasks)
            
            if similar:
                confirm = questionary.confirm(
                    f"Do you mean: {similar['task_name']}?"
                ).ask()
                if confirm:
                    selected_tasks.append(similar)
                    task = set_task_target(similar)
                    print(f" Added: {similar['task_name']}")
            else:
                print("NO similar task found.")

        

        

        if not questionary.confirm("Add another?").ask():
            selected_tasks = show_summary_task(selected_tasks)
            break




if __name__ == "__main__":
    main()
