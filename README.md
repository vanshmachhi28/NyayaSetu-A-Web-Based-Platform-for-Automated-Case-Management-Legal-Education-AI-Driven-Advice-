# NyayaSetu – Legal Automation & Learning Platform ⚖️✨

Welcome to **NyayaSetu**, a next-generation web platform built with Django to simplify, automate, and empower the legal journey for advocates, students, and the public. NyayaSetu seamlessly blends technology with legal practice—offering tools for instant case management, document generation, learning, and AI-powered advice. 🌟

---

## Project Overview 📘

NyayaSetu showcases the power of Django and MySQL, providing a secure, scalable, and user-friendly experience. With a strong focus on automation and accessibility, the platform reduces paperwork, streamlines workflows, and makes legal expertise more reachable for everyone. 🚀🔒

---

## Core Features 🛠️

- **Automated Case Import:** Enter a case number and instantly fetch details from court sites—no manual entry, no typos. 🔎📄
- **AI Legal Bot:** Get instant, plain-English legal summaries and next-step advice using a smart language model. 🤖⚡
- **Document Generator:** Effortlessly create affidavits, agreements, and petitions from simple forms—ready to file or export as PDF. 📑🖨️
- **Role-Based Dashboards:** Tailored interfaces and permissions for advocates, students, and public users. 👦‍🎓👩‍⚖️
- **Learning & Mock Test Hub:** Legal notes, interactive quizzes, and internship info for law students. 📚🔖
- **Q&A Forum:** Public and students ask questions, advocates answer; all moderated for quality and safety. 💬💡
- **PDF/CSV Export:** Download reports and documents with a single click for offline use. 📥
- **Legal Awareness Hub:** Layman-friendly explanations of IPC, CrPC, and common legal rights and processes. 🏛️

---

## Why NyayaSetu Matters 🌏

Legal clarity and access are no longer a privilege, but a necessity. NyayaSetu bridges legal expertise and technology—removing friction, supporting learning, and helping users make smarter, faster decisions. It's a complete solution for the modern legal era. 🚀💡

---

## Technologies Used 🛠️

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=green)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=for-the-badge&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
**LLM Integration:** (OpenAI, Groq)

---

## Screenshots 🖼️

All major flows in NyayaSetu are captured in the **Screenshots** folder:

- `Screenshots/Dashboard.jpg` – Main dashboard overview
- `Screenshots/Login_Page.jpg` – Login and role selection
- `Screenshots/Admin_HomePage.jpg` – Admin home with key stats
- `Screenshots/Admin_Login.jpg` – Admin authentication
- `Screenshots/Admin_Search_Log.jpg` – Admin search history / logs
- `Screenshots/Admin_UserQuery.jpg` – Admin view of user queries
- `Screenshots/Document_Generator.jpg` – Auto document generator interface
- `Screenshots/QAForm.jpg` – Q&A forum submission form
- `Screenshots/Quiz.jpg` – Quiz/MCQ module interface

These images give a quick visual tour of NyayaSetu’s UI for evaluators and recruiters.

---

## Quiz Module Content 🧠

The **Quiz** folder contains text files with curated questions used in the Learning & Mock Test Hub:

- `Quiz/Beginner Quiz.txt` – Basic legal awareness questions
- `Quiz/Challenge Quizzes.txt` – Harder, scenario-based questions
- `Quiz/Exam Prep Quizzes.txt` – Questions designed for exam-style practice
- `Quiz/Law_Basics_Quiz.txt` – Core IPC/CrPC and fundamental legal concepts
- `Quiz/Subject-wise Quizzes.txt` – Topic-wise grouped questions

These files make it easy to update or extend the quiz bank without changing the code.

---

## Court Search & Case Import Module 🔍

The **search module** folder documents how NyayaSetu’s automated case import works:

- `search module/module 9 api story.txt` – Narrative and technical explanation of the API-based search feature (Module 9).  
  It explains how the system:
  - Takes an official case number as input  
  - Calls the court website/API  
  - Parses party names, dates, status, and judgment text  
  - Saves results into the Django models with minimal manual typing

This file is helpful for understanding the design decisions, API usage, and scraping/automation logic behind the case import feature.

---

## Project Stages Timeline 🗂️

| Stage        | Highlights                                                        |
|--------------|-------------------------------------------------------------------|
| Planning     | Conceptualized features & user flows                              |
| Setup        | Django/MySQL configuration, project scaffolding                   |
| Core Dev     | Built major modules: case import, Q&A, doc gen, bot, UI           |
| Testing      | Manual & some automated tests, UI polish                          |
| Finalization | Role-based workflows, bugfixes, doc writing                       |
| Release      | GitHub upload, screenshots, ready to demo                         |

---

## Getting Started / Installation 🚀

1. **Clone the repository:**
    ```
    git clone https://github.com/yourusername/NyayaSetu.git
    cd NyayaSetu
    ```
2. **Install dependencies:**
    ```
    pip install -r requirements.txt
    ```
3. **Database Setup:**
    - Create an empty MySQL database.
    - Configure database credentials in `djangoProject/settings.py`.
    - Run migrations:
        ```
        python manage.py migrate
        ```
    - *(Optional: Load demo data as explained in docs/fixtures, if present.)*
4. **Run the development server:**
    ```
    python manage.py runserver
    ```

---

## Usage

- Login via role-based dashboard as Advocate, Student, or Public.
- Use case import, legal bot, document generation, quizzes, and forum.
- Export documents or data as PDF/CSV.

---

## Contributing

Contributions, issues, and feature requests are welcome—fork the repository and submit a pull request!

---

## License

This project is open source. See `LICENSE` for details.

---

## Contact

Developed by Vansh Prakash Machhi  
*Questions? Feedback?*  
[My_Email](mailto:machhivansh470@gmail.com)   

---

> Embrace the future of law with NyayaSetu!  
> _Connecting legal minds with technology, one case at a time._
