"""
Database seed data — careers, skills, roadmaps, and projects.
Run via: flask seed-db
"""
import json


SKILLS_DATA = [
    # Technical
    {"name": "Python", "category": "technical", "description": "General-purpose programming language"},
    {"name": "JavaScript", "category": "technical", "description": "Front-end and Node.js scripting"},
    {"name": "HTML/CSS", "category": "technical", "description": "Web markup and styling"},
    {"name": "SQL", "category": "technical", "description": "Relational database querying"},
    {"name": "React", "category": "technical", "description": "JavaScript UI library"},
    {"name": "Node.js", "category": "technical", "description": "Server-side JavaScript runtime"},
    {"name": "Flask / Django", "category": "technical", "description": "Python web frameworks"},
    {"name": "Git & GitHub", "category": "technical", "description": "Version control"},
    {"name": "Data Analysis (Pandas)", "category": "technical", "description": "Data manipulation with Pandas"},
    {"name": "Machine Learning (Scikit-learn)", "category": "technical", "description": "ML library for Python"},
    {"name": "TensorFlow / PyTorch", "category": "technical", "description": "Deep learning frameworks"},
    {"name": "Cloud (AWS/Azure/GCP)", "category": "technical", "description": "Cloud platform services"},
    {"name": "Docker & Kubernetes", "category": "technical", "description": "Containerisation and orchestration"},
    {"name": "Linux / Bash", "category": "technical", "description": "Command-line and scripting"},
    {"name": "Networking Fundamentals", "category": "technical", "description": "TCP/IP, DNS, firewalls"},
    {"name": "Cybersecurity Concepts", "category": "technical", "description": "Threats, vulnerabilities, OWASP"},
    {"name": "Figma / Adobe XD", "category": "technical", "description": "UI design and prototyping tools"},
    {"name": "SEO & SEM", "category": "technical", "description": "Search engine optimisation and marketing"},
    {"name": "Google Analytics", "category": "technical", "description": "Web analytics platform"},
    {"name": "Excel / Spreadsheets", "category": "technical", "description": "Data analysis with spreadsheets"},
    {"name": "Testing (Pytest/Selenium)", "category": "technical", "description": "Automated testing tools"},
    {"name": "REST APIs", "category": "technical", "description": "HTTP API design and consumption"},
    {"name": "PostgreSQL", "category": "technical", "description": "Enterprise relational database"},
    # Soft
    {"name": "Problem Solving", "category": "soft", "description": "Analytical and creative thinking"},
    {"name": "Communication", "category": "soft", "description": "Written and verbal communication"},
    {"name": "Teamwork", "category": "soft", "description": "Collaborative working"},
    {"name": "Time Management", "category": "soft", "description": "Meeting deadlines and prioritising"},
    {"name": "Critical Thinking", "category": "soft", "description": "Evaluating information logically"},
    {"name": "Adaptability", "category": "soft", "description": "Learning and adjusting quickly"},
    {"name": "Attention to Detail", "category": "soft", "description": "Precision in work"},
    {"name": "Creativity", "category": "soft", "description": "Generating novel ideas"},
]


CAREERS_DATA = [
    {
        "slug": "python-developer",
        "title": "Python Developer",
        "category": "Software Development",
        "short_description": "Build web applications, automation tools, and APIs using Python.",
        "description": (
            "Python Developers write clean, efficient code to build web applications, automate tasks, "
            "and develop APIs. They work across industries including finance, health-tech, e-commerce, "
            "and data science. Entry-level roles often involve backend web development, scripting, "
            "or contributing to open-source projects."
        ),
        "education_level": "bachelor",
        "avg_salary": "$65,000 – $120,000",
        "demand_level": "High",
        "is_beginner_friendly": True,
        "icon": "bi-code-slash",
        "entry_roles": json.dumps(["Junior Python Developer", "Backend Developer", "Automation Engineer", "API Developer"]),
        "next_steps": json.dumps([
            "Complete a Python web framework project (Flask or Django)",
            "Contribute to an open-source Python repository",
            "Build a REST API with authentication",
            "Apply for junior developer or internship roles",
        ]),
        "skills": ["Python", "Flask / Django", "REST APIs", "SQL", "Git & GitHub", "Linux / Bash", "PostgreSQL", "Problem Solving"],
    },
    {
        "slug": "web-developer",
        "title": "Web Developer",
        "category": "Software Development",
        "short_description": "Design and build responsive websites and web applications.",
        "description": (
            "Web Developers create the digital interfaces that users interact with every day. "
            "They may specialise in front-end (HTML, CSS, JavaScript), back-end (server, database, API), "
            "or full-stack development. Strong demand across every industry."
        ),
        "education_level": "bachelor",
        "avg_salary": "$55,000 – $110,000",
        "demand_level": "High",
        "is_beginner_friendly": True,
        "icon": "bi-globe",
        "entry_roles": json.dumps(["Junior Web Developer", "Front-End Developer", "Full-Stack Intern"]),
        "next_steps": json.dumps([
            "Build and publish at least two personal projects",
            "Learn a front-end framework (React, Vue, or Svelte)",
            "Study responsive design and accessibility",
            "Apply to web developer internships",
        ]),
        "skills": ["HTML/CSS", "JavaScript", "React", "Node.js", "Git & GitHub", "REST APIs", "SQL", "Problem Solving"],
    },
    {
        "slug": "data-analyst",
        "title": "Data Analyst",
        "category": "Data & Analytics",
        "short_description": "Analyse datasets to uncover insights and support business decisions.",
        "description": (
            "Data Analysts collect, clean, and interpret structured data to answer business questions. "
            "They produce reports, dashboards, and visualisations that help organisations make informed decisions. "
            "Excel and SQL are the core entry-level tools; Python and BI tools grow in importance with experience."
        ),
        "education_level": "bachelor",
        "avg_salary": "$55,000 – $95,000",
        "demand_level": "High",
        "is_beginner_friendly": True,
        "icon": "bi-bar-chart-line",
        "entry_roles": json.dumps(["Junior Data Analyst", "Business Intelligence Analyst", "Reporting Analyst"]),
        "next_steps": json.dumps([
            "Build a data analysis portfolio project using a public dataset",
            "Earn a free SQL certification (e.g. from Mode Analytics or Kaggle)",
            "Learn Power BI or Tableau for visualisation",
            "Apply for data analyst graduate roles",
        ]),
        "skills": ["SQL", "Excel / Spreadsheets", "Data Analysis (Pandas)", "Python", "Google Analytics", "Critical Thinking", "Communication", "Attention to Detail"],
    },
    {
        "slug": "ai-ml-engineer",
        "title": "AI / ML Engineer",
        "category": "Artificial Intelligence",
        "short_description": "Design and build machine learning models and AI-powered systems.",
        "description": (
            "AI/ML Engineers apply mathematics, statistics, and programming to build models that learn from data. "
            "They work on recommendation systems, image recognition, NLP, and predictive analytics. "
            "A strong foundation in Python, mathematics, and data analysis is essential before specialising in ML."
        ),
        "education_level": "bachelor",
        "avg_salary": "$90,000 – $160,000",
        "demand_level": "High",
        "is_beginner_friendly": False,
        "icon": "bi-robot",
        "entry_roles": json.dumps(["Junior ML Engineer", "Data Scientist (Junior)", "AI Research Assistant"]),
        "next_steps": json.dumps([
            "Complete a Kaggle competition or ML course (fast.ai, Coursera)",
            "Build and publish an end-to-end ML project",
            "Study mathematics: linear algebra, statistics, calculus",
            "Apply for ML internships or research assistant roles",
        ]),
        "skills": ["Python", "Machine Learning (Scikit-learn)", "TensorFlow / PyTorch", "Data Analysis (Pandas)", "SQL", "Mathematics", "Critical Thinking", "Problem Solving"],
    },
    {
        "slug": "cybersecurity-analyst",
        "title": "Cybersecurity Analyst",
        "category": "Cybersecurity",
        "short_description": "Protect systems and networks from cyber threats and attacks.",
        "description": (
            "Cybersecurity Analysts monitor, detect, and respond to security incidents. "
            "They assess vulnerabilities, implement defences, and ensure compliance with security standards. "
            "Entry-level roles often involve SOC analysis, vulnerability scanning, and incident response."
        ),
        "education_level": "bachelor",
        "avg_salary": "$65,000 – $120,000",
        "demand_level": "High",
        "is_beginner_friendly": False,
        "icon": "bi-shield-lock",
        "entry_roles": json.dumps(["SOC Analyst (Level 1)", "Junior Security Analyst", "Penetration Testing Intern"]),
        "next_steps": json.dumps([
            "Earn CompTIA Security+ or a similar entry-level certification",
            "Set up a home lab with Kali Linux and practice on TryHackMe",
            "Study OWASP Top 10 and network fundamentals",
            "Apply for SOC analyst or security intern positions",
        ]),
        "skills": ["Cybersecurity Concepts", "Networking Fundamentals", "Linux / Bash", "Python", "Problem Solving", "Attention to Detail", "Critical Thinking"],
    },
    {
        "slug": "ui-ux-designer",
        "title": "UI/UX Designer",
        "category": "Design",
        "short_description": "Create intuitive, accessible user interfaces and experiences.",
        "description": (
            "UI/UX Designers research user needs, design wireframes and prototypes, and collaborate with developers "
            "to deliver excellent digital experiences. They combine psychology, design principles, and technical "
            "knowledge to make software easy and enjoyable to use."
        ),
        "education_level": "diploma",
        "avg_salary": "$55,000 – $105,000",
        "demand_level": "High",
        "is_beginner_friendly": True,
        "icon": "bi-palette",
        "entry_roles": json.dumps(["Junior UI Designer", "UX Research Assistant", "Product Designer (Junior)"]),
        "next_steps": json.dumps([
            "Build three case studies in Figma and publish them",
            "Study Nielsen Norman Group UX guidelines",
            "Complete Google's UX Design Certificate",
            "Apply for junior designer or internship roles",
        ]),
        "skills": ["Figma / Adobe XD", "HTML/CSS", "Creativity", "Communication", "Attention to Detail", "Critical Thinking", "Problem Solving"],
    },
    {
        "slug": "cloud-engineer",
        "title": "Cloud Engineer",
        "category": "Cloud & DevOps",
        "short_description": "Design, deploy, and manage scalable cloud infrastructure.",
        "description": (
            "Cloud Engineers build and maintain infrastructure on platforms like AWS, Azure, and GCP. "
            "They design scalable, reliable, and cost-effective cloud architectures and automate deployments "
            "using Infrastructure as Code and CI/CD pipelines."
        ),
        "education_level": "bachelor",
        "avg_salary": "$80,000 – $150,000",
        "demand_level": "High",
        "is_beginner_friendly": False,
        "icon": "bi-cloud",
        "entry_roles": json.dumps(["Cloud Support Engineer", "DevOps Intern", "Junior Cloud Architect"]),
        "next_steps": json.dumps([
            "Earn AWS Cloud Practitioner or Azure Fundamentals certification",
            "Deploy a project on AWS or GCP with Docker",
            "Learn Terraform for infrastructure as code",
            "Apply for cloud support or DevOps intern roles",
        ]),
        "skills": ["Cloud (AWS/Azure/GCP)", "Docker & Kubernetes", "Linux / Bash", "Python", "Networking Fundamentals", "Git & GitHub", "Problem Solving"],
    },
    {
        "slug": "software-tester",
        "title": "Software Tester / QA Engineer",
        "category": "Software Development",
        "short_description": "Ensure software quality through manual and automated testing.",
        "description": (
            "Software Testers / QA Engineers design test plans, execute tests, and report defects. "
            "They are the last line of defence before software reaches users. "
            "Entry-level testers often start with manual testing before progressing to automation frameworks."
        ),
        "education_level": "diploma",
        "avg_salary": "$50,000 – $90,000",
        "demand_level": "Medium",
        "is_beginner_friendly": True,
        "icon": "bi-bug",
        "entry_roles": json.dumps(["Junior QA Analyst", "Manual Tester", "Automation Test Engineer (Junior)"]),
        "next_steps": json.dumps([
            "Learn Selenium or Playwright for test automation",
            "Practise writing test cases for a real application",
            "Study ISTQB Foundation Level syllabus",
            "Apply for QA intern or junior tester positions",
        ]),
        "skills": ["Testing (Pytest/Selenium)", "Python", "Attention to Detail", "Communication", "Problem Solving", "Critical Thinking", "Git & GitHub"],
    },
    {
        "slug": "digital-marketing-specialist",
        "title": "Digital Marketing Specialist",
        "category": "Marketing",
        "short_description": "Grow brands and audiences through online channels and campaigns.",
        "description": (
            "Digital Marketing Specialists plan and execute online campaigns across SEO, SEM, social media, "
            "email, and content marketing. They analyse metrics, optimise campaigns, and report on ROI. "
            "A blend of creative and analytical skills is essential."
        ),
        "education_level": "bachelor",
        "avg_salary": "$45,000 – $85,000",
        "demand_level": "High",
        "is_beginner_friendly": True,
        "icon": "bi-megaphone",
        "entry_roles": json.dumps(["Digital Marketing Intern", "SEO Analyst", "Social Media Coordinator"]),
        "next_steps": json.dumps([
            "Earn Google Digital Marketing & E-commerce Certificate",
            "Build a personal or mock brand campaign portfolio",
            "Set up and optimise a Google Ads or Meta Ads test campaign",
            "Apply for digital marketing intern roles",
        ]),
        "skills": ["SEO & SEM", "Google Analytics", "Communication", "Creativity", "Excel / Spreadsheets", "Critical Thinking", "Attention to Detail"],
    },
    {
        "slug": "business-analyst",
        "title": "Business Analyst",
        "category": "Business & Strategy",
        "short_description": "Bridge the gap between business needs and technology solutions.",
        "description": (
            "Business Analysts gather requirements, model business processes, and translate stakeholder "
            "needs into clear specifications for development teams. They use data analysis, documentation, "
            "and communication skills to deliver business value."
        ),
        "education_level": "bachelor",
        "avg_salary": "$60,000 – $110,000",
        "demand_level": "Medium",
        "is_beginner_friendly": True,
        "icon": "bi-briefcase",
        "entry_roles": json.dumps(["Junior Business Analyst", "Systems Analyst (Entry)", "Business Analysis Intern"]),
        "next_steps": json.dumps([
            "Study BABOK (Business Analysis Body of Knowledge)",
            "Learn to write user stories and BDD scenarios",
            "Build a requirements document for a fictional project",
            "Apply for BA graduate or intern roles",
        ]),
        "skills": ["SQL", "Excel / Spreadsheets", "Communication", "Critical Thinking", "Problem Solving", "Attention to Detail", "Teamwork"],
    },
]


ROADMAPS_DATA = {
    "python-developer": {
        "title": "Python Developer Learning Roadmap",
        "description": "A structured path from Python beginner to job-ready Python developer.",
        "estimated_weeks": 20,
        "stages": [
            {
                "order": 1,
                "title": "Python Fundamentals",
                "description": "Master the core of Python before anything else.",
                "topics": json.dumps(["Variables & data types", "Control flow", "Functions", "Lists, dicts, sets", "File I/O", "Error handling"]),
                "resources": json.dumps([
                    {"title": "Python.org Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "docs"},
                    {"title": "Automate the Boring Stuff with Python (free)", "url": "https://automatetheboringstuff.com/", "type": "book"},
                    {"title": "freeCodeCamp Python Full Course", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "type": "video"},
                ]),
                "exercises": json.dumps(["Number guessing game", "Simple calculator", "Student grade tracker"]),
                "estimated_hours": 30,
            },
            {
                "order": 2,
                "title": "Object-Oriented Programming & Modules",
                "description": "Learn OOP concepts and how to structure larger programs.",
                "topics": json.dumps(["Classes & objects", "Inheritance", "Encapsulation", "Standard library modules", "Virtual environments", "pip & packages"]),
                "resources": json.dumps([
                    {"title": "Real Python — OOP Tutorial", "url": "https://realpython.com/python3-object-oriented-programming/", "type": "article"},
                    {"title": "Corey Schafer OOP Playlist", "url": "https://www.youtube.com/playlist?list=PL-osiE80TeTt2d9bfVyTiXJA-UTHn6WwU", "type": "video"},
                ]),
                "exercises": json.dumps(["Library management system", "Bank account simulator"]),
                "estimated_hours": 20,
            },
            {
                "order": 3,
                "title": "Web Development with Flask",
                "description": "Build your first web application.",
                "topics": json.dumps(["Flask routing", "Templates (Jinja2)", "Forms & validation", "SQLAlchemy ORM", "User authentication", "REST APIs"]),
                "resources": json.dumps([
                    {"title": "Flask Mega-Tutorial by Miguel Grinberg", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world", "type": "article"},
                    {"title": "Flask Official Docs", "url": "https://flask.palletsprojects.com/", "type": "docs"},
                ]),
                "exercises": json.dumps(["To-do app with login", "Blog with CRUD operations"]),
                "estimated_hours": 40,
            },
            {
                "order": 4,
                "title": "Databases & SQL",
                "description": "Store and query data effectively.",
                "topics": json.dumps(["SQL basics", "Joins & aggregations", "PostgreSQL", "SQLAlchemy relationships", "Migrations with Alembic"]),
                "resources": json.dumps([
                    {"title": "SQLZoo (interactive SQL)", "url": "https://sqlzoo.net/", "type": "interactive"},
                    {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "article"},
                ]),
                "exercises": json.dumps(["Design a database for an e-commerce site", "Write 10 SQL queries on a public dataset"]),
                "estimated_hours": 20,
            },
            {
                "order": 5,
                "title": "Git, Testing & Deployment",
                "description": "Ship reliable code to production.",
                "topics": json.dumps(["Git workflow", "Unit testing with Pytest", "CI with GitHub Actions", "Deployment on Render / Heroku", "Environment variables & secrets"]),
                "resources": json.dumps([
                    {"title": "Pro Git (free book)", "url": "https://git-scm.com/book/en/v2", "type": "book"},
                    {"title": "Pytest Official Docs", "url": "https://docs.pytest.org/", "type": "docs"},
                ]),
                "exercises": json.dumps(["Deploy your Flask app to Render", "Write unit tests for your blog app"]),
                "estimated_hours": 15,
            },
        ],
    },
    "web-developer": {
        "title": "Web Developer Learning Roadmap",
        "description": "From HTML beginner to full-stack web developer.",
        "estimated_weeks": 24,
        "stages": [
            {
                "order": 1,
                "title": "HTML & CSS Foundations",
                "description": "Build your first web pages.",
                "topics": json.dumps(["HTML5 structure", "CSS properties", "Flexbox & Grid", "Responsive design", "Media queries"]),
                "resources": json.dumps([
                    {"title": "freeCodeCamp Responsive Web Design", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "type": "interactive"},
                    {"title": "MDN HTML Guide", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "docs"},
                ]),
                "exercises": json.dumps(["Personal portfolio page", "Landing page clone"]),
                "estimated_hours": 25,
            },
            {
                "order": 2,
                "title": "JavaScript Essentials",
                "description": "Make your pages interactive.",
                "topics": json.dumps(["Variables, loops, functions", "DOM manipulation", "Events", "Fetch API / AJAX", "ES6+ features"]),
                "resources": json.dumps([
                    {"title": "JavaScript.info (free & comprehensive)", "url": "https://javascript.info/", "type": "book"},
                    {"title": "freeCodeCamp JS Algorithms", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "interactive"},
                ]),
                "exercises": json.dumps(["Quiz app", "Weather app using a public API"]),
                "estimated_hours": 35,
            },
            {
                "order": 3,
                "title": "React Front-End Framework",
                "description": "Build modern component-based UIs.",
                "topics": json.dumps(["Components & props", "State & hooks", "React Router", "Fetching data", "Context API"]),
                "resources": json.dumps([
                    {"title": "React Official Docs", "url": "https://react.dev/", "type": "docs"},
                    {"title": "Scrimba React Course (free)", "url": "https://scrimba.com/learn/learnreact", "type": "interactive"},
                ]),
                "exercises": json.dumps(["Task manager app", "Movie search app"]),
                "estimated_hours": 40,
            },
            {
                "order": 4,
                "title": "Back-End with Node.js & Express",
                "description": "Build APIs and server-side logic.",
                "topics": json.dumps(["Node.js basics", "Express routing", "REST API design", "Authentication (JWT)", "SQL / MongoDB"]),
                "resources": json.dumps([
                    {"title": "The Odin Project — Node Path", "url": "https://www.theodinproject.com/paths/full-stack-javascript", "type": "interactive"},
                    {"title": "Express Official Docs", "url": "https://expressjs.com/", "type": "docs"},
                ]),
                "exercises": json.dumps(["CRUD API for a blog", "Authentication REST API"]),
                "estimated_hours": 35,
            },
            {
                "order": 5,
                "title": "Deployment & Portfolio",
                "description": "Ship your projects publicly.",
                "topics": json.dumps(["Git workflow", "Netlify / Vercel for front-end", "Render for back-end", "Environment variables", "HTTPS"]),
                "resources": json.dumps([
                    {"title": "Netlify Docs", "url": "https://docs.netlify.com/", "type": "docs"},
                    {"title": "Render Docs", "url": "https://render.com/docs", "type": "docs"},
                ]),
                "exercises": json.dumps(["Deploy all three portfolio projects live"]),
                "estimated_hours": 10,
            },
        ],
    },
    "data-analyst": {
        "title": "Data Analyst Learning Roadmap",
        "description": "From spreadsheets to professional data analysis.",
        "estimated_weeks": 18,
        "stages": [
            {
                "order": 1,
                "title": "Excel & Spreadsheet Mastery",
                "description": "Start with the most widely-used data tool.",
                "topics": json.dumps(["Formulas & functions", "PivotTables", "VLOOKUP / XLOOKUP", "Charts and graphs", "Data cleaning"]),
                "resources": json.dumps([
                    {"title": "Excel Jet — free tutorials", "url": "https://exceljet.net/", "type": "article"},
                    {"title": "GCFGlobal Excel Course", "url": "https://edu.gcfglobal.org/en/excel/", "type": "interactive"},
                ]),
                "exercises": json.dumps(["Sales report with PivotTable", "Monthly budget tracker"]),
                "estimated_hours": 20,
            },
            {
                "order": 2,
                "title": "SQL for Data Analysis",
                "description": "Query databases to extract insights.",
                "topics": json.dumps(["SELECT, WHERE, ORDER BY", "JOINs", "GROUP BY & aggregations", "Subqueries", "Window functions"]),
                "resources": json.dumps([
                    {"title": "Mode Analytics SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "article"},
                    {"title": "SQLZoo Interactive Exercises", "url": "https://sqlzoo.net/", "type": "interactive"},
                ]),
                "exercises": json.dumps(["Analyse a public dataset with 10+ queries", "Write a sales dashboard query"]),
                "estimated_hours": 25,
            },
            {
                "order": 3,
                "title": "Python for Data Analysis",
                "description": "Use Python to process and visualise data.",
                "topics": json.dumps(["Python basics", "Pandas DataFrames", "NumPy", "Matplotlib / Seaborn", "Jupyter Notebooks"]),
                "resources": json.dumps([
                    {"title": "Kaggle Python Course (free)", "url": "https://www.kaggle.com/learn/python", "type": "interactive"},
                    {"title": "Kaggle Pandas Course (free)", "url": "https://www.kaggle.com/learn/pandas", "type": "interactive"},
                ]),
                "exercises": json.dumps(["Exploratory data analysis on a Kaggle dataset", "Weather data visualisation project"]),
                "estimated_hours": 30,
            },
            {
                "order": 4,
                "title": "Data Visualisation & BI Tools",
                "description": "Tell stories with data using dashboards.",
                "topics": json.dumps(["Tableau Public or Power BI basics", "Dashboard design principles", "Interactive charts"]),
                "resources": json.dumps([
                    {"title": "Tableau Free Training", "url": "https://www.tableau.com/learn/training", "type": "video"},
                    {"title": "Microsoft Power BI Learning", "url": "https://learn.microsoft.com/en-us/power-bi/", "type": "docs"},
                ]),
                "exercises": json.dumps(["Build a sales performance dashboard", "COVID-19 data visualisation"]),
                "estimated_hours": 20,
            },
        ],
    },
}


PROJECTS_DATA = [
    # Python Developer
    {
        "career_slug": "python-developer",
        "title": "Personal Budget Tracker",
        "problem_statement": "Most people struggle to track daily expenses. Build a command-line tool to record income and expenses, categorise transactions, and display monthly summaries.",
        "difficulty": "Beginner",
        "technologies": json.dumps(["Python", "SQLite", "Click (CLI library)"]),
        "core_features": json.dumps(["Add/edit/delete transactions", "Category tagging", "Monthly summary report", "CSV export"]),
        "milestones": json.dumps(["Set up SQLite schema", "CRUD operations for transactions", "Category summary", "CSV export"]),
        "learning_outcomes": json.dumps(["File I/O", "SQLite with Python", "CLI design", "Data aggregation"]),
        "advanced_features": json.dumps(["ASCII chart of spending", "Recurring transaction support", "Budget alerts"]),
    },
    {
        "career_slug": "python-developer",
        "title": "Flask Task Management API",
        "problem_statement": "Build a REST API for a task manager where users can register, create tasks, and mark them complete.",
        "difficulty": "Intermediate",
        "technologies": json.dumps(["Python", "Flask", "SQLAlchemy", "PostgreSQL", "JWT"]),
        "core_features": json.dumps(["User registration & JWT auth", "CRUD for tasks", "Task priorities and due dates", "Filter and search"]),
        "milestones": json.dumps(["Database models", "Auth endpoints", "Task CRUD", "Filtering & pagination", "Deploy to Render"]),
        "learning_outcomes": json.dumps(["REST API design", "JWT authentication", "Database relationships", "Deployment"]),
        "advanced_features": json.dumps(["Email reminders", "Team tasks & sharing", "Analytics endpoint"]),
    },
    # Web Developer
    {
        "career_slug": "web-developer",
        "title": "Responsive Portfolio Website",
        "problem_statement": "Create a professional personal portfolio to showcase your projects, skills, and contact information.",
        "difficulty": "Beginner",
        "technologies": json.dumps(["HTML5", "CSS3", "JavaScript"]),
        "core_features": json.dumps(["Hero section", "Projects grid", "Skills section", "Contact form", "Mobile-responsive"]),
        "milestones": json.dumps(["HTML structure", "CSS styling", "JavaScript interactions", "Deploy to GitHub Pages"]),
        "learning_outcomes": json.dumps(["Semantic HTML", "CSS Flexbox/Grid", "Responsive design", "GitHub Pages deployment"]),
        "advanced_features": json.dumps(["Dark mode toggle", "Animated skill bars", "Blog section"]),
    },
    {
        "career_slug": "web-developer",
        "title": "Full-Stack Recipe App",
        "problem_statement": "Build a full-stack application where users can save, share, and search recipes.",
        "difficulty": "Intermediate",
        "technologies": json.dumps(["React", "Node.js", "Express", "PostgreSQL"]),
        "core_features": json.dumps(["User authentication", "Recipe CRUD", "Search and filter", "Image upload"]),
        "milestones": json.dumps(["Back-end API", "Database schema", "React front-end", "Auth flow", "Deployment"]),
        "learning_outcomes": json.dumps(["React hooks", "REST API integration", "Full-stack architecture", "Auth flow"]),
        "advanced_features": json.dumps(["Rating system", "Meal planner", "Shopping list generator"]),
    },
    # Data Analyst
    {
        "career_slug": "data-analyst",
        "title": "COVID-19 Data Dashboard",
        "problem_statement": "Explore a public COVID-19 dataset to build visualisations and a summary dashboard.",
        "difficulty": "Beginner",
        "technologies": json.dumps(["Python", "Pandas", "Matplotlib", "Seaborn", "Jupyter Notebook"]),
        "core_features": json.dumps(["Data cleaning", "Time-series charts", "Country comparisons", "Summary statistics"]),
        "milestones": json.dumps(["Load & clean data", "Summary statistics", "Time-series plots", "Country comparison", "Jupyter notebook report"]),
        "learning_outcomes": json.dumps(["Data cleaning", "Pandas operations", "Visualisation storytelling"]),
        "advanced_features": json.dumps(["Interactive Plotly charts", "Tableau/Power BI version", "Predictive trendline"]),
    },
    # AI/ML Engineer
    {
        "career_slug": "ai-ml-engineer",
        "title": "Movie Recommendation System",
        "problem_statement": "Build a collaborative filtering recommendation engine trained on the MovieLens dataset.",
        "difficulty": "Intermediate",
        "technologies": json.dumps(["Python", "Scikit-learn", "Pandas", "Flask"]),
        "core_features": json.dumps(["Data preprocessing", "Collaborative filtering model", "Top-N recommendations", "Simple web UI"]),
        "milestones": json.dumps(["Load & explore dataset", "Build user-item matrix", "Train model", "Evaluation metrics", "Flask API"]),
        "learning_outcomes": json.dumps(["Collaborative filtering", "Model evaluation", "API integration"]),
        "advanced_features": json.dumps(["Hybrid filtering (content + collaborative)", "Real-time user feedback"]),
    },
    # Cybersecurity
    {
        "career_slug": "cybersecurity-analyst",
        "title": "Network Port Scanner",
        "problem_statement": "Build a Python tool to scan open ports on a target host and identify running services.",
        "difficulty": "Beginner",
        "technologies": json.dumps(["Python", "Socket library", "Threading"]),
        "core_features": json.dumps(["Multi-threaded port scan", "Service banner grabbing", "Report generation"]),
        "milestones": json.dumps(["Basic TCP connect scan", "Threading for speed", "Banner grabbing", "Report output"]),
        "learning_outcomes": json.dumps(["TCP/IP networking", "Sockets", "Threading", "Ethical hacking mindset"]),
        "advanced_features": json.dumps(["UDP scanning", "OS fingerprinting", "Integration with CVE database"]),
    },
    # UI/UX Designer
    {
        "career_slug": "ui-ux-designer",
        "title": "Mobile Banking App Redesign",
        "problem_statement": "Redesign the UI of a fictional (or real publicly documented) mobile banking app to improve usability.",
        "difficulty": "Beginner",
        "technologies": json.dumps(["Figma"]),
        "core_features": json.dumps(["User research summary", "Wireframes", "High-fidelity mockups", "Interactive prototype", "Usability test notes"]),
        "milestones": json.dumps(["Competitor analysis", "User persona", "Low-fi wireframes", "High-fi designs", "Prototype & test"]),
        "learning_outcomes": json.dumps(["User research", "Wireframing", "Prototyping", "Design system creation"]),
        "advanced_features": json.dumps(["Accessibility audit", "Motion design spec", "Handoff documentation"]),
    },
]
