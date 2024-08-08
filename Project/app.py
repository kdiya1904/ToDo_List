from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Initialize the todo list with a tuple of (task, completed, subtasks)
todo_list = []


@app.route('/')
def index():
    """Render the main page with the current todo list."""
    # Prepare the todo list with indices
    tasks_with_index = [(index, task) for index, task in enumerate(todo_list)]
    return render_template('index.html', todo_list=tasks_with_index)

@app.route('/remove/<int:task_num>', methods=['POST'])
def remove_task(task_num):
    """Remove a task from the todo list by its index."""
    if 0 <= task_num < len(todo_list):
        todo_list.pop(task_num)
    return redirect(url_for('index'))

@app.route('/add', methods=['POST'])
def add_task():
    """Add a task to the todo list."""
    task = request.form.get('task')
    if task:
        todo_list.append((task, False, []))  # Assuming a tuple with task, completed status, and subtasks
    return redirect(url_for('index'))


@app.route('/toggle/<int:task_num>')
def toggle_task(task_num):
    """Toggle the completion status of a task."""
    if 0 <= task_num < len(todo_list):
        task, completed, subtasks = todo_list[task_num]
        if not completed:
            # Mark the task as completed
            todo_list[task_num] = (task, True, subtasks)
        else:
            # If the task is already completed, remove it
            todo_list.pop(task_num)
            print(f"Removed completed task: '{task}'")
    return redirect(url_for('index'))


@app.route('/view/<int:task_num>', methods=['GET', 'POST'])
def view_task(task_num):
    """View a specific task and its subtasks, and add subtasks."""
    if request.method == 'POST':
        subtask = request.form.get('subtask')
        if subtask:
            todo_list[task_num][2].append((subtask, False))  # Add subtask to the selected task
            return redirect(url_for('view_task', task_num=task_num))

    task, completed, subtasks = todo_list[task_num]

    # Handle subtask completion
    for i in range(len(subtasks)):
        if request.args.get(f'subtask-{i}'):  # Check if the checkbox for the subtask was clicked
            subtasks[i] = (subtasks[i][0], not subtasks[i][1])  # Toggle completion status

    # Pass both the subtasks and their indices to the template
    subtasks_with_index = [(index, subtask) for index, subtask in enumerate(subtasks)]

    return render_template('view_task.html', task=task, completed=completed, subtasks=subtasks_with_index,
                           task_num=task_num)


if __name__ == '__main__':
    app.run(debug=True)
