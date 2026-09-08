from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "rc_patel_grievance_secret_key"

MYSQL_HOST = "localhost"
MYSQL_USER = "root"
MYSQL_PASSWORD = "kunal"
MYSQL_DATABASE = "college_grievance"

DEPARTMENTS = [
    "Computer Engineering",
    "Information Technology",
    "Mechanical Engineering",
    "Civil Engineering",
    "Electrical Engineering",
    "Electronics Engineering"
]


def get_db():
    try:
        return mysql.connector.connect(
            host=MYSQL_HOST,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DATABASE
        )
    except Error as e:
        print("Database Error:", e)
        return None


def admin_required():
    return "user_id" in session and session.get("role") == "admin"


def student_required():
    return "user_id" in session and session.get("role") == "student"


def faculty_required():
    return "user_id" in session and session.get("role") == "faculty"


def hod_required():
    return "user_id" in session and session.get("role") == "hod"


@app.route("/")
def index():
    if "user_id" in session:
        role = session.get("role")
        if role == "admin":
            return redirect(url_for("admin_dashboard"))
        elif role == "student":
            return redirect(url_for("student_dashboard"))
        elif role == "faculty":
            return redirect(url_for("faculty_dashboard"))
        elif role == "hod":
            return redirect(url_for("hod_dashboard"))
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        if not email or not password:
            flash("Please enter email and password.", "danger")
            return redirect(url_for("login"))

        db = get_db()
        if not db:
            flash("Database connection failed.", "danger")
            return redirect(url_for("login"))

        cursor = db.cursor(dictionary=True)
        user = None

        try:
            cursor.execute(
                "SELECT * FROM users WHERE email = %s",
                (email,)
            )
            user = cursor.fetchone()
        except Error as e:
            print("Login Database Error:", e)
        finally:
            cursor.close()
            db.close()

        if user:
            password_valid = False

            try:
                password_valid = check_password_hash(
                    user["password"], password
                )
            except Exception:
                password_valid = False

            if not password_valid and user["password"] == password:
                password_valid = True

            if password_valid:
                session["user_id"] = user["id"]
                session["name"] = user["name"]
                session["email"] = user["email"]
                session["role"] = user["role"]
                session["department"] = (user.get("department") or "").strip()

                flash("Login successful.", "success")

                if user["role"] == "admin":
                    return redirect(url_for("admin_dashboard"))
                elif user["role"] == "student":
                    return redirect(url_for("student_dashboard"))
                elif user["role"] == "faculty":
                    return redirect(url_for("faculty_dashboard"))
                elif user["role"] == "hod":
                    return redirect(url_for("hod_dashboard"))

        flash("Invalid email or password.", "danger")

    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        department = request.form.get("department", "").strip()
        password = request.form.get("password", "")
        confirm_password = request.form.get("confirm_password", "")

        if not name or not email or not department or not password:
            flash("Please fill all required fields.", "danger")
            return redirect(url_for("register"))

        if department not in DEPARTMENTS:
            flash("Please select a valid department.", "danger")
            return redirect(url_for("register"))

        if password != confirm_password:
            flash("Passwords do not match.", "danger")
            return redirect(url_for("register"))

        db = get_db()
        if not db:
            flash("Database connection failed.", "danger")
            return redirect(url_for("register"))

        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            if cursor.fetchone():
                flash("Email already registered.", "warning")
                return redirect(url_for("register"))

            hashed_password = generate_password_hash(password)

            cursor.execute("""
                INSERT INTO users
                (name, email, password, role, department)
                VALUES (%s, %s, %s, 'student', %s)
            """, (name, email, hashed_password, department))

            db.commit()
            flash("Registration successful. Please login.", "success")

        except Error as e:
            db.rollback()
            print("Registration Error:", e)
            flash("Registration failed.", "danger")

        finally:
            cursor.close()
            db.close()

        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/student")
def student_dashboard():
    if not student_required():
        return redirect(url_for("login"))

    db = get_db()
    complaints = []

    if db:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, student_name, student_email, department,
                       subject AS title, description, status,
                       hod_reply, created_at
                FROM complaints
                WHERE student_email = %s
                ORDER BY created_at DESC
            """, (session.get("email"),))
            complaints = cursor.fetchall()
        except Error as e:
            print("Student Dashboard Error:", e)
        finally:
            cursor.close()
            db.close()

    total_complaints = len(complaints)
    pending_complaints = sum(c["status"] == "Pending" for c in complaints)
    in_progress_complaints = sum(c["status"] == "In Progress" for c in complaints)
    resolved_complaints = sum(c["status"] == "Resolved" for c in complaints)

    return render_template(
        "student_dashboard.html",
        complaints=complaints,
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints
    )


@app.route("/submit-complaint", methods=["GET", "POST"])
def submit_complaint():
    if not student_required():
        return redirect(url_for("login"))

    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        department = (session.get("department") or "").strip()

        if not title or not description:
            flash("Please enter subject and description.", "danger")
            return redirect(url_for("submit_complaint"))

        if department not in DEPARTMENTS:
            flash("Invalid department.", "danger")
            return redirect(url_for("submit_complaint"))

        db = get_db()
        if not db:
            flash("Database connection failed.", "danger")
            return redirect(url_for("submit_complaint"))

        cursor = db.cursor()

        try:
            cursor.execute("""
                INSERT INTO complaints
                (student_name, student_email, department, subject,
                 description, status)
                VALUES (%s, %s, %s, %s, %s, 'Pending')
            """, (
                session.get("name"),
                session.get("email"),
                department,
                title,
                description
            ))

            db.commit()
            flash("Complaint submitted successfully.", "success")

        except Error as e:
            db.rollback()
            print("Complaint Insert Error:", e)
            flash("Unable to submit complaint.", "danger")

        finally:
            cursor.close()
            db.close()

        return redirect(url_for("my_complaints"))

    return render_template("submit_complaint.html")


@app.route("/my-complaints")
def my_complaints():
    if not student_required():
        return redirect(url_for("login"))

    db = get_db()
    complaints = []

    if db:
        cursor = db.cursor(dictionary=True)
        try:
            cursor.execute("""
                SELECT id, student_name, student_email, department,
                       subject AS title, description, status,
                       hod_reply, created_at
                FROM complaints
                WHERE student_email = %s
                ORDER BY created_at DESC
            """, (session.get("email"),))
            complaints = cursor.fetchall()
        except Error as e:
            print("My Complaints Error:", e)
        finally:
            cursor.close()
            db.close()

    return render_template("my_complaints.html", complaints=complaints)


def get_department_complaints(department):
    db = get_db()
    complaints = []

    if not db:
        return complaints

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute("""
            SELECT id, student_name, student_email, department,
                   subject AS title, description, status,
                   hod_reply, created_at
            FROM complaints
            WHERE LOWER(TRIM(department)) = LOWER(TRIM(%s))
            ORDER BY created_at DESC
        """, (department,))
        complaints = cursor.fetchall()
    except Error as e:
        print("Department Complaints Error:", e)
    finally:
        cursor.close()
        db.close()

    return complaints


@app.route("/faculty")
def faculty_dashboard():
    if not faculty_required():
        return redirect(url_for("login"))

    complaints = get_department_complaints(
        (session.get("department") or "").strip()
    )

    total_assigned = len(complaints)
    pending_assigned = sum(c["status"] == "Pending" for c in complaints)
    in_progress_assigned = sum(c["status"] == "In Progress" for c in complaints)
    resolved_assigned = sum(c["status"] == "Resolved" for c in complaints)

    return render_template(
        "faculty_dashboard.html",
        complaints=complaints,
        total_assigned=total_assigned,
        pending_assigned=pending_assigned,
        in_progress_assigned=in_progress_assigned,
        resolved_assigned=resolved_assigned
    )


@app.route("/faculty/complaints")
def assigned_complaints():
    if not faculty_required():
        return redirect(url_for("login"))

    department = (session.get("department") or "").strip()
    complaints = get_department_complaints(department)

    return render_template(
        "assigned_complaints.html",
        complaints=complaints
    )


@app.route("/faculty/update/<int:complaint_id>", methods=["POST"])
def faculty_update_complaint(complaint_id):
    if not faculty_required():
        return redirect(url_for("login"))

    status = request.form.get("status", "In Progress")

    allowed_status = [
        "Pending", "In Progress", "Resolved", "Rejected"
    ]

    if status not in allowed_status:
        status = "In Progress"

    department = (session.get("department") or "").strip()
    db = get_db()

    if db:
        cursor = db.cursor()

        try:
            cursor.execute("""
                UPDATE complaints
                SET status = %s
                WHERE id = %s
                AND LOWER(TRIM(department)) = LOWER(TRIM(%s))
            """, (status, complaint_id, department))

            db.commit()

            if cursor.rowcount > 0:
                flash("Complaint status updated.", "success")
            else:
                flash("Complaint not found in your department.", "warning")

        except Error as e:
            db.rollback()
            print("Faculty Update Error:", e)
            flash("Unable to update complaint.", "danger")

        finally:
            cursor.close()
            db.close()

    return redirect(url_for("assigned_complaints"))


@app.route("/hod")
def hod_dashboard():
    if not hod_required():
        return redirect(url_for("login"))

    department = (session.get("department") or "").strip()
    complaints = get_department_complaints(department)

    total_complaints = len(complaints)
    pending_complaints = sum(c["status"] == "Pending" for c in complaints)
    in_progress_complaints = sum(c["status"] == "In Progress" for c in complaints)
    resolved_complaints = sum(c["status"] == "Resolved" for c in complaints)
    rejected_complaints = sum(c["status"] == "Rejected" for c in complaints)

    return render_template(
        "hod_dashboard.html",
        complaints=complaints,
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints,
        rejected_complaints=rejected_complaints,
        department=department
    )


@app.route("/hod/complaints")
def department_complaints():
    if not hod_required():
        return redirect(url_for("login"))

    department = (session.get("department") or "").strip()
    complaints = get_department_complaints(department)

    return render_template(
        "department_complaints.html",
        complaints=complaints,
        department=department
    )


@app.route("/hod/complaints/update/<int:complaint_id>", methods=["POST"])
def hod_update_complaint(complaint_id):
    if not hod_required():
        return redirect(url_for("login"))

    status = request.form.get("status", "Pending")
    hod_reply = request.form.get("hod_reply", "").strip()

    allowed_status = [
        "Pending", "In Progress", "Resolved", "Rejected"
    ]

    if status not in allowed_status:
        status = "Pending"

    department = (session.get("department") or "").strip()
    db = get_db()

    if not db:
        flash("Database connection failed.", "danger")
        return redirect(url_for("department_complaints"))

    cursor = db.cursor()

    try:
        cursor.execute("""
            UPDATE complaints
            SET status = %s, hod_reply = %s
            WHERE id = %s
            AND LOWER(TRIM(department)) = LOWER(TRIM(%s))
        """, (
            status,
            hod_reply,
            complaint_id,
            department
        ))

        db.commit()

        if cursor.rowcount > 0:
            flash(
                "Complaint status and reply updated successfully.",
                "success"
            )
        else:
            flash(
                "Complaint not found in your department.",
                "warning"
            )

    except Error as e:
        db.rollback()
        print("HOD UPDATE ERROR:", e)
        flash("Unable to update complaint.", "danger")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("department_complaints"))


@app.route("/admin")
def admin_dashboard():
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db()
    complaints = []
    total_users = 0

    if db:
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id, student_name, student_email, department,
                       subject AS title, description, status,
                       hod_reply, created_at
                FROM complaints
                ORDER BY created_at DESC
            """)
            complaints = cursor.fetchall()

            cursor.execute("SELECT COUNT(*) AS total FROM users")
            result = cursor.fetchone()

            if result:
                total_users = result["total"]

        except Error as e:
            print("Admin Dashboard Error:", e)

        finally:
            cursor.close()
            db.close()

    total_complaints = len(complaints)
    pending_complaints = sum(c["status"] == "Pending" for c in complaints)
    in_progress_complaints = sum(c["status"] == "In Progress" for c in complaints)
    resolved_complaints = sum(c["status"] == "Resolved" for c in complaints)
    rejected_complaints = sum(c["status"] == "Rejected" for c in complaints)

    return render_template(
        "admin_dashboard.html",
        complaints=complaints,
        total_users=total_users,
        total_complaints=total_complaints,
        pending_complaints=pending_complaints,
        in_progress_complaints=in_progress_complaints,
        resolved_complaints=resolved_complaints,
        rejected_complaints=rejected_complaints
    )


@app.route("/admin/users")
def manage_users():
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db()
    users = []

    if db:
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id, name, email, role, department, created_at
                FROM users
                ORDER BY created_at DESC
            """)
            users = cursor.fetchall()
        except Error as e:
            print("Manage Users Error:", e)
        finally:
            cursor.close()
            db.close()

    return render_template("manage_users.html", users=users)


@app.route("/admin/users/add", methods=["POST"])
def add_user():
    if not admin_required():
        return redirect(url_for("login"))

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip()
    password = request.form.get("password", "kunal")
    role = request.form.get("role", "student")
    department = request.form.get("department", "").strip()

    if not name or not email:
        flash("Name and email are required.", "danger")
        return redirect(url_for("manage_users"))

    allowed_roles = ["student", "faculty", "hod", "admin"]

    if role not in allowed_roles:
        role = "student"

    if department and department not in DEPARTMENTS:
        flash("Invalid department.", "danger")
        return redirect(url_for("manage_users"))

    db = get_db()

    if not db:
        flash("Database connection failed.", "danger")
        return redirect(url_for("manage_users"))

    cursor = db.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT id FROM users WHERE email = %s",
            (email,)
        )

        if cursor.fetchone():
            flash("User already exists.", "warning")
            return redirect(url_for("manage_users"))

        hashed_password = generate_password_hash(password)

        cursor.execute("""
            INSERT INTO users
            (name, email, password, role, department)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            name,
            email,
            hashed_password,
            role,
            department
        ))

        db.commit()
        flash("User added successfully.", "success")

    except Error as e:
        db.rollback()
        print("Add User Error:", e)
        flash("Unable to add user.", "danger")

    finally:
        cursor.close()
        db.close()

    return redirect(url_for("manage_users"))


@app.route("/admin/users/delete/<int:user_id>", methods=["POST"])
def delete_user(user_id):
    if not admin_required():
        return redirect(url_for("login"))

    if user_id == session.get("user_id"):
        flash("You cannot delete your own account.", "danger")
        return redirect(url_for("manage_users"))

    db = get_db()

    if db:
        cursor = db.cursor()

        try:
            cursor.execute(
                "DELETE FROM users WHERE id = %s",
                (user_id,)
            )

            db.commit()

            if cursor.rowcount > 0:
                flash("User deleted successfully.", "success")
            else:
                flash("User not found.", "warning")

        except Error as e:
            db.rollback()
            flash(
                "User cannot be deleted because related records exist.",
                "danger"
            )
            print("Delete User Error:", e)

        finally:
            cursor.close()
            db.close()

    return redirect(url_for("manage_users"))


@app.route("/admin/complaints")
def manage_complaints():
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db()
    complaints = []

    if db:
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT id, student_name, student_email, department,
                       subject AS title, description, status,
                       hod_reply, created_at
                FROM complaints
                ORDER BY created_at DESC
            """)
            complaints = cursor.fetchall()
        except Error as e:
            print("Manage Complaints Error:", e)
        finally:
            cursor.close()
            db.close()

    return render_template(
        "manage_complaints.html",
        complaints=complaints
    )


@app.route("/admin/complaints/update/<int:complaint_id>", methods=["POST"])
def admin_update_complaint(complaint_id):
    if not admin_required():
        return redirect(url_for("login"))

    status = request.form.get("status", "Pending")

    allowed_status = [
        "Pending", "In Progress", "Resolved", "Rejected"
    ]

    if status not in allowed_status:
        status = "Pending"

    db = get_db()

    if db:
        cursor = db.cursor()

        try:
            cursor.execute("""
                UPDATE complaints
                SET status = %s
                WHERE id = %s
            """, (status, complaint_id))

            db.commit()
            flash("Complaint updated successfully.", "success")

        except Error as e:
            db.rollback()
            print("Admin Update Complaint Error:", e)
            flash("Unable to update complaint.", "danger")

        finally:
            cursor.close()
            db.close()

    return redirect(url_for("manage_complaints"))


@app.route("/admin/analytics")
def analytics():
    if not admin_required():
        return redirect(url_for("login"))

    db = get_db()
    complaints = []

    category_labels = []
    category_values = []

    department_labels = []
    department_values = []

    monthly_labels = []
    monthly_submitted = []
    monthly_resolved = []

    priority_labels = []
    priority_values = []

    if db:
        cursor = db.cursor(dictionary=True)

        try:
            cursor.execute("""
                SELECT *
                FROM complaints
                ORDER BY created_at DESC
            """)
            complaints = cursor.fetchall()

            cursor.execute("""
                SELECT department, COUNT(*) AS total
                FROM complaints
                GROUP BY department
            """)

            department_data = cursor.fetchall()

            for row in department_data:
                department_labels.append(row["department"])
                department_values.append(row["total"])

        except Error as e:
            print("Analytics Error:", e)

        finally:
            cursor.close()
            db.close()

    total = len(complaints)
    resolved = sum(c["status"] == "Resolved" for c in complaints)
    pending = sum(c["status"] == "Pending" for c in complaints)
    in_progress = sum(c["status"] == "In Progress" for c in complaints)
    rejected = sum(c["status"] == "Rejected" for c in complaints)

    return render_template(
        "analytics.html",
        complaints=complaints,
        total=total,
        resolved=resolved,
        pending=pending,
        in_progress=in_progress,
        rejected=rejected,
        category_labels=category_labels,
        category_values=category_values,
        department_labels=department_labels,
        department_values=department_values,
        monthly_labels=monthly_labels,
        monthly_submitted=monthly_submitted,
        monthly_resolved=monthly_resolved,
        priority_labels=priority_labels,
        priority_values=priority_values
    )


@app.route("/logout")
def logout():
    session.clear()
    flash("You have been logged out.", "info")
    return redirect(url_for("login"))


@app.errorhandler(404)
def page_not_found(error):
    return render_template("index.html"), 404


@app.errorhandler(413)
def file_too_large(error):
    flash("File size must be less than 5 MB.", "danger")
    return redirect(url_for("submit_complaint"))


@app.errorhandler(500)
def internal_error(error):
    print("Internal Server Error:", error)
    return """
    <h2>Internal Server Error</h2>
    <p>Please check the terminal for the exact error.</p>
    """, 500


if __name__ == "__main__":
    print("=" * 60)
    print("SMART COLLEGE GRIEVANCE MANAGEMENT SYSTEM")
    print("R. C. Patel College of Engineering and Polytechnic")
    print("=" * 60)
    print("Server: http://127.0.0.1:5000")
    print("=" * 60)

    app.run(
        debug=True,
        host="127.0.0.1",
        port=5000
    )
