from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import ImageTk, Image
import mysql.connector
import subprocess
import openpyxl


root = Tk()
root.title("Similarity Search of EMR")
root.geometry("750x550")


# Connect to MySQL
mydb = mysql.connector.connect(
    host = "localhost",
    user = "root",
    passwd = "123456",
    database = "emr"
)


# Create a cursor and initialize it
my_cursor = mydb.cursor()


# Create a global variable to capure the query csv_id
csv_id = 0


# Configuration window
def go_to_conf():
    conf = Toplevel(master=root)
    conf.title("Configuration Setup")
    conf.geometry("900x450")
    conf.transient(root)
    conf.grab_set()
    #root.wait_window(conf)

    # Create Labels
    topK_label = Label(conf, text="Select Top K Value", font=("Times", 16))
    topK_label.grid(row=0, column=0, columnspan=5, padx="10", pady="15", sticky=W)
    configuration_label = Label(conf, text="Specify Comparison Methods", font=("Times", 16))
    configuration_label.grid(row=2, column=0, columnspan=5, padx="10", pady="5", sticky=W)
    text_comparison_label = Label(conf, text="Text Component Weight", font=("Times", 14))
    text_comparison_label.grid(row=3, column=0, columnspan=5, sticky=W, padx="17", pady="5")
    interval_combine_label = Label(conf, text="Interval Component Weight", font=("Times", 14))
    interval_combine_label.grid(row=6, column=0, columnspan=5, sticky=W, padx="17", pady="5")
    overall_combine_label = Label(conf, text="Overall Combine Weight", font=("Times", 14))
    overall_combine_label.grid(row=10, column=0, columnspan=5, sticky=W, padx="17", pady="5")

    diagonosis_label = Label(conf, text="Diagonosis")
    diagonosis_label.grid(row=4, column=0, sticky=W, padx="30", pady="5")
    complaint_label = Label(conf, text="Complaint")
    complaint_label.grid(row=4, column=2, sticky=W, padx="30", pady="5")
    Medical_history_label = Label(conf, text="Medical History")
    Medical_history_label.grid(row=4, column=4, sticky=W, padx="30", pady="5")
    smoking_label = Label(conf, text="Smoking History")
    smoking_label.grid(row=5, column=0, sticky=W, padx="30", pady="5")
    drinking_label = Label(conf, text="Drinking History")
    drinking_label.grid(row=5, column=2, sticky=W, padx="30", pady="5")
    age_label = Label(conf, text="Age")
    age_label.grid(row=7, column=0, sticky=W, padx="30", pady="5")
    visit_label = Label(conf, text="Number of Visits")
    visit_label.grid(row=7, column=2, sticky=W, padx="30", pady="5")
    heartbeat_label = Label(conf, text="Heartbeat")
    heartbeat_label.grid(row=7, column=4, sticky=W, padx="30", pady="5")
    text_slider_label = Label(conf, text="Text")
    text_slider_label.grid(row=11, column=0, sticky=W, padx="30", pady="5")
    enumeration_slider_label = Label(conf, text="Enumeration")
    enumeration_slider_label.grid(row=11, column=2, sticky=W, padx="30", pady="5")
    interval_slider_label = Label(conf, text="Interval")
    interval_slider_label.grid(row=11, column=4, sticky=W, padx="30", pady="5")

    # Create drop down box
    topK_drop = ttk.Combobox(conf, value=["5", "10", "15", "20"])
    topK_drop.current(0)
    topK_drop.grid(row=0, column=2, padx="20")
    topK_drop.config(width=20)

    diagonosis_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    diagonosis_slider.set(5)
    diagonosis_slider.grid(row=4, column=1)
    complaint_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    complaint_slider.set(5)
    complaint_slider.grid(row=4, column=3)
    medical_history_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    medical_history_slider.set(3)
    medical_history_slider.grid(row=4, column=5)
    smoking_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    smoking_slider.set(2)
    smoking_slider.grid(row=5, column=1)
    drinking_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    drinking_slider.set(2)
    drinking_slider.grid(row=5, column=3)
    age_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    age_slider.set(5)
    age_slider.grid(row=7, column=1)
    visit_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    visit_slider.set(4)
    visit_slider.grid(row=7, column=3)
    heartbeat_slider = Scale(conf, from_=0, to=5, orient=HORIZONTAL)
    heartbeat_slider.set(3)
    heartbeat_slider.grid(row=7, column=5)

    # Create a slider to specify combine weight
    text_slider = Scale(conf, from_=0, to=10, orient=HORIZONTAL)
    text_slider.set(5)
    text_slider.grid(row=11, column=1)
    enumeration_slider = Scale(conf, from_=0, to=10, orient=HORIZONTAL)
    enumeration_slider.set(5)
    enumeration_slider.grid(row=11, column=3)
    interval_slider = Scale(conf, from_=0, to=10, orient=HORIZONTAL)
    interval_slider.set(5)
    interval_slider.grid(row=11, column=5)

    # Call external executable to conduct similarity search
    def search_result():
        # update new configuration file based on customized specification
        diagonosis = str(diagonosis_slider.get())
        complaint = str(complaint_slider.get())
        medical_history = str(medical_history_slider.get())
        smoking = str(smoking_slider.get())
        drinking = str(drinking_slider.get())
        age = str(age_slider.get())
        visit = str(visit_slider.get())
        heartbeat = str(heartbeat_slider.get())
        text_weight = str(text_slider.get())
        enumertaion_weight = str(enumeration_slider.get())
        interval_weight = str(interval_slider.get())

        config_file = open("conf.json", "w+")
        content = (
            '{"category":{"text":{"idx":[13,15,16,18,19]},'
            '"enumeration":{"idx":[7,9,11,14,17,20]},'
            '"interval":{"idx":[2,4,6]}},'
            '"if-null":{"text":{"default":0},'
            '"enumeration":{"default":1},"interval":{"default":1}},'
            '"single-dist":{"text":{"default":"jaccard","specific":{}},'
            '"enumeration":{"default":"equality","specific":{}},'
            '"interval":{"default":"norm","specific":{},"norm":{"2":100,"4":100,"6":100}}},'
            '"group-dist":{"text":{"type":"l1' 
            '","weights":{"13": ' + diagonosis + ', "15": ' + complaint + 
            ', "16": ' + medical_history + ', "18": ' + smoking + ', "19": ' + drinking + '}},'
            '"enumeration":{"type":"precision","weights":{}},'
            '"interval":{"type":"l2","weights":{"2": ' + age + 
            ', "4": ' + visit + ', "6": ' + heartbeat + '}}},'
            '"final-dist":{"type":"l1","weights":{"text":' + text_weight + 
            ',"enumeration":' + enumertaion_weight + ',"interval":' + interval_weight + '}}}'
        )
        config_file.write(content)
        config_file.close()

        # Create result frame
        result = Toplevel(master=conf)
        result.title("Search Result")
        result.geometry("700x700")
        result.transient(conf)
        result.grab_set()
        result_frame = Frame(result)
        result_frame.grid(row=0, column=0, pady="10", padx="45")
        result_verticle_scrollbar = Scrollbar(result_frame, orient=VERTICAL)
        result_horizontal_scrollbar = Scrollbar(result_frame, orient=HORIZONTAL)
        result_listbox = Listbox(result_frame, width=60, yscrollcommand=result_verticle_scrollbar.set, \
            xscrollcommand=result_horizontal_scrollbar.set)
        result_verticle_scrollbar.config(command=result_listbox.yview)
        result_horizontal_scrollbar.config(command=result_listbox.xview)
        result_verticle_scrollbar.pack(side=RIGHT, fill=Y)
        result_horizontal_scrollbar.pack(side=BOTTOM, fill=X)
        result_listbox.pack()
        
        # conduct similarity search and report search result
        topK = str(topK_drop.get())
        query_id = str(csv_id)
        p1 = subprocess.run(['./dummy_app', './conf.json', './real_data.csv', query_id, topK], \
            capture_output=True, text=True)
        lower_bound = 3
        upper_bound = int(topK) + 3
        for i in range(lower_bound, upper_bound):
            row = p1.stdout.split('\n')[i]
            #query_label = Label(result, text=p1.stdout.split('\n')[i])
            record_emrid = int(row.split(',')[0])
            #print(record_emrid)
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE csv_id = %s;"
            my_cursor.execute(sql, (record_emrid,))
            attempt = my_cursor.fetchall()
            # skip error message in case the returned result is not in the database
            if not attempt:
                pass
            else:
                fit_emr = attempt[0]
                #fit_emr_label = Label(result, text=fit_emr)
                #fit_emr_label.grid(row=(i-3), column=0, padx="20", sticky=W)
                result_listbox.insert(END, fit_emr)

        # show detailed information if necessary
        def show_details():
            selected = result_listbox.get(ANCHOR)
            text_widget = Text(result, height=20, width=60)
            text_widget.grid(row=3, column=0, padx="30")
            text_widget.configure(wrap=WORD)
            if not selected:
                warning = Toplevel(master=result)
                warning.geometry("400x100")
                warning.title("Warning")
                Label(warning, text="No record is selected.\n Please choose one record first.").pack()
                warning.transient(result)
                warning.grab_set()
                result.wait_window(warning)

                #messagebox.showwarning("Warning", \
                #    "No record is selected. Please choose one record first.")
            else:
                csv_id = result_listbox.get(ANCHOR)[0]
                sql = "SELECT ID, Age, Sex, Diagnosis, Complaint, Medical_history, \
                    Smoking_history, Drinking_history FROM translate_data WHERE id = %s;"
                my_cursor.execute(sql, (csv_id,))
                info = my_cursor.fetchall()[0]
                text_widget.insert(END, "EMR ID: " + str(info[0]) + "\n")
                text_widget.insert(END, "Age: " + str(info[1]) + "\n")
                text_widget.insert(END, "Sex: " + str(info[2]) + "\n")
                text_widget.insert(END, "Diagnosis: " + str(info[3]) + "\n")
                text_widget.insert(END, "Complaint: " + str(info[4]) + "\n")
                text_widget.insert(END, "Medical History: " + str(info[5]) + "\n")
                text_widget.insert(END, "Smoking History: " + str(info[6]) + "\n")
                text_widget.insert(END, "Drinking History: " + str(info[7]) + "\n")
                text_widget.configure(state='disabled')
        
        detail_button = Button(result, text="Show details", width=45, command=show_details)
        detail_button.grid(row=1, column=0, padx="10", pady="10")

    # Create search button
    search_button = Button(conf, text="Search", width=45, command=search_result)
    search_button.grid(row=13, column=0, padx="10", pady="30", columnspan=6)

# Search by EMR ID method
# Create labels
search_ID_label = Label(root, text="Search by EMR ID", font=("Times", 16))
search_ID_label.grid(row=0, column=0, columnspan=5, padx="10", pady="15", sticky=W)
EMRID_label = Label(root, text="EMR ID:")
EMRID_label.grid(row=1, column=0, sticky=W, padx="30", pady="5")


# Create entry boxes
EMRID_box = Entry(root, width=54)
EMRID_box.insert(END, "Enter the EMR ID")
EMRID_box.grid(row=1, column=1, padx="5", columnspan=3)


# Get the csv_id of the selected EMR record
def store_id_1():
    global csv_id
    emr_id = EMRID_box.get()
    sql = "SELECT csv_id FROM translate_data WHERE id = %s;"
    my_cursor.execute(sql, (emr_id,))
    result = my_cursor.fetchall()
    if not result:
        pop = Tk()
        pop.title("Warning")
        pop.geometry("400x100")
        pop_label = Label(pop, text="No matched result for current EMR ID")
        pop_label.pack()
        # pop_label.grid(row=0, column=0, columnspan=5, padx="10", pady="15")
    else: 
        csv_id = result[0][0]
        go_to_conf()

# Create buttons
find_ID_button = Button(root, text="Next", command=store_id_1)
find_ID_button.grid(row=1, column=4, padx="10")


# Create frame and scrollbar
EMR_frame = Frame(root)
EMR_frame.grid(row=9, column=0, pady="10", columnspan=4)

# Create a list box and configure scrollbar
EMR_verticle_scrollbar = Scrollbar(EMR_frame, orient=VERTICAL)
EMR_horizontal_scrollbar = Scrollbar(EMR_frame, orient=HORIZONTAL)
EMR_listbox = Listbox(EMR_frame, width=60, yscrollcommand=EMR_verticle_scrollbar.set, \
    xscrollcommand=EMR_horizontal_scrollbar.set)
EMR_verticle_scrollbar.config(command=EMR_listbox.yview)
EMR_horizontal_scrollbar.config(command=EMR_listbox.xview)
EMR_verticle_scrollbar.pack(side=RIGHT, fill=Y)
EMR_horizontal_scrollbar.pack(side=BOTTOM, fill=X)
EMR_listbox.insert(END, "Please specify at least one feature and click on Find.")
EMR_listbox.insert(END, "Matched EMR results will show here.")
EMR_listbox.pack()


# Search by Features method
def search_by_feature():
    # Clear listbox first
    EMR_listbox.delete(0, END)

    # Get selected feature
    feature1 = feature1_drop.get()
    feature2 = feature2_drop.get()
    feature3 = feature3_drop.get()

    # Find EMR candidate by specified feature
    def insert_records(records):
        if not records:
            EMR_listbox.insert(END, "No matched EMR record.") 
        else:
            for result in records:
                EMR_listbox.insert(END, result)
        EMR_listbox.pack()

    def find_one_feature(feature, value):
        # Determine query command
        if (feature == "Age" or feature == "Operation_id" or feature == "Sex" or feature == "Blood_type"):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + \
                feature + " = %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (value,))
        if (feature == "Diagnosis" or feature == "Medical_history" or feature == "Smoking_history" or feature == "Drinking_history"):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + \
                feature + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, ('%' + value + '%',))
        records = my_cursor.fetchall()
        insert_records(records)
    
    def find_two_features(featureA, valueA, featureB, valueB):
        if ((featureA == "Age" or featureA == "Operation_id" or featureA == "Sex" or featureA == "Blood_type") and \
            (featureB == "Age" or featureB == "Operation_id" or featureB == "Sex" or featureB == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " +\
                 featureA + " = %s AND " + featureB + " = %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueA, valueB,))
        elif (featureA == "Age" or featureA == "Operation_id" or featureA == "Sex" or featureA == "Blood_type"):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + \
                featureA + " = %s AND " + featureB + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueA, '%' + valueB + '%',))
        elif (featureB == "Age" or featureB == "Operation_id" or featureB == "Sex" or featureB == "Blood_type"):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + \
                featureB + " = %s AND " + featureA + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueB, '%' + valueA + '%',))
        else:
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + \
                featureA + " LIKE %s AND " + featureB + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, ('%' + valueA + '%', '%' + valueB + '%',))
        records = my_cursor.fetchall()
        insert_records(records)

    def find_three_features(featureA, valueA, featureB, valueB, featureC, valueC):
        if ((featureA == "Age" or featureA == "Operation_id" or featureA == "Sex" or featureA == "Blood_type") and \
            (featureB == "Age" or featureB == "Operation_id" or featureB == "Sex" or featureB == "Blood_type") and \
            (featureC == "Age" or featureC == "Operation_id" or featureC == "Sex" or featureC == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureA + " = %s AND " + featureB + \
                " = %s AND " + featureC + " = %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueA, valueB, valueC,))
        elif ((featureA == "Age" or featureA == "Operation_id" or featureA == "Sex" or featureA == "Blood_type") and \
            (featureB == "Age" or featureB == "Operation_id" or featureB == "Sex" or featureB == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureA + " = %s AND " + featureB + \
                " = %s AND " + featureC + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueA, valueB, '%' + valueC + '%',))
        elif ((featureA == "Age" or featureA == "Operation_id" or featureA == "Sex" or featureA == "Blood_type") and \
            (featureC == "Age" or featureC == "Operation_id" or featureC == "Sex" or featureC == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureA + " = %s AND " + featureC + \
                " = %s AND " + featureB + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueA, valueC, '%' + valueB + '%',))
        elif ((featureB == "Age" or featureB == "Operation_id" or featureB == "Sex" or featureB == "Blood_type") and \
            (featureC == "Age" or featureC == "Operation_id" or featureC == "Sex" or featureC == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureB + " = %s AND " + featureC + \
                " = %s AND " + featureA + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueB, valueC, '%' + valueA + '%',))
        elif ((featureA == "Age" or featureA == "Operation_id" or featureA == "Sex" or featureA == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureA + " = %s AND " + featureB + \
                " LIKE %s AND " + featureC + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueA, '%' + valueB + '%', '%' + valueC + '%',))
        elif ((featureB == "Age" or featureB == "Operation_id" or featureB == "Sex" or featureB == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureB + " = %s AND " + featureA + \
                " LIKE %s AND " + featureC + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueB, '%' + valueA + '%', '%' + valueC + '%',))
        elif ((featureC == "Age" or featureC == "Operation_id" or featureC == "Sex" or featureC == "Blood_type")):
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureC + " = %s AND " + featureA + \
                " LIKE %s AND " + featureB + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, (valueC, '%' + valueA + '%', '%' + valueB + '%',))
        else:
            sql = "SELECT ID, Age, Sex, Diagnosis FROM translate_data WHERE " + featureA + " LIKE %s AND " + featureB + \
                " LIKE %s AND " + featureC + " LIKE %s ORDER BY ID DESC LIMIT 20;"
            my_cursor.execute(sql, ('%' + valueA + '%', '%' + valueB + '%', '%' + valueC + '%',))
        records = my_cursor.fetchall()
        insert_records(records)
  
    # Output search result to list box
    if (feature1 == "select feature" and feature2 == "select feature" and feature3 == "select feature"):
        EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
        EMR_listbox.pack()
    # One feature
    elif (feature1 != "select feature" and feature2 == "select feature" and feature3 == "select feature"):
        if (not feature1_box.get()):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        else: 
            find_one_feature(feature1, feature1_box.get())
    elif (feature1 == "select feature" and feature2 != "select feature" and feature3 == "select feature"):
        if (not feature2_box.get()):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        else: 
            find_one_feature(feature2, feature2_box.get())
    elif (feature1 == "select feature" and feature2 == "select feature" and feature3 != "select feature"):
        if (not feature3_box.get()):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        else: 
            find_one_feature(feature3, feature3_box.get())
    # Two features
    elif (feature1 != "select feature" and feature2 != "select feature" and feature3 == "select feature"):
        if ((not feature1_box.get()) and (not feature2_box.get())):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        elif (not feature1_box.get()): 
            find_one_feature(feature2, feature2_box.get())
        elif (not feature2_box.get()): 
            find_one_feature(feature1, feature1_box.get())
        else: 
            find_two_features(feature1, feature1_box.get(), feature2, feature2_box.get())
    elif (feature1 != "select feature" and feature2 == "select feature" and feature3 != "select feature"):
        if ((not feature1_box.get()) and (not feature3_box.get())):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        elif (not feature1_box.get()): 
            find_one_feature(feature3, feature3_box.get())
        elif (not feature3_box.get()): 
            find_one_feature(feature1, feature1_box.get())
        else: 
            find_two_features(feature1, feature1_box.get(), feature3, feature3_box.get())
    elif (feature1 == "select feature" and feature2 != "select feature" and feature3 != "select feature"):
        if ((not feature2_box.get()) and (not feature3_box.get())):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        elif (not feature2_box.get()): 
            find_one_feature(feature3, feature3_box.get())
        elif (not feature3_box.get()): 
            find_one_feature(feature2, feature2_box.get())
        else: 
            find_two_features(feature2, feature2_box.get(), feature3, feature3_box.get())
    # Three features
    else:
        if ((not feature1_box.get()) and (not feature2_box.get()) and (not feature3_box.get())):
            EMR_listbox.insert(END, "No feature is selected. Please specify at least one feature.")
            EMR_listbox.pack()
        elif ((not feature1_box.get()) and (not feature2_box.get())): 
            find_one_feature(feature3, feature3_box.get())
        elif ((not feature1_box.get()) and (not feature3_box.get())): 
            find_one_feature(feature2, feature2_box.get())
        elif ((not feature2_box.get()) and (not feature3_box.get())): 
            find_one_feature(feature1, feature1_box.get())
        elif (not feature1_box.get()): 
            find_two_features(feature2, feature2_box.get(), feature3, feature3_box.get())
        elif (not feature2_box.get()): 
            find_two_features(feature1, feature1_box.get(), feature3, feature3_box.get())
        elif (not feature3_box.get()): 
            find_two_features(feature1, feature1_box.get(), feature2, feature2_box.get())
        else: 
            find_three_features(feature1, feature1_box.get(), feature2, feature2_box.get(), feature3, feature3_box.get())


# Get the csv_id of the selected EMR record
def store_id_2():
    global csv_id
    if not EMR_listbox.get(ANCHOR):
        pop = Tk()
        pop.title("Warning")
        pop.geometry("400x100")
        pop_label = Label(pop, text="No EMR record is selected")
        pop_label.pack()
    else:
        emr_id = EMR_listbox.get(ANCHOR)[0]
        sql = "SELECT csv_id FROM translate_data WHERE id = %s;"
        my_cursor.execute(sql, (emr_id,))
        result = my_cursor.fetchall()
        if not result:
            pop = Tk()
            pop.title("Warning")
            pop.geometry("400x100")
            pop_label = Label(pop, text="No matched result for current EMR ID")
            pop_label.pack()
        else: 
            csv_id = result[0][0]
            go_to_conf()


# Create button
next_button = Button(root, text="Next", height=5, command=store_id_2)
next_button.grid(row=9, column=4)


# Create labels
search_feature_label = Label(root, text="Search by Features", font=("Times", 16))
search_feature_label.grid(row=3, column=0, columnspan=5, padx="10", pady="10", sticky=W)
feature1_label = Label(root, text="Feature 1:")
feature1_label.grid(row=5, column=0, sticky=W, padx="30", pady="5")
feature2_label = Label(root, text="Feature 2:")
feature2_label.grid(row=6, column=0, sticky=W, padx="30", pady="5")
feature3_label = Label(root, text="Feature 3:")
feature3_label.grid(row=7, column=0, sticky=W, padx="30", pady="5")
value1_label = Label(root, text="Value:")
value1_label.grid(row=5, column=2, sticky=W, padx="10")
value2_label = Label(root, text="Value:")
value2_label.grid(row=6, column=2, sticky=W, padx="10")
value3_label = Label(root, text="Value:")
value3_label.grid(row=7, column=2, sticky=W, padx="10")


# Create drop down box
feature1_drop = ttk.Combobox(root, value=["select feature", "Age", "Operation_id", "Sex",  \
    "Blood_type", "Diagnosis", "Medical_history", "Smoking_history", "Drinking_history"])
feature1_drop.current(0)
feature1_drop.grid(row=5, column=1)
feature2_drop = ttk.Combobox(root, value=["select feature", "Age", "Operation_id", "Sex",  \
    "Blood_type", "Diagnosis", "Medical_history", "Smoking_history", "Drinking_history"])
feature2_drop.current(0)
feature2_drop.grid(row=6, column=1)
feature3_drop = ttk.Combobox(root, value=["select feature", "Age", "Operation_id", "Sex",  \
    "Blood_type", "Diagnosis", "Medical_history", "Smoking_history", "Drinking_history"])
feature3_drop.current(0)
feature3_drop.grid(row=7, column=1)


# Create entry boxes
feature1_box = Entry(root)
feature1_box.grid(row=5, column=3, padx="5")
feature2_box = Entry(root)
feature2_box.grid(row=6, column=3, padx="5")
feature3_box = Entry(root)
feature3_box.grid(row=7, column=3, padx="5")


# Clear Text Fields
def clear_fields():
    feature1_box.delete(0, END)
    feature2_box.delete(0, END)
    feature3_box.delete(0, END)
    feature1_drop.current(0)
    feature2_drop.current(0)
    feature3_drop.current(0)
    EMR_listbox.delete(0, END)
    EMR_listbox.insert(END, "Please specify at least one feature and click on Find.")
    EMR_listbox.insert(END, "Matched EMR results will show here.")


# Create buttons
clear_button = Button(root, text="Clear Fields", command=clear_fields)
clear_button.grid(row=8, column=3, padx="10", pady="10")
findByfeature_button = Button(root, text="Find", command=search_by_feature)
findByfeature_button.grid(row=8, column=4, padx="10")


# Create footer
footer_label = Label(root, text="Developed by Yuewen Wu, 2021©")
footer_label.grid(row=10, column=0, padx="10", pady="10", columnspan=2, sticky=W)


# Insert school logo
princeton_width = 15
princeton_height = 20
princeton_logo = Image.open("Princeton.png")
princeton_logo = princeton_logo.resize((princeton_width, princeton_height), Image.ANTIALIAS)
princeton_photoImg = ImageTk.PhotoImage(princeton_logo)
princeton_label = Label(root, image=princeton_photoImg)
princeton_label.grid(row=10, column=5)

Tsinghua_width = 20
Tsinghua_height = 20
Tsinghua_logo = Image.open("Tsinghua.png")
Tsinghua_logo = Tsinghua_logo.resize((Tsinghua_width, Tsinghua_height), Image.ANTIALIAS)
Tsinghua_photoImg = ImageTk.PhotoImage(Tsinghua_logo)
Tsinghua_label = Label(root, image=Tsinghua_photoImg)
Tsinghua_label.grid(row=10, column=6)


root.mainloop()