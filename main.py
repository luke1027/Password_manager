from tkinter import *
import password_generator
import pyperclip
import json

DEFAULT_EMAIL = "luke@email.com"


# ---------------------------- SEARCH ------------------------------- #
def search():
    website = entry_website.get()
    show = Toplevel(window)
    show.title(website)
    show.configure(padx=20, pady=20)
    try:
        with open("account.json", "r") as file:
            data = json.load(file)
            if website in data:
                username = data[website]["username"]
                password = data[website]["password"]
                message = f"Username: {username}\n" \
                          f"Password: {password}"
            else:
                message = "No details for the website"
    except FileNotFoundError:
        message = "No details for the website"
    info_text = Label(master=show, text=message)
    info_text.pack()


# ---------------------------- PASSWORD GENERATOR ------------------------------- #
def random_password():
    entry_password.delete(0, END)
    new_password = password_generator.password()
    entry_password.insert(0, new_password)
    pyperclip.copy(new_password)


# ---------------------------- SAVE PASSWORD ------------------------------- #


def save():
    website = entry_website.get()
    username = entry_username.get()
    password = entry_password.get()
    new_data = {
        website: {
            "username": username,
            "password": password
        }
    }

    if website == "" or password == "":
        empty_message = Toplevel(window)
        empty_message.title("Warning")
        empty_message.configure(padx=20, pady=20)
        empty_label = Label(empty_message, text="Please don't leave the blank empty!")
        empty_label.pack()
    else:
        def packed_function():
            agree()
            is_ok.destroy()

        def agree():
            try:
                with open("account.json", "r") as file:
                    data = json.load(file)
            except FileNotFoundError:
                with open("account.json", "w") as file:
                    json.dump(new_data, file, indent=4)
            else:
                data.update(new_data)
                with open("account.json", "w") as file:
                    json.dump(data, file, indent=4)
            finally:
                entry_website.delete(0, END)
                entry_username.delete(0, END)
                entry_username.insert(0, DEFAULT_EMAIL)
                entry_password.delete(0, END)

        is_ok = Toplevel(window)
        is_ok.title(website)
        is_ok.configure(padx=20, pady=20)

        message = f"These are the details entered:\n" \
                  f"Username: {username}\n" \
                  f"Password: {password}"
        info_text = Label(master=is_ok, text=message)
        info_text.grid(column=2, row=0)

        button_yes = Button(master=is_ok, text="YES", command=packed_function)
        button_yes.grid(column=1, row=1)

        button_no = Button(master=is_ok, text="NO", command=is_ok.destroy)
        button_no.grid(column=3, row=1)

        is_ok.tkraise(window)


# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50)

canvas = Canvas()
canvas.config(width=200, height=200)
logo = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=logo)
canvas.grid(column=1, row=0)

# Labels
label_website = Label()
label_website.config(text="Website:")
label_website.grid(column=0, row=1)

label_username = Label()
label_username.config(text="Email/Username:")
label_username.grid(column=0, row=2)

label_password = Label()
label_password.config(text="Password:")
label_password.grid(column=0, row=3)

# Entries
entry_website = Entry()
entry_website.config(width=21)
entry_website.grid(column=1, row=1)
entry_website.focus()

entry_username = Entry()
entry_username.config(width=35)
entry_username.grid(column=1, row=2, columnspan=2)
entry_username.insert(END, DEFAULT_EMAIL)

entry_password = Entry()
entry_password.config(width=21)
entry_password.grid(column=1, row=3, )

# Button
button_search = Button()
button_search.config(text="Search", command=search, width=14)
button_search.grid(column=2, row=1)

button_random = Button()
button_random.config(text="Generate Password", command=random_password)
button_random.grid(column=2, row=3)

button_add = Button()
button_add.config(text="Add", width=36, command=save)
button_add.grid(column=1, row=4, columnspan=2)
window.mainloop()
