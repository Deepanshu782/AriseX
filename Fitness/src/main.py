import csv
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


def main():
    path = "/home/deepanshu/Documents/coding/python/AriseX/dataset/fitness_tasks.csv"
    tasks = load_tasks(path)
    task_names= [row['task_name'] for row in tasks]
    selected_tasks = []

    print("\n==== Fitness Task =====\n")

    top_10_tasks(path)
    
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
                    print(f" Added: {similar['task_name']}")
            else:
                print("NO similar task found.")

        

        

        if not questionary.confirm("Add another?").ask():
            selected_tasks = show_summary_task(selected_tasks)
            break




if __name__ == "__main__":
    main()
