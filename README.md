# Campus Progress Tracker

A comprehensive full-stack web application for colleges and educational institutions to track syllabus progress, monitor student confidence levels, and provide data-driven insights for academic improvement.

## Features

### Role-Based Access Control
- **Admin Dashboard**: Overall analytics, syllabus completion tracking, faculty status monitoring, low confidence alerts, parent visibility summary
- **Faculty Dashboard**: Add daily syllabus logs, view student feedback, weak topic analytics, faculty activity tracking
- **Student Dashboard**: View syllabus progress, submit confidence feedback, request revisions, track improvement history
- **Parent Dashboard**: View child's academic progress, confidence levels, faculty remarks, revision recommendations, learning health status

### Key Features
- 🔐 Secure authentication with password hashing and session management
- 📊 Interactive dashboards with Chart.js analytics
- 📱 Fully responsive design (mobile, tablet, desktop)
- 🎨 Professional blue and white academic theme
- 📈 Comprehensive analytics and reporting
- 🔔 Low-confidence alerts and revision recommendations
- 👥 Parent-child data mapping for secure access

## Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (development) with MySQL support (production)
- **ORM**: SQLAlchemy
- **Authentication**: Flask-Login with password hashing
- **CSRF Protection**: Flask-WTF

### Frontend
- **Framework**: HTML5, CSS3, JavaScript
- **Styling**: Bootstrap 5.3
- **Icons**: Bootstrap Icons
- **Charts**: Chart.js
- **Responsive**: Mobile-first design

## Project Structure

```
campus-progress-tracker/
├── app/
│   ├── __init__.py              # Flask app initialization
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   ├── student.py           # Student model
│   │   ├── parent.py            # Parent model
│   │   ├── faculty.py           # Faculty model
│   │   ├── subject.py           # Subject model
│   │   ├── class_model.py       # Class model
│   │   ├── faculty_log.py       # Faculty log model
│   │   ├── student_feedback.py  # Student feedback model
│   │   └── parent_student_mapping.py  # Parent-student mapping
│   ├── routes/                  # Application routes
│   │   ├── __init__.py
│   │   ├── auth.py              # Authentication routes
│   │   ├── admin.py             # Admin dashboard routes
│   │   ├── faculty.py           # Faculty dashboard routes
│   │   ├── student.py           # Student dashboard routes
│   │   ├── parent.py            # Parent dashboard routes
│   │   └── main.py              # Main routes
│   ├── templates/               # HTML templates
│   │   ├── base.html            # Base template
│   │   ├── dashboard_base.html  # Dashboard base template
│   │   ├── index.html           # Home page
│   │   ├── auth/                # Auth templates
│   │   ├── admin/               # Admin templates
│   │   ├── faculty/             # Faculty templates
│   │   ├── student/             # Student templates
│   │   └── parent/              # Parent templates
│   └── static/                  # Static files
│       ├── css/
│       │   └── style.css        # Custom CSS
│       └── js/
│           └── main.js          # Custom JavaScript
├── instance/                     # Instance folder for SQLite database
├── config.py                     # Application configuration
├── init_db.py                    # Database initialization script
├── run.py                        # Application entry point
├── requirements.txt              # Python dependencies
└── README.md                    # This file
```

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Navigate to Project Directory
```bash
cd C:\Users\anisa\CascadeProjects\campus-progress-tracker
```

### Step 2: Install Python Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Initialize Database with Sample Data
```bash
python init_db.py
```

This will create the SQLite database and insert sample data including:
- Admin, Faculty, Student, and Parent users
- Classes and Subjects
- Faculty logs and Student feedback
- Parent-student mappings

**Sample Login Credentials:**
- Admin: `admin` / `admin123`
- Faculty: `faculty` / `faculty123`
- Student: `student` / `student123`
- Parent: `parent` / `parent123`

### Step 4: Run the Application
```bash
python run.py
```

The application will start on `http://localhost:5000`

## Database Schema

### Users
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email address
- `password_hash`: Hashed password
- `role`: Role (admin, faculty, student, parent)
- `full_name`: Full name
- `is_active`: Account status
- `created_at`: Creation timestamp
- `last_login`: Last login timestamp

### Students
- `id`: Primary key
- `user_id`: Foreign key to Users
- `roll_number`: Unique roll number
- `class_id`: Foreign key to Classes
- `date_of_birth`: Date of birth
- `admission_date`: Admission date
- `phone`: Phone number
- `address`: Address

### Parents
- `id`: Primary key
- `user_id`: Foreign key to Users
- `phone`: Phone number
- `occupation`: Occupation

### Faculty
- `id`: Primary key
- `user_id`: Foreign key to Users
- `employee_id`: Unique employee ID
- `department`: Department
- `qualification`: Qualification
- `phone`: Phone number
- `joining_date`: Joining date

### Classes
- `id`: Primary key
- `name`: Class name (e.g., "10th Grade - A")
- `grade`: Grade (e.g., "10th")
- `section`: Section (e.g., "A")
- `academic_year`: Academic year
- `class_teacher_id`: Foreign key to Faculty

### Subjects
- `id`: Primary key
- `name`: Subject name
- `code`: Subject code
- `class_id`: Foreign key to Classes
- `total_units`: Total units
- `description`: Description

### FacultyLogs
- `id`: Primary key
- `faculty_id`: Foreign key to Faculty
- `class_id`: Foreign key to Classes
- `subject_id`: Foreign key to Subjects
- `unit`: Unit
- `topic`: Topic
- `date`: Date
- `completion_percentage`: Completion percentage (0-100)
- `confidence_level`: Confidence level (Low, Medium, High)
- `remarks`: Remarks
- `created_at`: Creation timestamp

### StudentFeedback
- `id`: Primary key
- `student_id`: Foreign key to Students
- `class_id`: Foreign key to Classes
- `subject_id`: Foreign key to Subjects
- `topic`: Topic
- `confidence_level`: Confidence level (Low, Medium, High)
- `need_revision`: Revision needed flag
- `comment`: Comment
- `date`: Date
- `created_at`: Creation timestamp

### ParentStudentMapping
- `id`: Primary key
- `parent_id`: Foreign key to Parents
- `student_id`: Foreign key to Students
- `relationship`: Relationship (Father, Mother, Guardian)
- `is_primary`: Primary parent flag

## Configuration

### Environment Variables
The application uses the configuration from `config.py`. For production, you can set:

```env
SECRET_KEY=your-secret-key-here
FLASK_ENV=production
DATABASE_URL=mysql+pymysql://user:password@localhost/campus_progress
```

### Configuration Options
Edit `config.py` to customize:
- Secret key
- Database URI (SQLite for development, MySQL for production)
- Session lifetime
- CSRF settings
- Debug mode

## Usage

### For Admin
1. Login with admin credentials
2. View overall analytics on dashboard
3. Monitor faculty updates and student confidence
4. Track low confidence alerts
5. View subject-wise and class-wise performance
6. Manage students, faculty, parents, classes, and subjects

### For Faculty
1. Login with faculty credentials
2. Add daily syllabus progress logs
3. View submitted logs history
4. View student feedback for your subjects
5. Analyze weak topics to focus on

### For Students
1. Login with student credentials
2. View syllabus progress for your class
3. Submit confidence feedback for topics
4. Request revisions for difficult topics
5. Track your improvement over time

### For Parents
1. Login with parent credentials
2. View your child's academic progress
3. Monitor confidence levels across subjects
4. Read faculty remarks
5. Get revision suggestions based on weak areas

## Development

### Adding New Features
1. Add new models in `app/models/`
2. Add new routes in `app/routes/`
3. Create frontend templates in `app/templates/`
4. Add custom CSS in `app/static/css/`
5. Add custom JavaScript in `app/static/js/`

### Testing
```bash
# Run the application in development mode
python run.py

# Access the application at http://localhost:5000
```

## Production Deployment

### Using Gunicorn
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 run:app
```

### Using MySQL in Production
1. Install MySQL and create database
2. Install PyMySQL: `pip install pymysql`
3. Update `config.py` with MySQL connection string
4. Set `FLASK_ENV=production`

### Security Considerations
- Change default secret keys in production
- Use HTTPS in production
- Set `SESSION_COOKIE_SECURE=True` in production
- Use environment variables for sensitive data
- Implement proper error handling
- Add rate limiting for API endpoints

## Troubleshooting

### Database Issues
- Delete `instance/campus_progress.db` and run `python init_db.py` to reset
- Check database permissions

### Authentication Issues
- Clear browser cookies
- Check session configuration
- Verify password hashing

### Dashboard Not Loading
- Check browser console for errors
- Verify static files are accessible
- Check template syntax

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is licensed under the MIT License.

## Support

For issues, questions, or contributions, please contact the development team.

## Acknowledgments

- Flask framework
- SQLAlchemy ORM
- Bootstrap for responsive design
- Chart.js for data visualization
- Bootstrap Icons for iconography
