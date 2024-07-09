import sqlite3
from tkinter import *
from tkinter import messagebox
from tkinter.ttk import Treeview
import tkinter.font as font

primary_color = '#ddd5ca'
bg_color = '#ddd5ca'
text_color = '#333333'

root = Tk()
root.geometry('850x300+0+0')
root['bg'] = bg_color
root.title('Library Progame')

# init layouts
fm_main = Frame(root, bg=primary_color)
fm_main.pack(fill=BOTH, expand=True)

db_path = 'Book.db'

str_newbooks = StringVar()
str_category = StringVar()


myFont = font.Font(family='Helvetica',weight="bold",size=15)
buttonFont = font.Font(family='Helvetica', size=13, weight='bold')
pageFont = font.Font(family='Helvetica', size=12, weight='bold')

#show all books
def show_list():
    new_window = Toplevel(root)
    new_window.geometry('600x500+900+100')
    new_window['bg'] = bg_color
    new_window.title('Book list')

    # init layouts
    fm_main = Frame(new_window, bg=primary_color)
    fm_main.pack(fill=BOTH, expand=True)

    fm_treeview = Frame(new_window)
    fm_treeview.pack(side=TOP, fill=BOTH, expand=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Book_list')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    list_column = ( 'Book_title', 'Category','Status')
    tree = Treeview(fm_treeview, height=90, show='headings', columns=list_column, padding=(5,5,5,5))
    
    tree.heading('Book_title', text='Book Title')
    tree.heading('Category', text='Category')
    tree.heading('Status', text='Status')
    
    tree.column('Book_title', width=200, stretch=False,anchor=CENTER)
    tree.column('Category', width=200, stretch=False,anchor=CENTER)
    tree.column('Status', width=100, stretch=False,anchor=CENTER)
    tree.pack(side=TOP, fill=BOTH, expand=True)
    #show the book
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close() 
    #button to Exit
    btn_cancel = Button(fm_main, text='Cancel', font=buttonFont, command=new_window.destroy,image=img_cancel,compound=LEFT)
    btn_cancel.pack(side=LEFT, padx=10, pady=10,ipadx=10, ipady=7)

#borrow window
def Borrow_Book_window():
    
    new_window = Toplevel(root)
    new_window.geometry('600x500+900+100')
    new_window['bg'] = bg_color
    new_window.title('Borrow Book')

    # init layouts
    fm_main = Frame(new_window, bg=primary_color)
    fm_main.pack(fill=BOTH, expand=True)

    fm_treeview = Frame(new_window)
    fm_treeview.pack(side=TOP, fill=BOTH, expand=True)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Book_list')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    list_column = ( 'Book_title', 'Category','Status')
    tree = Treeview(fm_treeview, height=90, show='headings', columns=list_column, padding=(5,5,5,5))
   
    tree.heading('Book_title', text='Book Title')
    tree.heading('Category', text='Category')
    tree.heading('Status', text='Status')
    
    tree.column('Book_title', width=200, stretch=False,anchor=CENTER)
    tree.column('Category', width=200, stretch=False,anchor=CENTER)
    tree.column('Status', width=200, stretch=False,anchor=CENTER)
    tree.pack(side=TOP, fill=BOTH, expand=True)
    #show the book
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close() 
    
    #select the book if status is NOT-Available can't borrow
    def select_book():
        selected_item = tree.selection()[0]
        selected_book = tree.item(selected_item)['values'][0]
        selected_category = tree.item(selected_item)['values'][1]
        selected_status = tree.item(selected_item)['values'][2]
        if selected_status == 'Available':
            str_newbooks.set(selected_book)
            str_category.set(selected_category)
            tree.delete(selected_item)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE Book_list SET Status = "NOT-Available" WHERE Book_title = ?', (selected_book,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'You have borrowed the book')
        else:
            messagebox.showinfo('Error', 'The book is not available')
    #button to borrow the book
    btn_borrow = Button(fm_main, text='Borrow', font=buttonFont, command=select_book,image=img2,compound=LEFT)
    btn_borrow.pack(side=LEFT, padx=10, pady=10,ipadx=10, ipady=5)
    #button to cancel the borrow
    btn_cancel = Button(fm_main, text='Cancel', font=buttonFont, command=new_window.destroy,image=img_cancel,compound=LEFT)
    btn_cancel.pack(side=LEFT, padx=10, pady=10,ipadx=10, ipady=7)

#return the book
def return_book():
    new_window = Toplevel(root)
    new_window.geometry('550x500+900+100')
    new_window['bg'] = bg_color
    new_window.title('Return Book')

    # init layouts
    fm_main = Frame(new_window, bg=primary_color)
    fm_main.pack(fill=BOTH, expand=True)


    fm_treeview = Frame(new_window)
    fm_treeview.pack(side=TOP, fill=BOTH, expand=True)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Book_list')
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    list_column = ( 'Book_title', 'Category','Status')
    tree = Treeview(fm_treeview, height=90, show='headings', columns=list_column, padding=(5,5,5,5))
   
    tree.heading('Book_title', text='Book Title')
    tree.heading('Category', text='Category')
    tree.heading('Status', text='Status')
    
    
    tree.column('Book_title', width=150, stretch=False,anchor=CENTER)
    tree.column('Category', width=150, stretch=False,anchor=CENTER)
    tree.column('Status', width=150, stretch=False,anchor=CENTER)
    
    tree.pack(side=TOP, fill=BOTH, expand=True)
    #show the book
    for row in rows:
        tree.insert('', 'end', values=row)
    conn.close() 

    #select the book if status is Available can't return
    def select_book():
        selected_item = tree.selection()[0]
        selected_book = tree.item(selected_item)['values'][0]
        selected_category = tree.item(selected_item)['values'][1]
        selected_status = tree.item(selected_item)['values'][2]
        if selected_status == 'NOT-Available':
            str_newbooks.set(selected_book)
            str_category.set(selected_category)
            tree.delete(selected_item)
            conn = sqlite3.connect(db_path)
            cursor = conn.cursor()
            cursor.execute('UPDATE Book_list SET Status = "Available" WHERE Book_title = ?', (selected_book,))
            conn.commit()
            conn.close()
            messagebox.showinfo('Success', 'You have return the book')
        else:
            messagebox.showinfo('Error', 'The book is available')
    #button to return the book
    btn_return = Button(fm_main, text='Return', font=buttonFont, command=select_book,image=img3,compound=LEFT)
    btn_return.pack(side=LEFT, padx=10, pady=10,ipadx=10, ipady=5)
    #button to cancel the return
    btn_cancel = Button(fm_main, text='Cancel', font=buttonFont, command=new_window.destroy,image=img_cancel,compound=LEFT)
    btn_cancel.pack(side=LEFT, padx=10, pady=10,ipadx=10, ipady=7)

#add new book
def add_book():
    new_window = Toplevel(root)
    new_window.geometry('300x400+900+100')
    new_window['bg'] = bg_color
    new_window.title('Add Book')

    fm_add= Frame(new_window, bg=primary_color)
    fm_add.pack(fill=BOTH, expand=True)

    #put the picture on top of the window and center it in the window
    lbl_picture = Label(fm_add, image=img4, bg=primary_color)
    lbl_picture.place(x=130, y=20)

    add__book = Entry(fm_add, textvariable=str_newbooks,font=('Helvetica 15')).place(x=100, y=100,height=40, width=150)
    add_cat = Entry(fm_add, textvariable=str_category,font=('Helvetica 15')).place(x=100, y=200,height=40, width=150)
    


    Label(fm_add, text='Book Title', bg=primary_color, font=pageFont,fg=text_color).place(x=10, y=115)
    Label(fm_add, text='Category', bg=primary_color, font=pageFont,fg=text_color).place(x=10, y=215)
    
   
    def add_book_to_db():
        if str_newbooks.get() == '':
            messagebox.showinfo('Error', 'Please enter the book title')
            return
        if str_category.get() == '':
            str_category.set('general')
        conn = sqlite3.connect(db_path)
        cur = conn.cursor()
        insert_sql = 'INSERT INTO Book_list (Book_title, Category, Status) VALUES (?,?,?)'
        cur.execute(insert_sql, [str_newbooks.get(), str_category.get(), 'Available'])
        conn.commit()
        conn.close()
        messagebox.showinfo('Success', 'Book added successfully')
        new_window.destroy()
    btn_add = Button(fm_add, text='Add', command=add_book_to_db,font=buttonFont,compound=LEFT).place(x=100, y=300, height=40, width=100)
    btn_cancel = Button(fm_add, text='Cancel', command=new_window.destroy,font=buttonFont,compound=LEFT).place(x=100, y=350, height=40, width=100)

#exit the program
def exit_program():
    if messagebox.askokcancel('Quit', 'Do you want to quit?'):
        root.destroy()


 


img1 = PhotoImage(file='Photo/open-book.png').subsample(12,12)
img2 = PhotoImage(file='Photo/borrow.png').subsample(11,11)
img3 = PhotoImage(file='Photo/return.png').subsample(12,12)
img4 = PhotoImage(file='Photo/book.png').subsample(12,12)
img5 = PhotoImage(file='Photo/exit.png').subsample(12,12)
img_cancel = PhotoImage(file='Photo/remove.png').subsample(13,13)
#List Book button
bnb_list = Button(fm_main,text = "Book Name",font=('Tahoma 10 bold'),command=show_list,image=img1,compound=LEFT).grid(row=0, column=0,ipady=23,ipadx=20,padx=20,pady=50)

#change_status button
bnb_change_status = Button(fm_main,text = "Borrow Book",font=('Tahoma 10 bold'),command=Borrow_Book_window,image=img2,compound=LEFT).grid(row=0, column=1,ipady=20,ipadx=20,padx=20,pady=50)
#add button
bnb_add = Button(fm_main,text = "Add Book",font=('Tahoma 10 bold'),command=add_book,image=img4,compound=LEFT).grid(row=0, column=4,ipady=20,ipadx=20,padx=20,pady=50)
#exit button
bnb_exit = Button(fm_main,text = "Exit",font=('Tahoma 10 bold'),command=exit_program,image=img5,compound=LEFT).grid(row=1, column=4,ipady=10,ipadx=10)
#return button
bnb_return = Button(fm_main,text = "Return Book",font=('Tahoma 10 bold'),command=return_book,image=img3,compound=LEFT).grid(row=0, column=3,ipady=20,ipadx=20,padx=20,pady=50)

root.mainloop()
