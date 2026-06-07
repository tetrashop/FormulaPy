# FormulaPy – Symbolic Integral Calculator API

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104-green)](https://fastapi.tiangolo.com/)
[![SymPy](https://img.shields.io/badge/SymPy-1.12-orange)](https://www.sympy.org/)

**FormulaPy** is a lightweight, high‑performance REST API for symbolic indefinite integration. It leverages the battle‑tested [SymPy](https://www.sympy.org/) engine to compute antiderivatives of elementary functions and displays results in both plain text and beautiful LaTeX format. A clean web interface is included for demonstration and manual testing.

---

## 📚 Table of Contents

- [Mathematical Background](#mathematical-background)
- [Features](#features)
- [API Specification](#api-specification)
- [Installation & Local Deployment](#installation--local-deployment)
- [Deployment on Vercel](#deployment-on-vercel)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)

---

## 🧠 Mathematical Background

Indefinite integration (antidifferentiation) is the process of finding a function \(F(x)\) such that  
\[
F'(x) = f(x)
\]  
The general solution is written as  
\[
\int f(x)\,dx = F(x) + C
\]  
where \(C\) is an arbitrary constant.  

**FormulaPy** does not implement custom integration algorithms; instead, it delegates to **SymPy**, a computer algebra system (CAS) that implements the **Risch algorithm** for elementary functions, pattern matching, and heuristic integration. SymPy supports:

- Polynomials, rational functions, exponentials, logarithms  
- Trigonometric and hyperbolic functions (sin, cos, tan, cot, sec, csc)  
- Inverse trigonometric functions (asin, acos, atan)  
- Special functions (error function, gamma, etc.)  

The API returns the symbolic result (as a SymPy expression) and its LaTeX representation, ready for embedding in documents or web pages.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔢 **Symbolic integration** | handles a wide range of elementary and special functions |
| 📐 **LaTeX output** | every result is returned as both a plain string and valid LaTeX |
| 🌐 **Web UI** | ready‑to‑use HTML interface with MathJax rendering |
| ⚡ **REST API** | simple `POST /api/integrate` endpoint for programmatic use |
| 🚀 **Serverless ready** | deploy to Vercel, AWS Lambda, or any Python‑compatible platform |
| ✅ **Error handling** | invalid expressions return descriptive error messages |

---

## 📡 API Specification

### Endpoint

`POST /api/integrate`

### Request Body (JSON)

| Field       | Type   | Required | Default | Description                                 |
|-------------|--------|----------|---------|---------------------------------------------|
| `expression`| string | Yes      | –       | Mathematical expression in SymPy syntax.    |
| `variable`  | string | No       | `"x"`   | The integration variable.                   |

**Example request**  
```json
{
  "expression": "sin(x)**2 + 1/x",
  "variable": "x"
}
```

Response Body (JSON)

Field Type Description
result string Plain‑text representation of the antiderivative.
latex string LaTeX code (without  ...  delimiters).
success boolean true if integration succeeded.
error string Error message (only present if success=false).

Example response

```json
{
  "result": "x/2 - sin(2*x)/4 + log(x)",
  "latex": "\\frac{x}{2} - \\frac{\\sin{\\left(2x\\right)}}{4} + \\log{\\left(x\\right)}",
  "success": true,
  "error": ""
}
```

Health Check

GET /api/health

Returns {"status": "ok"} – useful for monitoring.

---

🧪 Installation & Local Deployment

Prerequisites

· Python 3.9 or later
· pip package manager

Steps

1. Clone the repository
   ```bash
   git clone https://github.com/yourusername/FormulaPy.git
   cd FormulaPy
   ```
2. Create a virtual environment (optional but recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate      # Linux / macOS
   venv\Scripts\activate          # Windows
   ```
3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```
4. Run the development server
   ```bash
   uvicorn main:app --reload
   ```
5. Open the web interface
      Navigate to http://localhost:8000 in your browser.

---

☁️ Deployment on Vercel

1. Install Vercel CLI (optional)
   ```bash
   npm i -g vercel
   ```
2. From the project root
   ```bash
   vercel --prod
   ```
   Follow the interactive prompts. Vercel automatically detects the Python configuration via vercel.json.
3. Environment variables – no secrets are required for basic deployment.

Once deployed, your API will be available at https://your-project.vercel.app/api/integrate and the UI at the root URL.

---

📝 Usage Examples

Using curl

```bash
curl -X POST https://your-project.vercel.app/api/integrate \
  -H "Content-Type: application/json" \
  -d '{"expression": "exp(2*x) * cos(x)"}'
```

Using Python requests

```python
import requests

response = requests.post(
    "https://your-project.vercel.app/api/integrate",
    json={"expression": "x**3 + sqrt(x)"}
)
print(response.json()["latex"])
```

Sample integrations

Input expression Result (indefinite integral)
x**2 + 3*x + 5 x**3/3 + 3*x**2/2 + 5*x
sin(2*x) -cos(2*x)/2
1/(1+x**2) atan(x)
exp(-x**2) sqrt(pi)*erf(x)/2
log(x) / x log(x)**2/2

---

📁 Project Structure

```
FormulaPy/
├── main.py                # FastAPI application (endpoints, integration logic)
├── requirements.txt       # Python dependencies
├── vercel.json            # Vercel deployment configuration
├── static/
│   └── index.html         # Web interface (MathJax, responsive design)
├── README.md              # This documentation
└── LICENSE                # MIT license
```

---

🤝 Contributing

Contributions are welcome! To maintain stability:

1. Fork the repository.
2. Create a feature branch (git checkout -b feature/new-rule).
3. Commit your changes (git commit -m 'Add integration rule for ...').
4. Push to the branch (git push origin feature/new-rule).
5. Open a Pull Request.

Please ensure that all existing tests (if added in the future) pass and that new functionality includes proper error handling.

---

📄 License

This project is released under the MIT License. See the LICENSE file for full details.

---

🙏 Acknowledgements

· SymPy – the backbone of symbolic mathematics.
· FastAPI – modern, fast web framework.
· Vercel – seamless serverless deployment.
· MathJax – beautiful LaTeX rendering in the browser.

---

FormulaPy – symbolic integration, made simple.
Built for education, research, and rapid prototyping.
