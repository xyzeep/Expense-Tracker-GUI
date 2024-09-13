# Importing all the essential libraries
import datetime
import customtkinter as ctk
import sqlite3
from CTkMessagebox import CTkMessagebox
from tktooltip import ToolTip
from PIL import Image
import webbrowser
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from subprocess import Popen
import csv
import matplotlib.pyplot as plt
# 
# to fix a fatal bug
fig = None
# Today's info
today = datetime.date.today()

# Global varaibles which need to be modified later
current_user = None
current_username = None
current_user_firstname = None

# Defining all the images
logo1 = ctk.CTkImage(dark_image=Image.open("assets/logo1.png"), size=(70, 70))
logo2 = ctk.CTkImage(dark_image=Image.open("assets/logo2.png"), size=(90, 90))
eyeopen = ctk.CTkImage(dark_image=Image.open("assets/view.png"), size=(36, 36))
eyehide = ctk.CTkImage(dark_image=Image.open("assets/hide.png"), size=(36, 36))
illustration = ctk.CTkImage(dark_image=Image.open(
    "assets/illustration.png"), size=(772, 842))
usericon = ctk.CTkImage(dark_image=Image.open(
    "assets/usericon.png"), size=(70, 70))
dashboard_illustration = ctk.CTkImage(dark_image=Image.open(
    "assets/dashillustrate.webp"), size=(707, 241))
plusimage = ctk.CTkImage(dark_image=Image.open(
    "assets/plus.png"), size=(46, 46))
aboutusimage = ctk.CTkImage(
    dark_image=Image.open("assets/info.png"), size=(34, 34))
logoutimage = ctk.CTkImage(dark_image=Image.open(
    "assets/logout.png"), size=(40, 40))
backimage = ctk.CTkImage(dark_image=Image.open(
    "assets/back.png"), size=(30, 30))
deleteicon = ctk.CTkImage(dark_image=Image.open(
    "assets/deleteicon.png"), size=(25, 25))

### Defining all the functions needed ###


def on_closing():
    plt.close(fig)
    root.destroy()


def plot_expenses_by_category():

    # Connect to the SQLite database
    conn = sqlite3.connect("expensetracker.db")
    cursor = conn.cursor()

    # Query to sum the expenses for each category
    cursor.execute(
        "SELECT category, SUM(price) FROM expensedetails WHERE user_id = ? GROUP BY category", (current_user,))
    results = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Check if there are any expenses
    if not results:
        return

    # Extract categories and corresponding total expenses
    categories = [row[0] for row in results]
    amounts = [row[1] for row in results]

    # Clear the frame before adding the new plot
    for widget in plot_frame.winfo_children():
        widget.destroy()

    def func(pct, allvalues):
        return f'{pct:.1f}%'

    # Create a figure for the pie chart
    global fig
    fig, ax = plt.subplots(figsize=(12, 8.1))
    wedges, texts, autotexts = ax.pie(
        amounts,
        labels=None,
        colors=['#ff6f61', '#6b5b95', '#88b04b', '#f7cac9', '#92a8d1'],
        # Use custom function for percentage labels
        autopct=lambda pct: func(pct, amounts),
        startangle=140,
        wedgeprops=dict(width=0.4),  # Increase width here for thicker wedges
        pctdistance=1.15  # Position percentage labels further from the center
    )
    ax.set_title("Expenses by Category", fontsize=30,
                 fontweight='bold', color='#333d79', fontname='Calibri')

    ax.legend(
        wedges,  # Use the wedge objects for the legend
        categories,  # Labels for the legend
        title="Categories",
        title_fontsize='18',
        loc="center left",
        # Position the legend outside the pie chart
        bbox_to_anchor=(-0.4, -0.4, 2, 1),
        fontsize='16'
    )

    for autotext in autotexts:
        autotext.set_fontsize(18)
        autotext.set_color('black')

    # Embed the plot into the customtkinter frame
    canvas = FigureCanvasTkAgg(fig, master=plot_frame,)
    canvas.draw()
    canvas.get_tk_widget().pack(fill=ctk.BOTH, expand=True,)


def export_csv():
    """
    Export all expenses of a user to a CSV file.
    """

    # Connect to the SQLite database
    conn = sqlite3.connect("expensetracker.db")
    cursor = conn.cursor()

    # Query to select the relevant expense details for the user

    cursor.execute(
        "SELECT expense_name, price, category, date FROM expensedetails WHERE user_id = ?", (current_user,))
    expenses = cursor.fetchall()

    print(expenses)

    # Check if there are any expenses to export
    if not expenses:
        return

    # Write the data to a CSV file
    output_file = "expenses_" + current_username + ".csv"
    with open(output_file, mode='w', newline='') as file:
        writer = csv.writer(file)
        # Write the header
        writer.writerow(['Expense', 'Price', 'Category', 'Date'])
        # Write the expense details
        writer.writerows(expenses)

    export_msg = CTkMessagebox(main_frame, title="Export .csv", message=".csv exported successfully!",
                               icon="check", option_2="View", option_1="Okay", fg_color="#fff", button_color="#333d79", text_color="#333d79", font=('Arial', 18, "bold"), bg_color="#fff", button_hover_color="#8B8DE5", button_width=20, button_height=15, title_color="#333d79", border_width=3, width=300, height=80, border_color="#333d79", corner_radius=0)
    export_response = export_msg.get()
    if export_response == "View":
        try:
            # Specify the path to the application you want to use to open the file
            app_path = r"C:\Program Files\Microsoft Office\root\Office16\EXCEL.EXE"  # path for Excel
            Popen([app_path, output_file])  # Open the file in excel


        except Exception as e:
            CTkMessagebox.showerror("Error", f"Unable to open file: {e}")

    conn.close()


def open_link(element):  # Function to open any kind of external links(using webbrowser library)
    if element == "about_us":
        url = "https://youtu.be/VeYgJ9OBu_w"
        webbrowser.open(url)
    elif element == "termsandcondition":
        pdf_url = "E:/project_scratch-Copy/assets/TermsandConditions.pdf"
        webbrowser.open(pdf_url)


def expensedetails_add():  # Function to add expense detials in the database
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS expensedetails(
            expense_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            expense_name TEXT NOT NULL,
            price INT NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL
            )"""
    )
    conn.commit()
    conn.close()
    if not expenses_input.get() or not amount_input.get() or category_input.get() == "Select..." or not date_input.get():
        add_exp_msg.configure(
            text="Please fill out all the required fields and try again.", text_color="red")
        return
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO expensedetails(user_id, expense_name, price, category, date) VALUES (?,?,?,?,?)",

        (current_user, expenses_input.get(), amount_input.get(),
            category_input.get(), date_input.get()),
    )
    conn.commit()
    conn.close()
    add_exp_msg.configure(
        text="Expense added successfully.", text_color="green")

    # emptying the fields after insertion of expense details
    expenses_input.delete(0, ctk.END)
    amount_input.delete(0, ctk.END)
    date_input.delete(0, ctk.END)
    selected_category.set("Select...")


def create_user():  # Function to create a new user(sign up)
    # Connect to SQLite database
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()

    # Create the 'users' table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL,
            first_name TEXT,
            last_name TEXT,
            coventry_id UNIQUE,
            gender
        )
    ''')

    # Fetch the data from the input widgets
    username = username_entry_signup.get()
    password = password_entry_signup.get()
    first_name = first_entry.get()
    last_name = last_entry.get()
    coventry_id = security_answer.get()
    gender = gender_var.get()

    # Check if the username already exists
    cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
    existing_user = cursor.fetchone()

    if existing_user:
        invalid_signup_label.configure(text="Username not available.")
    else:
        # Insert new user details into the table
        cursor.execute('''INSERT INTO users (username, password, first_name, last_name, coventry_id, gender)
            VALUES (?, ?, ?, ?, ?, ?)''', (username, password, first_name, last_name, coventry_id, gender))

        conn.commit()

        invalid_login_label.configure(
            text="Account created successfully!", text_color="Green")
        show_login_frame()
        username_entry_signup.delete(0, ctk.END)
        password_entry_signup.delete(0, ctk.END)
        first_entry.delete(0, ctk.END)
        last_entry.delete(0, ctk.END)
        security_answer.delete(0, ctk.END)
        gender_var.set(None)

    # Close the database connection
    conn.close()


def toggle_password(entry, toggle_button):  # Function to toggle password visibility
    if entry.cget("show") == "*":
        toggle_button.configure(image=eyehide)
        entry.configure(show="")
    else:
        toggle_button.configure(image=eyeopen)
        entry.configure(show="*")


def reset_password():  # Function to reset users' password
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()

    # Check if the username exists
    cursor.execute('SELECT coventry_id FROM users WHERE username = ?',
                   (username_reset_frame.get(),))
    result = cursor.fetchone()

    if result:
        user_coventry_id = result[0]

        if user_coventry_id == coventry_id_reset_frame.get():
            # Replace with value from password entry box
            new_password = new_password_reset_frame.get()

            cursor.execute('UPDATE users SET password = ? WHERE username = ?',
                           (new_password, username_reset_frame.get()))
            conn.commit()
            show_login_frame()
            invalid_login_label.configure(
                text="Password reset successfully!", text_color="Green")
            username_reset_frame.delete(0, ctk.END)
            coventry_id_reset_frame.delete(0, ctk.END)
            new_password_reset_frame.delete(0, ctk.END)
        else:
            reset_pw_error.configure(text="Coventry ID didn't match.")
    else:
        reset_pw_error.configure(text="Please enter a valid username!")

    conn.close()


def logout():  # Function to logout the user
    msg = CTkMessagebox(main_frame, title="Logout", message="Do you want to logout?",
                        icon="question", option_2="Yes", option_1="No", fg_color="#fff", button_color="#333d79", text_color="#333d79", font=('Arial', 18, "bold"), bg_color="#fff", button_hover_color="#8B8DE5", button_width=20, button_height=15, title_color="#333d79", border_width=3, width=300, height=80, border_color="#333d79", corner_radius=0)
    logout_response = msg.get()
    if logout_response == "Yes":
        show_login_frame()
        plt.close(fig)
    elif logout_response == "No":
        pass


def delete_expense(expense_id, label):
    """
    Delete the expense from the database and remove the widget from the Tkinter frame.
    """
    # Connect to the SQLite database
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()

    # Delete the expense from the database
    cursor.execute(
        'DELETE FROM expensedetails WHERE expense_id=?', (expense_id,))
    conn.commit()

    # Close the database connection
    conn.close()

    # Remove the widget from the Tkinter frame
    label.destroy()


def retrieve_allexpensedetails():  # Function to retrieve the expenses and display it on the application

    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()
    cursor.execute(
        'SELECT date FROM expensedetails WHERE user_id=?', (current_user,))
    allexpensedates = cursor.fetchall()
    month_dict = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
                  "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12", }

    selected_month_dates = []
    selected_month_dates.clear()

    for widget in view_exp_frame.winfo_children():
        if isinstance(widget, ctk.CTkButton) and widget.cget('image') == deleteicon:
            widget.destroy()

    for widget in table_frame.winfo_children():
        widget.destroy()

    for i in allexpensedates:
        if i[0][5:7] == (month_dict[selected_month.get()]):
            selected_month_dates.append(i[0])

    # List of all items users made their expenses on
    placeholders = ','.join('?' for _ in selected_month_dates)
    cursor.execute(
        f'SELECT expense_name FROM expensedetails WHERE user_id=? AND date IN ({placeholders}) ORDER BY STRFTIME("%Y-%m-%d", date) ASC', (current_user, *selected_month_dates))
    user_allexpensesitems = cursor.fetchall()

    # to get one on one expenses name
    for i in range(len(selected_month_dates)):
        expense_items = ctk.CTkLabel(
            table_frame, text=user_allexpensesitems[i], fg_color="#C7CBE5", width=200, height=50, font=('Calibri', 24, "bold"), text_color="black")
        expense_items.grid(row=i, column=0, padx=0.95)

    cursor.execute(
        f'SELECT price FROM expensedetails WHERE user_id=? AND date IN ({placeholders}) ORDER BY STRFTIME("%Y-%m-%d", date) ASC', (current_user, *selected_month_dates))
    user_allprices = cursor.fetchall()

    # to get one on one
    for i in range(len(selected_month_dates)):
        expense_items_price = ctk.CTkLabel(
            table_frame, text=user_allprices[i], fg_color="#C7CBE5", width=200, height=50, font=('Calibri', 24, "bold"), text_color="black")
        expense_items_price.grid(row=i, column=1, padx=0.95)

    cursor.execute(
        f'SELECT category FROM expensedetails WHERE user_id=? AND date IN ({placeholders}) ORDER BY STRFTIME("%Y-%m-%d", date) ASC', (current_user, *selected_month_dates))
    user_allcategories = cursor.fetchall()

    # to get one on one
    for i in range(len(selected_month_dates)):
        expense_items_categories = ctk.CTkLabel(
            table_frame, text=user_allcategories[i], fg_color="#C7CBE5", width=205, height=50, font=('Calibri', 24, "bold"), text_color="black")
        expense_items_categories.grid(row=i, column=2, padx=0.95)

    cursor.execute(
        f'SELECT date FROM expensedetails WHERE user_id=? AND date IN ({placeholders}) ORDER BY STRFTIME("%Y-%m-%d", date) ASC', (current_user, *selected_month_dates))
    user_alldates = cursor.fetchall()

    # to get one on one
    for i in range(len(selected_month_dates)):
        expense_items_dates = ctk.CTkLabel(
            table_frame, text=user_alldates[i], fg_color="#C7CBE5", width=200, height=50, font=('Calibri', 24, "bold"), text_color="black")
        expense_items_dates.grid(row=i, column=3, padx=1)

    cursor.execute(
        f'SELECT expense_id FROM expensedetails WHERE user_id=? AND date IN ({placeholders}) ORDER BY STRFTIME("%Y-%m-%d", date) ASC', (current_user, *selected_month_dates))
    user_allexpense_ids = cursor.fetchall()

    for i in range(len(selected_month_dates)):
        del_btn_name = "del_" + str(i)

        del_btn_name = ctk.CTkButton(
            view_exp_frame, image=deleteicon, text="", hover_color="#fff", bg_color="#fff", fg_color="#fff", width=20, font=('Calibri', 24, "bold"), text_color="black", command=lambda id=user_allexpense_ids[i][0]: delete_expense(id))
        del_btn_name.place(relx=0.018, rely=0.2 + i * 0.06)

    conn.commit()
    conn.close()


def delete_expense(id):

    delete_confirm = CTkMessagebox(main_frame, title="Confirm Delete", message="Do you really want to delete this record?",
                                   icon="check", option_2="Yes", option_1="No", fg_color="#fff", button_color="#333d79", text_color="#333d79", font=('Arial', 18, "bold"), bg_color="#fff", button_hover_color="#8B8DE5", button_width=20, button_height=15, title_color="#333d79", border_width=3, width=300, height=80, border_color="#333d79", corner_radius=0)
    delete_response = delete_confirm.get()
    if delete_response == "Yes":
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()

        # SQL query to delete the record
        cursor.execute(
            'DELETE FROM expensedetails WHERE expense_id = ?', (id,))
        # Commit the changes
        conn.commit()

        retrieve_allexpensedetails()
    else:
        pass


def verify_user():  # Function to check if the user already exists before logging in
    # Connect to SQLite database
    conn = sqlite3.connect('expensetracker.db')
    cursor = conn.cursor()
    username = username_entry.get()
    password = password_entry.get()
    # Check if the user exists with the provided username and password
    cursor.execute(
        'SELECT * FROM users WHERE username = ? AND password = ?', (username, password))
    user = cursor.fetchone()
    # Close the database connection
    conn.close()
    if user:
        global current_user
        global current_username
        global current_user_firstname
        show_add_expenese_frame()
        current_user = user[0]
        username_entry.delete(0, ctk.END)
        password_entry.delete(0, ctk.END)
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT username FROM users WHERE id = ?', (current_user,))
        current_username = cursor.fetchone()[0]
        user_name.configure(text=current_username)
        conn.commit()
        conn.close()
        conn = sqlite3.connect('expensetracker.db')
        cursor = conn.cursor()
        cursor.execute(
            'SELECT first_name FROM users WHERE id = ?', (current_user,))
        current_user_firstname = cursor.fetchone()[0]
        firstname.configure(text=current_user_firstname)
        conn.commit()
        conn.close()
    else:
        invalid_login_label.configure(
            text="Invalid inputs. Please try again.", text_color="red")


def validate_signup():  # Function to validate sign in(i.e to make sure that the inputs are not empty)
    # Get the values from the input fields
    username = username_entry_signup.get()
    password = password_entry_signup.get()
    first_name = first_entry.get()
    security_answer_text = security_answer.get()
    gender_value = gender_var.get()

    # Check if any field is empty
    if not username or not password or not first_name or not security_answer_text or not gender_value:
        invalid_signup_label.configure(
            text="Please fill out all the required fields and try again.", text_color="red")
    else:
        create_user()
        return


def hide_indicators():  # Function to hide the indication in the nav menu
    add_exp_btn.configure(text_color="white", fg_color="#333d79")
    view_exp_btn.configure(text_color="white", fg_color="#333d79")
    overview_btn.configure(text_color="white", fg_color="#333d79")


def indicate(btn):  # Function to show the indication in the nav menu
    hide_indicators()
    btn.configure(text_color="#333d79", fg_color="white")


def show_login_frame():  # Fucntion to pack the login frame (Default frame)
    global current_user
    global current_username
    current_user = None
    current_user = None
    signup_frame.pack_forget()
    main_frame.pack_forget()
    reset_pw_frame.pack_forget()
    login_frame.pack(fill="both", expand=True)


def show_reset_frame():  # Function to pack reset frame (activates when clicked on the forgot password button from login page)
    login_frame.pack_forget()
    main_frame.pack_forget()
    reset_pw_frame.pack(fill="both", expand=True)


def show_signup_frame():  # Function to pack the signup frame (activates when clicked on the signup button from login page)
    login_frame.pack_forget()
    main_frame.pack_forget()
    signup_frame.pack(fill="both", expand=True)


def show_add_expenese_frame():  # Function to show the Add expense page (this is the deafault frame which gets shown after loggin in)
    indicate(add_exp_btn)
    login_frame.pack_forget()
    signup_frame.pack_forget()
    overview_frame.place_forget()
    plt.close(fig)
    view_exp_frame.place_forget()
    main_frame.pack(fill="both", expand=True)
    add_exp_frame.place(relx=1, rely=0, anchor="ne")


def show_view_expense_frame():  # Function to show the view expense page after cliking on the view expense button from the nav menu
    indicate(view_exp_btn)
    add_exp_frame.place_forget()
    overview_frame.place_forget()
    view_exp_frame.place(relx=1, rely=0, anchor="ne")
    retrieve_allexpensedetails()
    plt.close(fig)


def show_overview_frame():  # Function to show the view expense page after cliking on the view expense button from the nav menu
    indicate(overview_btn)
    add_exp_frame.place_forget()
    view_exp_frame.pack_forget
    plot_expenses_by_category()
    overview_frame.place(relx=1, rely=0, anchor="ne")


###### Initializing the main root ctk window ######
root = ctk.CTk()
root.title("Expense Tracker")
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()


# this block of code sets the app in fullscreen windowed mode
# because tkinter's placing/packing methods are somewhat annoying to deal with, we decided to not let the users resize the app
root.resizable(False, False)
root.after(3, lambda: root.state("zoomed"))

# setting the theme of our application/and its widgets
root._set_appearance_mode("light")
# setting the app icon as blank because it didn't look good when we put one
root.iconbitmap(bitmap="assets/blank.ico")

##### Login Page Frame #####
login_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)

login_illustration = ctk.CTkLabel(login_frame, image=illustration, text="")
login_illustration.place(relx=1, rely=0, anchor="ne")

top_logo_login = ctk.CTkLabel(login_frame, image=logo1, text="",
                              corner_radius=20, fg_color="white", bg_color="white", width=1)
top_logo_login.place(relx=0.05, rely=0.07, anchor="center")

branding_login = ctk.CTkLabel(login_frame, text="Expense Tracker",
                              text_color="#333d79", font=('Arial', 36, "bold"), bg_color="white")
branding_login.place(relx=0.08, rely=0.07, anchor="w")

welcome_text = ctk.CTkLabel(login_frame, text="Welcome!", text_color="#333d79", font=(
    'Verdana', 54, "bold"), bg_color="white")
welcome_text.place(relx=0.0535, rely=0.245, anchor="w")

login_text = ctk.CTkLabel(login_frame, text="Login to your account",
                          text_color="#333d79", font=('Calibri', 30, "bold"), bg_color="white")
login_text.place(relx=0.0535, rely=0.39, anchor="w")

invalid_login_label = ctk.CTkLabel(
    login_frame, text="", text_color="red", font=("Calibri", 18), bg_color="white")
invalid_login_label.place(relx=0.055, rely=0.577, anchor="nw")

username_entry = ctk.CTkEntry(login_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Username",
                              placeholder_text_color="Grey", font=("Calibri", 20), width=485, corner_radius=7, text_color="black", height=48)
username_entry.place(relx=0.0535, rely=0.43, anchor="nw")

password_entry = ctk.CTkEntry(login_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Password",
                              show="*", placeholder_text_color="Grey", font=("Calibri", 20), width=485, corner_radius=7, text_color="black", height=48)
password_entry.place(relx=0.0535, rely=0.52, anchor="nw")

password_toggle_btn = ctk.CTkButton(login_frame, image=eyehide, fg_color="#E0E2EB", bg_color="#E0E2EB",
                                    text="", width=10, height=5, hover_color="#E0E2EB", command=lambda: toggle_password(password_entry, password_toggle_btn))
password_toggle_btn.place(relx=0.33, rely=0.523, anchor="nw")

login_button = ctk.CTkButton(login_frame, text="Login", fg_color="#333d79", text_color="#faebef", bg_color="White",
                             corner_radius=7, width=485, height=48, font=("Calibri", 20, "bold"), hover_color="#333d79", command=verify_user)
login_button.place(relx=0.0535, rely=0.61, anchor="nw")

signuptext = ctk.CTkLabel(login_frame, text="Don't have an account?", font=(
    "Calibri", 22), text_color="#333d79", fg_color="White", bg_color="White")
signuptext.place(relx=0.0535, rely=0.67, anchor="nw")
signupbutton = ctk.CTkButton(login_frame, text="Sign up!", font=("Calibri", 22, "bold"), text_color="#333d79",
                             fg_color="White", bg_color="white", width=1, hover_color="white", command=show_signup_frame)
signupbutton.place(relx=0.192, rely=0.667, anchor="nw")

forgot_button = ctk.CTkButton(login_frame, text="Forgot password?", font=("Calibri", 20, "bold"), text_color="#333d79",
                              fg_color="White", bg_color="white", width=1, hover_color="white", command=show_reset_frame)
forgot_button.place(relx=0.265, rely=0.67, anchor="nw")


##### Signup Page frame #####
signup_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)

signup_illustration = ctk.CTkLabel(signup_frame, image=illustration, text="")
signup_illustration.place(relx=1, rely=0, anchor="ne")

top_logo_signup = ctk.CTkLabel(signup_frame, image=logo1, text="",
                               corner_radius=20, fg_color="white", bg_color="white", width=1)
top_logo_signup.place(relx=0.05, rely=0.07, anchor="center")

branding_signup = ctk.CTkLabel(signup_frame, text="Expense Tracker",
                               text_color="#333d79", font=('Arial', 36, "bold"), bg_color="white")
branding_signup.place(relx=0.08, rely=0.07, anchor="w")

signup_text = ctk.CTkLabel(signup_frame, text="Create a new account",
                           text_color="#333d79", font=('Calibri', 36, "bold"), bg_color="white")
signup_text.place(relx=0.0535, rely=0.24, anchor="nw")

username_entry_signup = ctk.CTkEntry(signup_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Username*",
                                     placeholder_text_color="Grey", font=("Calibri", 20), width=280, corner_radius=7, text_color="black", height=48)
username_entry_signup.place(relx=0.0535, rely=0.32, anchor="nw")

password_entry_signup = ctk.CTkEntry(signup_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Password",
                                     show="*", placeholder_text_color="Grey", font=("Calibri", 20), width=280, corner_radius=7, text_color="black", height=48)
password_entry_signup.place(relx=0.246, rely=0.32, anchor="nw")

password_toggle_signup = ctk.CTkButton(signup_frame, image=eyehide, fg_color="#E0E2EB", bg_color="#E0E2EB",
                                       text="", width=10, height=5, hover_color="#E0E2EB", command=lambda: toggle_password(password_entry_signup, password_toggle_signup))
password_toggle_signup.place(relx=0.39, rely=0.323, anchor="nw")

first_entry = ctk.CTkEntry(signup_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="First name*",
                           placeholder_text_color="Grey", font=("Calibri", 20), width=280, corner_radius=7, text_color="black", height=48)
first_entry.place(relx=0.0535, rely=0.4, anchor="nw")

last_entry = ctk.CTkEntry(signup_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Last name",
                          placeholder_text_color="Grey", font=("Calibri", 20), width=280, corner_radius=7, text_color="black", height=48)
last_entry.place(relx=0.246, rely=0.4, anchor="nw")

# Security Question
security_qn = ctk.CTkLabel(signup_frame, text="Security Question", text_color="#333d79", font=(
    'Calibri', 24, "bold"), bg_color="white")
security_qn.place(relx=0.0535, rely=0.475, anchor="nw")

security_answer = ctk.CTkEntry(signup_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="What is your Coventry ID?",
                               placeholder_text_color="Grey", font=("Calibri", 20), width=280, corner_radius=7, text_color="black", height=48)
security_answer.place(relx=0.0535, rely=0.517, anchor="nw")

# Variable to store the selected gender #
gender_var = ctk.StringVar()
gender_label = ctk.CTkLabel(signup_frame, text="Gender", text_color="#333d79", font=(
    'Calibri', 24, "bold"), bg_color="white")
gender_label.place(relx=0.246, rely=0.475, anchor="nw")

male = ctk.CTkRadioButton(signup_frame, text="Male", value="male", variable=gender_var, radiobutton_width=20, radiobutton_height=20,
                          corner_radius=30, border_width_unchecked=3, bg_color="white", border_width_checked=6, fg_color="#333d79", border_color="#5F6368",
                          cursor="", hover=True, hover_color="#333d79", text_color="#333d79", font=("Calibri", 20, "bold"))
male.place(relx=0.246, rely=0.53, anchor="nw")

female = ctk.CTkRadioButton(signup_frame, text="Female", value="female", variable=gender_var, radiobutton_width=20, radiobutton_height=20,
                            corner_radius=30, border_width_unchecked=3, bg_color="white", border_width_checked=6, fg_color="#333d79", border_color="#5F6368",
                            cursor="arrow", hover=True, hover_color="#333d79", text_color="#333d79", font=("Calibri", 20, "bold"))
female.place(relx=0.3, rely=0.53, anchor="nw")

other = ctk.CTkRadioButton(signup_frame, text="Other", value="other", variable=gender_var, radiobutton_width=20, radiobutton_height=20,
                           corner_radius=30, border_width_unchecked=3, bg_color="white", border_width_checked=6, fg_color="#333d79", border_color="#5F6368",
                           cursor="arrow", hover=True, hover_color="#333d79", text_color="#333d79", font=("Calibri", 20, "bold"))
other.place(relx=0.37, rely=0.53, anchor="nw")

# signup button
signup_button_frame = ctk.CTkButton(signup_frame, text="Sign up", fg_color="#333d79", text_color="#faebef", bg_color="White",
                                    corner_radius=7, width=575, height=48, font=("Calibri", 20, "bold"), hover_color="#333d79", command=validate_signup)
signup_button_frame.place(relx=0.0535, rely=0.595, anchor="nw")

# terms and conditions
terms_text = ctk.CTkLabel(signup_frame, text="By signing up, you agree to our",
                          font=("Calibri", 20), text_color="#333d79", fg_color="White", bg_color="White")
terms_text.place(relx=0.175, rely=0.99, anchor="s")
termsandcondition = ctk.CTkButton(signup_frame, text="Terms and Conditions.",
                                  font=("Calibri", 20, "bold"), hover_color="White", text_color="#333d79", fg_color="White", bg_color="White", command=lambda: open_link("termsandcondition"))
termsandcondition.place(relx=0.32, rely=0.99, anchor="s")

# invalid message label
invalid_signup_label = ctk.CTkLabel(
    signup_frame, text="", text_color="red", font=("Calibri", 18), bg_color="white")
invalid_signup_label.place(relx=0.0535, rely=0.287, anchor="nw")


## go back to login page##
loginnote = ctk.CTkLabel(signup_frame, text="Already have an account?", font=(
    "Calibri", 26), text_color="#333d79", fg_color="White", bg_color="White")
loginnote.place(relx=0.0535, rely=0.6555, anchor="nw")
loginbutton_frame = ctk.CTkButton(signup_frame, text="Login", font=("Calibri", 26, "bold"), text_color="#333d79",
                                  fg_color="White", bg_color="white", width=1, hover_color="white", command=show_login_frame)
loginbutton_frame.place(relx=0.227, rely=0.654, anchor="nw")


######### reset password frame starts here#########
reset_pw_frame = ctk.CTkFrame(root, fg_color="white", corner_radius=0)

reset_illustration = ctk.CTkLabel(reset_pw_frame, image=illustration, text="")
reset_illustration.place(relx=1, rely=0, anchor="ne")

top_logo_reset = ctk.CTkLabel(reset_pw_frame, image=logo1, text="",
                              corner_radius=20, fg_color="white", bg_color="white", width=1)
top_logo_reset.place(relx=0.05, rely=0.07, anchor="center")

branding_reset = ctk.CTkLabel(reset_pw_frame, text="Expense Tracker",
                              text_color="#333d79", font=('Arial', 36, "bold"), bg_color="white")
branding_reset.place(relx=0.08, rely=0.07, anchor="w")

wegotyourback = ctk.CTkLabel(reset_pw_frame, text="We got your back!", text_color="#333d79", font=(
    'Verdana', 54, "bold"), bg_color="white")
wegotyourback.place(relx=0.0535, rely=0.245, anchor="w")

reset_text = ctk.CTkLabel(reset_pw_frame, text="Reset your password",
                          text_color="#333d79", font=('Calibri', 30, "bold"), bg_color="white")
reset_text.place(relx=0.0535, rely=0.38, anchor="w")

username_reset_frame = ctk.CTkEntry(reset_pw_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Username",
                                    placeholder_text_color="Grey", font=("Calibri", 20), width=485, corner_radius=7, text_color="black", height=48)
username_reset_frame.place(relx=0.0535, rely=0.43, anchor="nw")

coventry_id_reset_frame = ctk.CTkEntry(reset_pw_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="Coventry ID",
                                       placeholder_text_color="Grey", font=("Calibri", 20), width=485, corner_radius=7, text_color="black", height=48)
coventry_id_reset_frame.place(relx=0.0535, rely=0.5, anchor="nw")

new_password_reset_frame = ctk.CTkEntry(reset_pw_frame, bg_color="white", border_width=2, fg_color="#E0E2EB", border_color="#ADAEB5", placeholder_text="New password",
                                        show="*", placeholder_text_color="Grey", font=("Calibri", 20), width=485, corner_radius=7, text_color="black", height=48)
new_password_reset_frame.place(relx=0.0535, rely=0.57, anchor="nw")

reset_button = ctk.CTkButton(reset_pw_frame, text="Reset", fg_color="#333d79", text_color="#faebef", bg_color="White",
                             corner_radius=7, width=485, height=48, font=("Calibri", 20, "bold"), hover_color="#333d79", command=reset_password)
reset_button.place(relx=0.0535, rely=0.64, anchor="nw")

reset_pw_error = ctk.CTkLabel(reset_pw_frame, text="", fg_color="white", text_color="red",
                              bg_color="White", width=1, font=("Calibri", 20, "bold"))
reset_pw_error.place(relx=0.0535, rely=0.395, anchor="nw")

back_to_login = ctk.CTkButton(reset_pw_frame, image=backimage, text="Back", fg_color="white", text_color="#333d79",
                              bg_color="White", width=1, font=("Calibri", 28, "bold"), hover_color="white", command=show_login_frame)
back_to_login.place(relx=0.048, rely=0.71, anchor="nw")

########## Main Frame (Parent frame of add_exp_frame, view_exp_frame, overview_frame, and etc.)##############
main_frame = ctk.CTkFrame(
    root, width=screen_width, fg_color="white", height=screen_height, corner_radius=0)

nav_bar = ctk.CTkFrame(main_frame, width=screen_width/5,
                       fg_color="#333d79", height=screen_height, corner_radius=0)
nav_bar.place(relx=0, rely=0, anchor="nw")

user_icon = ctk.CTkLabel(main_frame, image=usericon,
                         text=" ", fg_color="#333d79")
user_icon.place(relx=0.01, rely=0.03, anchor="nw")


user_name = ctk.CTkLabel(main_frame, text="",
                         fg_color="#333d79", font=("Calibri", 30, "bold"), text_color="white")
user_name.place(relx=0.055, rely=0.055, anchor="nw")

# nav buttons
add_exp_btn = ctk.CTkButton(main_frame, text="   Add Expense", fg_color="white", text_color="#333d79", bg_color="#333d79",
                            corner_radius=30, width=250, height=62, font=("Calibri", 30, "bold"), hover=None, command=show_add_expenese_frame)
add_exp_btn.place(relx=0.06, rely=0.2, anchor="n")


view_exp_btn = ctk.CTkButton(main_frame, text="     View Expense", fg_color="#333d79", text_color="white", bg_color="#333d79",
                             corner_radius=30, width=250, height=62, font=("Calibri", 30, "bold"), hover=None, command=show_view_expense_frame)
view_exp_btn.place(relx=0.06, rely=0.3, anchor="n")


overview_btn = ctk.CTkButton(main_frame, text="Overview  ", fg_color="#333d79", text_color="white", bg_color="#333d79",
                             corner_radius=30, width=250, height=62, font=("Calibri", 30, "bold"), hover=None, command=show_overview_frame)
overview_btn.place(relx=0.06, rely=0.4, anchor="n")

about_us = ctk.CTkButton(main_frame, image=aboutusimage, text="About Us", fg_color="#333d79", bg_color="#333d79",
                         hover_color="#333d79", font=("Calibri", 30, "bold"), text_color="white", command=lambda: open_link("about_us"))
about_us.place(relx=0.07, rely=0.91, anchor="s")

logout_btn = ctk.CTkButton(main_frame, text="Logout    ", bg_color="#333d79", hover_color="#333d79", fg_color="#333d79", font=(
    "Calibri", 30, "bold"), image=logoutimage, text_color="#ff000d", command=logout)
logout_btn.place(relx=0.07, rely=0.97, anchor="s")

# Add Expense page frame (child of main_frame)
add_exp_frame = ctk.CTkFrame(
    main_frame, width=screen_width/1.25, fg_color="white", height=screen_height, corner_radius=0)

# add expense items
greetings = ctk.CTkLabel(add_exp_frame, text="Welcome, ",
                         fg_color="#fff", font=("Calibri", 52, "bold"), text_color="#333d79")
greetings.place(relx=0.06, rely=0.07, anchor="nw")
firstname = ctk.CTkLabel(add_exp_frame, text="User",
                         fg_color="#fff", font=("Calibri", 52, "bold"), text_color="#333d79")
firstname.place(relx=0.24, rely=0.07, anchor="nw")

add_expenses_text = ctk.CTkLabel(add_exp_frame, text="Did some spending? Add here.",
                                 fg_color="#fff", font=("Calibri", 30, "bold"), text_color="#333d79")
add_expenses_text.place(relx=0.06, rely=0.215, anchor="nw")

# Plus button
plus_button = ctk.CTkButton(add_exp_frame, image=plusimage, text="", fg_color="#fff", bg_color="#fff",
                            corner_radius=100, width=10, height=10, hover_color="#fff", command=expensedetails_add)
plus_button.place(relx=0.72, rely=0.255, anchor="nw")
# hover information using tooltip
# ToolTip(plus_button, msg="Add to expense table", delay=0.5, font=("Arial", 12, "bold"), follow=True,
#         parent_kwargs={"bg": "grey", "padx": 3, "pady": 3},
#         fg="white", bg="grey", padx=7, pady=7)

# add expense page's tabel items
expenses = ctk.CTkLabel(add_exp_frame, text="Expenses", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=200, height=50)
expenses.place(relx=0.06, rely=0.26, anchor="nw")

amount = ctk.CTkLabel(add_exp_frame, text="Amount (in Rs.)", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=200, height=50)
amount.place(relx=0.224, rely=0.26, anchor="nw")

caterory = ctk.CTkLabel(add_exp_frame, text="Category", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=205, height=50)
caterory.place(relx=0.388, rely=0.26, anchor="nw")

date = ctk.CTkLabel(add_exp_frame, text="Date", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=200, height=50)
date.place(relx=0.556, rely=0.26, anchor="nw")

# Tabel input items
expenses_input = ctk.CTkEntry(add_exp_frame, fg_color="#C7CBE5", font=(
    "Calibri", 24), width=200, height=50, corner_radius=0, border_width=0, text_color='black',  placeholder_text="")
expenses_input.place(relx=0.06, rely=0.32, anchor="nw")

amount_input = ctk.CTkEntry(add_exp_frame, fg_color="#C7CBE5", font=(
    "Calibri", 24), width=200, height=50, corner_radius=0, border_width=0, text_color='black', placeholder_text="")
amount_input.place(relx=0.224, rely=0.32, anchor="nw")


# category dropdown menu
# Set a default value from the options
selected_category = ctk.StringVar(value="Select...")
category_input = ctk.CTkOptionMenu(
    add_exp_frame, variable=selected_category, values=[
        "Food", "Transportation", "Shopping", "Housing", "Other"],
    width=205,
    height=50,
    corner_radius=0,
    fg_color="#C7CBE5",
    button_color="#C7CEE5",
    button_hover_color="#A4AAF0",
    text_color="Black",
    font=('Calibri', 24),
    dropdown_fg_color="#C7CBE5",
    dropdown_text_color="Black",
    dropdown_hover_color="#A4AAF0",
    dropdown_font=("Calibri", 22)
)
category_input.place(relx=0.388, rely=0.32, anchor="nw")

date_input = ctk.CTkEntry(add_exp_frame, fg_color="#C7CBE5", font=("Calibri", 24), width=200,
                          height=50, corner_radius=0, border_width=0, placeholder_text="yyyy/mm/dd", text_color='black', placeholder_text_color="#A9A9A9")
date_input.place(relx=0.556, rely=0.32, anchor="nw")

add_exp_msg = ctk.CTkLabel(
    add_exp_frame, text="", text_color="red", font=("Calibri", 22, "bold"), bg_color="white")
add_exp_msg.place(relx=0.06, rely=0.38, anchor="nw")


# Dashboard image
dashboard_image = ctk.CTkLabel(
    add_exp_frame, image=dashboard_illustration, text=" ", fg_color="#333d79")
dashboard_image.place(relx=0.5, rely=1, anchor="s")

# Quote
# dashboard_quote = ctk.CTkLabel(add_exp_frame, text="Did you know?\nTracking spending can help you\ncut unnecessary expenses and\nboost your savings by 10%!",
#                                fg_color="#fff", font=("Calibri", 30, "bold"), text_color="#333d79")
# dashboard_quote.place(relx=0.6, rely=0.77, anchor="nw")

############ View Expense Frame Starts here #############
view_exp_frame = ctk.CTkFrame(
    main_frame, width=screen_width/1.25, fg_color="white", height=screen_height, corner_radius=0)
table_frame = ctk.CTkScrollableFrame(
    view_exp_frame, width=819, fg_color="white", height=400, corner_radius=0, scrollbar_button_color="#333d79", scrollbar_button_hover_color="#7476BF")
table_frame.place(relx=0.059, rely=0.19, anchor="nw")

# Table items
filter_text = ctk.CTkLabel(view_exp_frame, text="Filters: ",
                           fg_color="white", font=("Calibri", 30, "bold"), text_color="#333d79")
filter_text.place(relx=0.06, rely=0.08, anchor="nw")
monthof_text = ctk.CTkLabel(view_exp_frame, text="Month of ",
                            fg_color="white", font=("Calibri", 30, "bold"), text_color="#333d79")
monthof_text.place(relx=0.14, rely=0.08, anchor="nw")

# view expense items
selected_month = ctk.StringVar(value=today.strftime("%B"))

dropdown_month = ctk.CTkOptionMenu(view_exp_frame, variable=selected_month, values=["January", "Feburary", "March", "April",
                                                                                    "May", "June", "July", "August", "September", "October", "November", "December"],
                                   width=150,
                                   height=40,
                                   corner_radius=10,
                                   fg_color="#C7CBE5",
                                   button_color="#C7CEE5",
                                   button_hover_color="#A4AAF0",
                                   text_color="Black",
                                   font=('Calibri', 20),
                                   state="readonly",
                                   dropdown_fg_color="#C7CBE5",
                                   dropdown_text_color="Black",
                                   dropdown_hover_color="#A4AAF0",
                                   dropdown_font=("Calibri", 18))
dropdown_month.place(relx=0.245, rely=0.078, anchor="nw")

year_text = ctk.CTkLabel(view_exp_frame, text="Year ",
                         fg_color="white", font=("Calibri", 30, "bold"), text_color="#333d79")
year_text.place(relx=0.38, rely=0.08, anchor="nw")

selected_year = ctk.StringVar(value=today.strftime("%Y"))
dropdown_year = ctk.CTkOptionMenu(view_exp_frame, variable=selected_year, values=["2024"],
                                  width=120,
                                  height=40,
                                  corner_radius=10,
                                  fg_color="#C7CBE5",
                                  button_color="#C7CEE5",
                                  button_hover_color="#A4AAF0",
                                  text_color="Black",
                                  font=('Calibri', 20),
                                  state="readonly",
                                  dropdown_fg_color="#C7CBE5",
                                  dropdown_text_color="Black",
                                  dropdown_hover_color="#A4AAF0",
                                  dropdown_font=("Calibri", 18))
dropdown_year.place(relx=0.435, rely=0.078, anchor="nw")

apply_filter_btn = ctk.CTkButton(view_exp_frame, text="Apply filters",
                                 fg_color="#fff", text_color="Green", font=("Calibri", 22, "bold"), width=20, height=30, corner_radius=30, hover_color="#fff", command=show_view_expense_frame)
apply_filter_btn.place(relx=0.545, rely=0.0789, anchor="nw")


# table rows and columns
expenses_clmn = ctk.CTkLabel(view_exp_frame, text="Expenses", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=200, height=50)
expenses_clmn.place(relx=0.06, rely=0.13, anchor="nw")

amount_clmn = ctk.CTkLabel(view_exp_frame, text="Amount (in Rs.)", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=200, height=50)
amount_clmn.place(relx=0.224, rely=0.13, anchor="nw")

caterory_clmn = ctk.CTkLabel(view_exp_frame, text="Category", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=205, height=50)
caterory_clmn.place(relx=0.388, rely=0.13, anchor="nw")

date_clmn = ctk.CTkLabel(view_exp_frame, text="Date", fg_color="#333d79", font=(
    "Calibri", 24, "bold"), width=200, height=50)
date_clmn.place(relx=0.556, rely=0.13, anchor="nw")


dashboard_image = ctk.CTkLabel(
    view_exp_frame, image=dashboard_illustration, text=" ", fg_color="#333d79")
dashboard_image.place(relx=0, rely=1, anchor="sw")

# Export button
export_btn = ctk.CTkButton(view_exp_frame, text="Export.csv",
                           fg_color="#333d79", text_color="#fff", font=("Calibri", 28, "bold"), width=150, height=50, corner_radius=10, hover_color="#7476BF", command=export_csv)
export_btn.place(relx=0.98, rely=0.95, anchor="se")


########### Overview Frame#########
overview_frame = ctk.CTkFrame(
    main_frame, width=screen_width/1.25, fg_color="#fff", height=screen_height, corner_radius=0)
plot_frame = ctk.CTkFrame(
    overview_frame, width=1, fg_color="#fff", height=screen_height, corner_radius=30)
plot_frame.place(relx=0.059, rely=0.19, anchor="nw")

havealook = ctk.CTkLabel(overview_frame, text="Have a look!!",
                         fg_color="#fff", font=("Calibri", 52, "bold"), text_color="#333d79")
havealook.place(relx=0.06, rely=0.07, anchor="nw")

#
# Show the login frame by default
show_login_frame()

root.protocol("WM_DELETE_WINDOW", on_closing)
# Start the main application loop
root.mainloop()
