<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Push Code to GitHub</title>
    <link href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/themes/prism.min.css" rel="stylesheet" />
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #282c34;
            color: white;
            text-align: center;
            padding: 20px;
        }
        h1 {
            margin-bottom: 20px;
        }
        #codeContainer {
            position: relative;
            width: 80%;
            height: 200px;
        }
        #codeInput {
            width: 100%;
            height: 100%;
            background-color: #1e1e1e;
            color: #dcdcdc;
            border: 1px solid #444;
            border-radius: 5px;
            padding: 10px;
            font-family: 'Courier New', Courier, monospace;
            resize: none;
            overflow: auto;
            white-space: pre;
            outline: none;
            position: absolute;
            top: 0;
            left: 0;
            z-index: 2;
        }
        #highlight {
            position: absolute;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            padding: 10px;
            border-radius: 5px;
            background-color: #1e1e1e;
            color: #dcdcdc;
            white-space: pre-wrap;
            word-wrap: break-word;
            z-index: 1;
            pointer-events: none; /* Prevent interaction with the highlight */
        }
        #fileNameInput {
            width: 80%;
            padding: 10px;
            margin-top: 10px;
            border: 1px solid #444;
            border-radius: 5px;
            background-color: #1e1e1e;
            color: #dcdcdc;
        }
        button {
            padding: 10px 20px;
            margin-top: 10px;
            border: none;
            border-radius: 5px;
            background-color: #007bff;
            color: white;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
        #loader {
            display: none;
            margin-top: 20px;
            animation: spin 1s linear infinite;
        }
        @keyframes spin {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }
    </style>
</head>
<body>
    <h1>Push Code to GitHub</h1>
    <div id="codeContainer">
        <pre id="highlight"></pre>
        <textarea id="codeInput" placeholder="Type your code here..." oninput="highlightCode()"></textarea>
    </div>
    <br>
    <input id="fileNameInput" type="text" placeholder="File Name (e.g., main.py)" />
    <br>
    <button onclick="pushCode()">Push to GitHub</button>
    <div id="loader">Loading...</div>

    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.24.1/prism.min.js"></script>
    <script>
        function highlightCode() {
            const codeInput = document.getElementById('codeInput');
            const highlight = document.getElementById('highlight');
            highlight.innerHTML = Prism.highlight(codeInput.value, Prism.languages.python, 'python');
        }

        async function pushCode() {
            const code = document.getElementById('codeInput').value;
            const fileName = document.getElementById('fileNameInput').value || "main.py";
            const loader = document.getElementById('loader');

            loader.style.display = 'block'; // Show loader

            try {
                const response = await fetch('http://127.0.0.1:5000/push', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ code, file_name: fileName }),
                });

                loader.style.display = 'none'; // Hide loader

                if (!response.ok) {
                    const errorResult = await response.json();
                    alert(`Error: ${errorResult.error || response.statusText}`);
                    return;
                }

                const result = await response.json();
                alert(result.message);
            } catch (error) {
                loader.style.display = 'none'; // Hide loader
                console.error("Failed to push code:", error);
                alert("An error occurred while trying to push the code.");
            }
        }
    </script>
</body>
</html>