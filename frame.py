#-------Done by team "New Floraison"
#----Naveen.B----#
#----Keerthana----#
#----Prithiga.S----#
#----Lokeshwaran----#

from tkinter import *
from tkinter import ttk
import datetime as dt
from mydb import *
from tkinter import messagebox
import customtkinter


customtkinter.set_appearance_mode("System")  # Modes: system (default), light, dark

customtkinter.set_default_color_theme("blue")  # Themes: blue (default), dark-blue, green

data = Database(db='myexpense.db')


#global variable

count = 0
selected_rowid = 0
# functions
def saveRecord():
    global data
    data.insertRecord(item_name=item_name.get(),
                      item_price=item_amt.get(),
                      purchase_date=transaction_date.get())
       
def setDate():
    date = dt.datetime.now()
    dopvar.set(f'{date:%d %B %Y}')

def clearEntries():
    item_name.delete(0, 'end')
    item_amt.delete(0, 'end')
    transaction_date.delete(0, 'end')

def fetch_records():
    f = data.fetchRecord('select rowid, * from expense_record')
    global count
   
   
    for rec in f:
        trv.insert(parent='',
                   index='0',
                   iid=count,
                   values=(rec[0], rec[1], rec[2], rec[3]))
       
       
       
        count += 1
    trv.after(400, refreshData)

def select_record(event):
    global selected_rowid
    selected = trv.focus()    
    val = trv.item(selected, 'values')
  
    try:
        selected_rowid = val[0]
        d = val[3]
        namevar.set(val[1])
        amtvar.set(val[2])
        dopvar.set(str(d))
   
   
    except Exception as ep:
        pass


def update_record():
    global selected_rowid

    selected = trv.focus()
	# Update record
    try:
        data.updateRecord(namevar.get(),
                          amtvar.get(),
                          dopvar.get(),
                          selected_rowid)
        



        trv.item(selected,
                 text="",
                 values=(namevar.get(),
                         amtvar.get(),
                         dopvar.get()
                         )
                )
        

    except Exception as ep:
        messagebox.showerror('Error',ep)

	# Clear entry boxes
    item_name.delete(0, END)
    item_amt.delete(0, END)
    transaction_date.delete(0, END)
    trv.after(400, refreshData)
    

def totalBalance():
    f = data.fetchRecord(query="Select sum(item_price) from expense_record")


    for i in f:

        for j in i:

            messagebox.showinfo('Current Balance: ', f"Total Expense: ' {j} \nBalance Remaining: {5000 - j}")

def refreshData():

    for item in trv.get_children():
      
      trv.delete(item)

    fetch_records()
    
def deleteRow():

    global selected_rowid
    data.removeRecord(selected_rowid)
    refreshData()






root = Tk()
root.title('Work Expenses')
root.geometry('680x400')

#-------------------------------------------------------------------------------------------------------------------------------------
f =('time new roman',14)
snvar = IntVar()
namevar = StringVar()
amtvar = IntVar()
dopvar = StringVar()





#----------------------------------------------------------------------------------------------------------------------------------
f2 = Frame(root)
f2.pack()

f1 = Frame(root,padx=10,pady=10,)
f1.pack(expand=True,fill=BOTH)

#------------------------------------------------------------------------------------------------------------------------------------
# Label widget
#Label(f1, text='SI NO', font=f,width=10).grid(row=0, column=0,sticky=W)
Label(f1, text='ITEM NAME', font=f,width=10).grid(row=1, column=0,sticky=W)
Label(f1, text='ITEM PRICE', font=f,width=10).grid(row=2, column=0,sticky=W)
Label(f1, text='PURCHASE DATE  ', font=f,width=16).grid(row=3, column=0,sticky=W)

# Entry widgets 
#item_sino = Entry(f1,
#                  font=f,
#                  textvariable=snvar,
#                  width=10)

item_name = Entry(f1,
                  font=f,
                  textvariable=namevar,
                  width=10)

item_amt = Entry(f1,
                 font=f,
                 textvariable=amtvar,
                 width=10)

transaction_date = Entry(f1,
                         font=f,
                         textvariable=dopvar,
                         width=10)

# Entry grid placement


#item_sino.grid(row=0,
#               column=1,
#               sticky=W,
#               pady=14)

item_name.grid(row=1,
               column=1,
               sticky=W,
               pady=14)

item_amt.grid(row=2,
              column=1,
              sticky=W,
              pady=14)

transaction_date.grid(row=3,
                      column=1,
                      sticky=W )

# Create the buttons




save_button = Button(f1,text="Save Record",
                     command=saveRecord,
                     width=15,
                     borderwidth=8,
                     bg='green')


save_button.grid(column=2,
                 row=0,
                 sticky=S,
                 padx=10)


clear_button = Button(f1,
                      text="Clear Entry",
                      command=clearEntries,
                      width=15,
                      borderwidth=8,
                      bg="orange")

clear_button.grid(column=2,
                  row=1,)


exit_button = Button(f1,
                     text="Exit",
                     command=lambda:root.destroy(),
                     width=15,
                     borderwidth=8,
                     bg='red')


exit_button.grid(column=2,
                 row=2,
                 sticky=N)


balance_button = Button(f1,
                        text="Total Balance",
                        command=totalBalance,
                        width=15,
                        borderwidth=8,
                        bg='grey')


balance_button.grid(column=3,
                    row=0,
                    sticky=S)


update_button = Button(f1,
                       text="Update Record",
                       command=update_record,
                       width=15,
                       borderwidth=8,
                       bg='yellow')


update_button.grid(column=3,
                   row=1,)


delete_button =Button(f1,
                      text="Delete Record",
                      command=deleteRow,
                      width=15,
                      borderwidth=8,
                      bg='red')


delete_button.grid(column=3,
                   row=2,
                   sticky=N)


button = customtkinter.CTkButton(f1,
                                 text="current date",
                                 command=setDate,
                                 width=280,
                                 border_width=10)


button.grid(column=2,
            row=3,
            sticky=N,
            columnspan=2,
            pady=10,
            padx=50)







#---------------------------------------------------------------------------------------------------------------------------------------

trv = ttk.Treeview(f2,
                   selectmode='browse',
                   columns=(1,2,3,4),
                   show='headings',
                   height=8)


trv.pack(side='left')


trv.column(1,
           anchor=CENTER,
           stretch=NO,
           width=80)

trv.column(2,
           anchor=CENTER,
           stretch=NO,
           width=220)

trv.column(3,
           anchor=CENTER,
           stretch=NO,
           width=140)

trv.column(4,
           anchor=CENTER,
           stretch=NO,
           width=210)

trv.heading(1,
            text='S.no')

trv.heading(2,
            text='item name')

trv.heading(3,
            text='item price')

trv.heading(4,
            text='purchase date')

style = ttk.Style()

style.theme_use('default')

style.map('Treeview')

scr = Scrollbar(f2,orient='vertical')

scr.configure(command=trv.yview)

scr.pack(side='right',fill='y')

trv.config(yscrollcommand=scr.set)













root.mainloop()