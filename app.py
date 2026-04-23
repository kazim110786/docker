from flask import Flask, request, jsonify

app = Flask(__name__)

tasks = []

@app.route('/')
def home():
    return """
<!DOCTYPE html>
<html>
<head>
    <title>Task Manager</title>

    <style>
        body {
            margin: 0;
            font-family: 'Segoe UI', sans-serif;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;

            /* 🌄 Background Image */
            background: url('https://images.unsplash.com/photo-1508780709619-79562169bc64') no-repeat center center/cover;
        }

        /* 🌙 Dark overlay */
        body::before {
            content: "";
            position: absolute;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.5);
            top: 0;
            left: 0;
        }

        .container {
            position: relative;
            background: rgba(255,255,255,0.15);
            backdrop-filter: blur(12px);
            padding: 30px;
            border-radius: 16px;
            width: 420px;
            text-align: center;
            color: white;
            box-shadow: 0 8px 25px rgba(0,0,0,0.4);
            animation: fadeIn 1s ease-in-out;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        h1 {
            margin-bottom: 10px;
        }

        p {
            font-size: 14px;
            color: #ddd;
        }

        input {
            width: 65%;
            padding: 10px;
            border-radius: 8px;
            border: none;
            outline: none;
        }

        button {
            padding: 10px 15px;
            border: none;
            border-radius: 8px;
            background: #00c6ff;
            background: linear-gradient(45deg, #00c6ff, #0072ff);
            color: white;
            cursor: pointer;
            margin-left: 5px;
            transition: 0.3s;
        }

        button:hover {
            transform: scale(1.05);
        }

        ul {
            list-style: none;
            padding: 0;
            margin-top: 20px;
        }

        li {
            background: rgba(255,255,255,0.2);
            margin: 10px 0;
            padding: 12px;
            border-radius: 10px;
            text-align: left;
            display: flex;
            align-items: center;
        }

        li::before {
            content: "✔️";
            margin-right: 10px;
        }

        footer {
            margin-top: 15px;
            font-size: 12px;
            color: #ccc;
        }
    </style>
</head>

<body>

<div class="container">
    <h1>🚀 Task Manager</h1>
    <p>Stay focused. Stay productive.</p>

    <form onsubmit="event.preventDefault(); addTask();">
        <input type="text" id="task" placeholder="Enter a task..." required>
        <button type="submit">Add</button>
    </form>

    <ul id="taskList"></ul>

    <footer>Made with ❤️ using Flask & Docker</footer>
</div>

<script>
function loadTasks() {
    fetch('/tasks')
    .then(res => res.json())
    .then(data => {
        const list = document.getElementById('taskList');
        list.innerHTML = '';
        data.forEach(task => {
            const li = document.createElement('li');
            li.textContent = task;
            list.appendChild(li);
        });
    });
}

function addTask(){
    const taskInput = document.getElementById('task');
    fetch('/tasks', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({task: taskInput.value})
    }).then(() => {
        taskInput.value = '';
        loadTasks();
    });
}

window.onload = loadTasks;
</script>

</body>
</html>
"""

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    if 'task' in data and data['task']:
        tasks.append(data['task'])
        return jsonify({"message": "Task added"}), 201
    return jsonify({"error": "Invalid task"}), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)