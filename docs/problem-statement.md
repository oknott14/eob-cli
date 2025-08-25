# 📝 Take-Home Assignment: Extract Structured Data from EOB PDFs

## 🎯 Objective

Build a command-line application that accepts Explanation of Benefits (EOB) PDFs and outputs structured data in JSON format.

The goal is to simulate a real-world task where AI is used to extract meaningful information from semi-structured documents for downstream automation.

## ✅ Core Requirements

Implement a CLI tool that accepts a local PDF or ZIP file of PDFs:

```
python extract_eob.py --file path/to/eob.pdf
```

The script should extract and return structured JSON output representing the claims data.

The application must use Gemini Flash as the underlying model.

You should use a modern orchestration framework such as:

- LangChain
- Google’s Agents SDK
- Or another agentic / structured-output framework

## 📁 Sample PDFs

Please include a ZIP file with 2–3 sample EOB PDFs that you’ve found from public sources or generated yourself. These examples will serve as the foundation for your testing and development.

Example to get started:
Blue Shield CA Sample EOB (Scribd)

## 🧪 Bonus Points

1. Add basic test coverage using your sample PDFs to validate your output.

1. Handle layout variations or missing values gracefully.

1. Share your process, prompt design, and reasoning in your README or notes.

1. Use tools like Cursor, Claude Code, or Windsurf to accelerate development and debug your approach.

## 📦 Submission

Please submit:

1. Your code (GitHub or zip)

1. A README.md with setup instructions, example usage, and any design notes

1. A ZIP file with 2–3 sample EOBs used in testing
