# statictext
Web page generator


StaticText is a simple static site generator written in Python. It converts Markdown content into styled HTML pages using a provided template and CSS.

## 📁 Project Structure


statictext/
├── content/
│ └── index.md # Your markdown content
├── static/
│ └── index.css # Your custom styles
├── template.html # Base HTML template with {{ Title }} and {{ Content }} placeholders
├── public/ # Output folder (auto-created)
│ └── index.html # Generated HTML file
├── src/
│ └── generate_page.py # Python script to generate the page
├── main.sh # Optional shell script to run the generator
└── README.md # This file

bash
Copy
Edit

## 🚀 Usage

### Step 1: Add Your Markdown Content

Edit `content/index.md` with your markdown text. Make sure it includes a `# Heading` at the top (this will be the page `<title>`).

### Step 2: Customize Your Template

Edit `template.html` to style your page layout. It must include:



### Step 3: Run the Generator


python3 src/generate_page.py

🧪 Tests
Run unit tests with:

bash
Copy
Edit
python3 -m unittest discover
📌 Requirements
Python 3.7+

## 🤝 Contributing
This project is open to improvements. If you want to explore how it works or extend its features:

### Clone the repo:

``` bash
Copy
Edit
git clone https://github.com/1GJones/statictext.git
cd statictext
Install dependencies if any (currently uses standard library only).
```
### Run the generator:

bash
Copy
Edit
python3 src/generate_page.py

### Run all tests:

bash
Copy
Edit
python3 -m unittest discover
Feel free to fork, build, and test it. If you're a hiring manager or a developer interested in contributing — try pulling the project down and running it locally.




## 🛠 Author
Gamal Jones – StaticText Project

```html
<title>{{ Title }}</title>
<div>{{ Content }}</div>

