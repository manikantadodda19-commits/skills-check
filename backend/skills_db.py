"""
Skills Database — Maps job roles to required skills, keywords, industry averages, and courses.
"""

JOB_ROLES = {
    "AI / ML Engineer": {
        "technical_skills": [
            "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
            "Keras", "Scikit-Learn", "NLP", "Computer Vision", "Neural Networks",
            "Data Preprocessing", "Feature Engineering", "Model Deployment",
            "MLOps", "NumPy", "Pandas", "Matplotlib", "SQL", "Git",
            "Docker", "AWS", "REST API", "Flask", "FastAPI", "Linux",
            "Statistics", "Probability", "Linear Algebra", "Calculus"
        ],
        "soft_skills": [
            "Problem Solving", "Communication", "Teamwork", "Critical Thinking",
            "Research", "Presentation", "Time Management", "Analytical Thinking"
        ],
        "ats_keywords": [
            "Python", "Machine Learning", "Deep Learning", "TensorFlow", "PyTorch",
            "NLP", "Computer Vision", "Neural Networks", "AWS", "Docker",
            "REST API", "SQL", "Scikit-Learn", "Pandas", "NumPy",
            "Model Deployment", "MLOps", "Data Pipeline", "Feature Engineering",
            "Keras", "Flask", "FastAPI", "Git", "Linux", "Statistics"
        ],
        "industry_avg": {
            "technical": 78,
            "soft": 72,
            "projects": 75
        },
        "description": "Develop machine learning models, analyze data, and deploy AI solutions.",
        "sample_jobs": [
            {"title": "AI / ML Engineer", "company": "Google", "location": "New York, NY", "type": "Full Time · Hybrid", "posted": "2 days ago"},
            {"title": "Senior AI / ML Engineer", "company": "Amazon", "location": "Seattle, WA", "type": "Full Time · Remote", "posted": "1 day ago"},
            {"title": "AI / ML Engineer", "company": "Tesla", "location": "San Francisco, CA", "type": "Full Time · Hybrid", "posted": "3 days ago"}
        ]
    },

    "Data Scientist": {
        "technical_skills": [
            "Python", "R", "SQL", "Machine Learning", "Deep Learning",
            "Statistics", "Probability", "Data Visualization", "Tableau", "Power BI",
            "Pandas", "NumPy", "Scikit-Learn", "TensorFlow", "PyTorch",
            "NLP", "A/B Testing", "Hypothesis Testing", "Regression",
            "Classification", "Clustering", "Feature Engineering",
            "Big Data", "Spark", "Hadoop", "Excel", "Git", "Jupyter"
        ],
        "soft_skills": [
            "Communication", "Storytelling", "Problem Solving", "Analytical Thinking",
            "Business Acumen", "Presentation", "Teamwork", "Curiosity"
        ],
        "ats_keywords": [
            "Python", "R", "SQL", "Machine Learning", "Statistics",
            "Data Visualization", "Tableau", "Power BI", "Pandas", "NumPy",
            "Scikit-Learn", "TensorFlow", "NLP", "A/B Testing", "Regression",
            "Classification", "Big Data", "Spark", "Feature Engineering",
            "Hypothesis Testing", "Deep Learning", "Jupyter", "Git"
        ],
        "industry_avg": {
            "technical": 76,
            "soft": 70,
            "projects": 73
        },
        "description": "Analyze complex datasets to derive insights and build predictive models.",
        "sample_jobs": [
            {"title": "Data Scientist", "company": "Meta", "location": "Menlo Park, CA", "type": "Full Time · Hybrid", "posted": "1 day ago"},
            {"title": "Senior Data Scientist", "company": "Netflix", "location": "Los Gatos, CA", "type": "Full Time · Remote", "posted": "3 days ago"},
            {"title": "Data Scientist", "company": "Microsoft", "location": "Redmond, WA", "type": "Full Time · Hybrid", "posted": "2 days ago"}
        ]
    },

    "Software Engineer": {
        "technical_skills": [
            "Python", "Java", "JavaScript", "TypeScript", "C++", "C#",
            "HTML", "CSS", "React", "Angular", "Node.js", "Express.js",
            "SQL", "NoSQL", "MongoDB", "PostgreSQL", "MySQL",
            "REST API", "GraphQL", "Docker", "Kubernetes", "AWS", "Azure", "GCP",
            "Git", "CI/CD", "Agile", "Scrum", "Linux",
            "Data Structures", "Algorithms", "System Design", "OOP",
            "Microservices", "Testing", "Unit Testing"
        ],
        "soft_skills": [
            "Communication", "Teamwork", "Problem Solving", "Time Management",
            "Leadership", "Adaptability", "Code Review", "Mentoring"
        ],
        "ats_keywords": [
            "Python", "Java", "JavaScript", "React", "Node.js", "SQL",
            "REST API", "Docker", "Kubernetes", "AWS", "Git", "CI/CD",
            "Agile", "Microservices", "System Design", "OOP",
            "Data Structures", "Algorithms", "TypeScript", "MongoDB",
            "PostgreSQL", "GraphQL", "Linux", "Testing", "HTML", "CSS"
        ],
        "industry_avg": {
            "technical": 80,
            "soft": 74,
            "projects": 78
        },
        "description": "Design, develop, and maintain software applications and systems.",
        "sample_jobs": [
            {"title": "Software Engineer", "company": "Google", "location": "Mountain View, CA", "type": "Full Time · Hybrid", "posted": "1 day ago"},
            {"title": "Senior Software Engineer", "company": "Apple", "location": "Cupertino, CA", "type": "Full Time · On-site", "posted": "2 days ago"},
            {"title": "Software Engineer", "company": "Spotify", "location": "New York, NY", "type": "Full Time · Remote", "posted": "4 days ago"}
        ]
    },

    "Cloud Engineer": {
        "technical_skills": [
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
            "Ansible", "Jenkins", "CI/CD", "Linux", "Bash", "Python",
            "Networking", "TCP/IP", "DNS", "Load Balancing", "VPN",
            "IAM", "Security", "Monitoring", "CloudWatch", "Prometheus",
            "Grafana", "Serverless", "Lambda", "EC2", "S3", "RDS",
            "VPC", "CloudFormation", "Helm", "Git", "SQL"
        ],
        "soft_skills": [
            "Problem Solving", "Communication", "Teamwork", "Documentation",
            "Troubleshooting", "Critical Thinking", "Adaptability", "Time Management"
        ],
        "ats_keywords": [
            "AWS", "Azure", "GCP", "Docker", "Kubernetes", "Terraform",
            "CI/CD", "Linux", "Python", "Serverless", "Lambda",
            "EC2", "S3", "IAM", "VPC", "CloudFormation", "Jenkins",
            "Monitoring", "Networking", "Bash", "Ansible", "Helm",
            "Security", "Load Balancing", "Git", "SQL"
        ],
        "industry_avg": {
            "technical": 75,
            "soft": 70,
            "projects": 72
        },
        "description": "Design, deploy, and manage cloud infrastructure and services.",
        "sample_jobs": [
            {"title": "Cloud Engineer", "company": "Amazon Web Services", "location": "Seattle, WA", "type": "Full Time · Hybrid", "posted": "1 day ago"},
            {"title": "Senior Cloud Engineer", "company": "Microsoft Azure", "location": "Redmond, WA", "type": "Full Time · Remote", "posted": "2 days ago"},
            {"title": "Cloud Infrastructure Engineer", "company": "Google Cloud", "location": "Austin, TX", "type": "Full Time · Hybrid", "posted": "3 days ago"}
        ]
    },

    "Data Analyst": {
        "technical_skills": [
            "SQL", "Excel", "Python", "R", "Tableau", "Power BI",
            "Data Visualization", "Statistics", "Data Cleaning",
            "Pandas", "NumPy", "Google Analytics", "Looker",
            "A/B Testing", "Hypothesis Testing", "Regression",
            "ETL", "Data Warehousing", "BigQuery", "Redshift",
            "Reporting", "Dashboard", "VBA", "Google Sheets", "Git"
        ],
        "soft_skills": [
            "Communication", "Analytical Thinking", "Attention to Detail",
            "Problem Solving", "Presentation", "Storytelling",
            "Business Acumen", "Time Management"
        ],
        "ats_keywords": [
            "SQL", "Excel", "Python", "Tableau", "Power BI",
            "Data Visualization", "Statistics", "Pandas", "NumPy",
            "A/B Testing", "ETL", "Data Warehousing", "BigQuery",
            "Google Analytics", "Looker", "Reporting", "Dashboard",
            "Regression", "Data Cleaning", "R", "Git"
        ],
        "industry_avg": {
            "technical": 74,
            "soft": 72,
            "projects": 70
        },
        "description": "Collect, process, and analyze data to help organizations make data-driven decisions.",
        "sample_jobs": [
            {"title": "Data Analyst", "company": "Uber", "location": "San Francisco, CA", "type": "Full Time · Hybrid", "posted": "2 days ago"},
            {"title": "Senior Data Analyst", "company": "Airbnb", "location": "San Francisco, CA", "type": "Full Time · Remote", "posted": "1 day ago"},
            {"title": "Business Data Analyst", "company": "JPMorgan Chase", "location": "New York, NY", "type": "Full Time · On-site", "posted": "3 days ago"}
        ]
    }
}


# Skill aliases for flexible matching
SKILL_ALIASES = {
    "ml": "Machine Learning",
    "dl": "Deep Learning",
    "ai": "Artificial Intelligence",
    "nlp": "NLP",
    "cv": "Computer Vision",
    "js": "JavaScript",
    "ts": "TypeScript",
    "py": "Python",
    "tf": "TensorFlow",
    "k8s": "Kubernetes",
    "postgres": "PostgreSQL",
    "mongo": "MongoDB",
    "aws": "AWS",
    "gcp": "GCP",
    "react.js": "React",
    "reactjs": "React",
    "node": "Node.js",
    "nodejs": "Node.js",
    "express": "Express.js",
    "expressjs": "Express.js",
    "restful api": "REST API",
    "restful apis": "REST API",
    "rest apis": "REST API",
    "rest": "REST API",
    "ci cd": "CI/CD",
    "cicd": "CI/CD",
    "continuous integration": "CI/CD",
    "continuous deployment": "CI/CD",
    "oop": "OOP",
    "object oriented": "OOP",
    "scikit learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "power bi": "Power BI",
    "powerbi": "Power BI",
    "a/b test": "A/B Testing",
    "ab testing": "A/B Testing",
    "cloud watch": "CloudWatch",
    "data structure": "Data Structures",
    "data structures": "Data Structures",
    "algorithm": "Algorithms",
    "algorithms": "Algorithms",
    "system design": "System Design",
    "micro services": "Microservices",
    "microservice": "Microservices",
    "html5": "HTML",
    "css3": "CSS",
    "html/css": "HTML",
    "c sharp": "C#",
    "csharp": "C#",
    "cpp": "C++",
    "sql server": "SQL",
    "mysql": "MySQL",
    "postgresql": "PostgreSQL",
    "big data": "Big Data",
    "data viz": "Data Visualization",
    "data visualization": "Data Visualization",
    "natural language processing": "NLP",
    "convolutional neural network": "Neural Networks",
    "cnn": "Neural Networks",
    "rnn": "Neural Networks",
    "recurrent neural network": "Neural Networks",
    "neural net": "Neural Networks",
    "neural network": "Neural Networks",
}


# Course catalog mapped to skills
COURSE_CATALOG = {
    "AWS": {
        "title": "AWS Cloud Practitioner",
        "platform": "Coursera",
        "description": "Learn AWS fundamentals to manage cloud services",
        "icon": "☁️",
        "url": "https://www.coursera.org/learn/aws-cloud-practitioner"
    },
    "Docker": {
        "title": "Docker Mastery",
        "platform": "Udemy",
        "description": "Master Docker containers and deployment workflows",
        "icon": "🐳",
        "url": "https://www.udemy.com/course/docker-mastery/"
    },
    "Deep Learning": {
        "title": "Deep Learning Specialization",
        "platform": "Coursera",
        "description": "Machine Learning and Neural Networks specialization by Andrew Ng",
        "icon": "🧠",
        "url": "https://www.coursera.org/specializations/deep-learning"
    },
    "TensorFlow": {
        "title": "TensorFlow Developer Certificate",
        "platform": "Coursera",
        "description": "Build and train neural networks with TensorFlow",
        "icon": "🔶",
        "url": "https://www.coursera.org/professional-certificates/tensorflow-in-practice"
    },
    "PyTorch": {
        "title": "PyTorch for Deep Learning",
        "platform": "Udemy",
        "description": "Learn PyTorch from scratch to advanced deep learning",
        "icon": "🔥",
        "url": "https://www.udemy.com/course/pytorch-for-deep-learning/"
    },
    "Kubernetes": {
        "title": "Kubernetes for Beginners",
        "platform": "Udemy",
        "description": "Learn Kubernetes orchestration and container management",
        "icon": "⚙️",
        "url": "https://www.udemy.com/course/learn-kubernetes/"
    },
    "REST API": {
        "title": "RESTful APIs with Python & Flask",
        "platform": "Udemy",
        "description": "Build professional REST APIs using Flask",
        "icon": "🔗",
        "url": "https://www.udemy.com/course/rest-api-flask-and-python/"
    },
    "SQL": {
        "title": "SQL Bootcamp",
        "platform": "Udemy",
        "description": "Complete SQL bootcamp from zero to hero",
        "icon": "🗄️",
        "url": "https://www.udemy.com/course/the-complete-sql-bootcamp/"
    },
    "React": {
        "title": "React - The Complete Guide",
        "platform": "Udemy",
        "description": "Dive into React.js with hooks, Redux, and Next.js",
        "icon": "⚛️",
        "url": "https://www.udemy.com/course/react-the-complete-guide/"
    },
    "JavaScript": {
        "title": "JavaScript Zero to Hero",
        "platform": "Coursera",
        "description": "Master JavaScript from fundamentals to advanced concepts",
        "icon": "📜",
        "url": "https://www.coursera.org/learn/javascript"
    },
    "Python": {
        "title": "Python for Everybody",
        "platform": "Coursera",
        "description": "Complete Python programming specialization",
        "icon": "🐍",
        "url": "https://www.coursera.org/specializations/python"
    },
    "Machine Learning": {
        "title": "Machine Learning by Stanford",
        "platform": "Coursera",
        "description": "Learn ML fundamentals with Andrew Ng",
        "icon": "🤖",
        "url": "https://www.coursera.org/learn/machine-learning"
    },
    "NLP": {
        "title": "Natural Language Processing Specialization",
        "platform": "Coursera",
        "description": "Master NLP with sequence models, attention, and transformers",
        "icon": "💬",
        "url": "https://www.coursera.org/specializations/natural-language-processing"
    },
    "Computer Vision": {
        "title": "Computer Vision with OpenCV & Python",
        "platform": "Udemy",
        "description": "Learn image processing and computer vision",
        "icon": "👁️",
        "url": "https://www.udemy.com/course/python-for-computer-vision-with-opencv-and-deep-learning/"
    },
    "Tableau": {
        "title": "Tableau Data Visualization",
        "platform": "Coursera",
        "description": "Create stunning data visualizations with Tableau",
        "icon": "📊",
        "url": "https://www.coursera.org/learn/data-visualization-tableau"
    },
    "Power BI": {
        "title": "Microsoft Power BI Desktop",
        "platform": "Udemy",
        "description": "Master Power BI for business intelligence",
        "icon": "📈",
        "url": "https://www.udemy.com/course/microsoft-power-bi-up-running-with-power-bi-desktop/"
    },
    "Terraform": {
        "title": "Terraform for AWS",
        "platform": "Udemy",
        "description": "Learn infrastructure as code with Terraform",
        "icon": "🏗️",
        "url": "https://www.udemy.com/course/terraform-beginner-to-advanced/"
    },
    "Git": {
        "title": "Git & GitHub Masterclass",
        "platform": "Udemy",
        "description": "Version control from beginner to advanced",
        "icon": "🔀",
        "url": "https://www.udemy.com/course/git-and-github-masterclass/"
    },
    "Java": {
        "title": "Java Programming Masterclass",
        "platform": "Udemy",
        "description": "Complete Java developer course",
        "icon": "☕",
        "url": "https://www.udemy.com/course/java-the-complete-java-developer-course/"
    },
    "Data Visualization": {
        "title": "Data Visualization with Python",
        "platform": "Coursera",
        "description": "Create compelling data visualizations",
        "icon": "📊",
        "url": "https://www.coursera.org/learn/python-for-data-visualization"
    },
    "Statistics": {
        "title": "Statistics & Probability",
        "platform": "Khan Academy",
        "description": "Foundational statistics and probability concepts",
        "icon": "📐",
        "url": "https://www.khanacademy.org/math/statistics-probability"
    },
    "CI/CD": {
        "title": "CI/CD with Jenkins & Docker",
        "platform": "Udemy",
        "description": "Build continuous integration and delivery pipelines",
        "icon": "🔄",
        "url": "https://www.udemy.com/course/learn-devops-ci-cd-with-jenkins/"
    },
    "Linux": {
        "title": "Linux Mastery",
        "platform": "Udemy",
        "description": "Master the Linux command line",
        "icon": "🐧",
        "url": "https://www.udemy.com/course/linux-mastery/"
    },
    "Node.js": {
        "title": "Node.js - The Complete Course",
        "platform": "Udemy",
        "description": "Build backend applications with Node.js",
        "icon": "🟢",
        "url": "https://www.udemy.com/course/the-complete-nodejs-developer-course/"
    },
    "Spark": {
        "title": "Apache Spark with Python",
        "platform": "Udemy",
        "description": "Big data processing with PySpark",
        "icon": "⚡",
        "url": "https://www.udemy.com/course/spark-and-python-for-big-data-with-pyspark/"
    },
    "Excel": {
        "title": "Excel Skills for Business",
        "platform": "Coursera",
        "description": "Master Excel for data analysis and reporting",
        "icon": "📗",
        "url": "https://www.coursera.org/specializations/excel"
    },
    "System Design": {
        "title": "System Design Interview Prep",
        "platform": "YouTube",
        "description": "Learn system design principles for scalable applications",
        "icon": "🏛️",
        "url": "https://www.youtube.com/results?search_query=system+design"
    },
    "Data Structures": {
        "title": "Data Structures & Algorithms",
        "platform": "Coursera",
        "description": "Master DSA for coding interviews",
        "icon": "🌳",
        "url": "https://www.coursera.org/specializations/data-structures-algorithms"
    },
    "Algorithms": {
        "title": "Algorithms Specialization",
        "platform": "Coursera",
        "description": "Divide & conquer, graph algorithms, and dynamic programming",
        "icon": "🧩",
        "url": "https://www.coursera.org/specializations/algorithms"
    },
}
