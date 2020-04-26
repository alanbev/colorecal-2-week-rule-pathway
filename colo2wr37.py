""" colorectal 2 wr clinic, investigation and pathway manager. In its current form this software is a demonstration of concept and no guarantee is given for its suitability for clinical use.  Concept and Code Copyright: Alan J Beveridge. For permission to use, copy edit or  adapt, contact ajbeveridge@tiscali.co.uk"""
from tkinter import *
#import pickle
import sqlite3
import string
#import datetime
from tkcalendar import DateEntry
# import docx

class MainMenu(Frame):
    """Generates master menu"""

    def __init__(self, master):
        super(MainMenu, self).__init__(master)
        self.grid()
        self.most_recent_patient_numb = 0  # used to generate clinic letter for current patient
        self.create_mainmenu_widgets()

    def create_mainmenu_widgets(self):
        Label(self, text="User Name").grid(row=1, column=0, sticky=W)
        self.username_box = Entry(self)
        self.username_box.grid(row=1, column=1, sticky=W)

        Label(self, text="Password").grid(row=2, column=0, sticky=W)
        self.password_box = Entry(self)
        self.password_box.grid(row=2, column=1, sticky=W)
        self.activate_login()

    def activate_login(self):
        self.login_button = Button(text="Log in", command=self.login)
        self.login_button.grid(row=2, column=3, sticky=W)

    def login(self):
        self.user_name = self.username_box.get()
        self.password = self.password_box.get()
        try:
            self.conn = sqlite3.connect('colotwr.db')
        except:
            Label(self, text="Missing database-Contact System Administrator").grid(row=4, column=0)
        self.cur = self.conn.cursor()
        self.cur.execute('''
        SELECT password FROM user WHERE user_ID=?
        ''', (self.user_name,))
        try:
            self.stored_pw_raw = self.cur.fetchone()
            self.stored_pw = self.stored_pw_raw[0]
            self.check_password()
        except:
            self.invalid_username = Label(self, text="incorrect username-please try again")
            self.invalid_username.grid(row=3, column=0)
            self.login_button.destroy()
            self.reenter_password = Button(text="Try Again", command=self.create_mainmenu_widgets)
            self.reenter_password.grid(row=4, column=3, sticky=W)

    def check_password(self):

        if self.password != self.stored_pw:
            self.wrong_pw_message = Label(self, text="Incorrect Password")
            self.wrong_pw_message.grid(row=4, column=0)
            self.login_button.destroy()
            self.reenter_password = Button(text="Try Again", command=self.create_mainmenu_widgets)
            self.reenter_password.grid(row=4, column=3, sticky=W)
        else:
            self.cur.execute('''
                SELECT  privilege, admin FROM user WHERE user_ID=?
                ''', (self.user_name,))
            self.user_status = self.cur.fetchone()
            user = (self.user_name, self.user_status[0])
        self.conn.close()
        if self.user_status[1] == 1:
            self.admin_button = Button(text="Admin Functions", command=self.admin_menu)
            self.admin_button.grid(row=8, column=2, sticky=W)

        self.new_patient_button = Button(self, text="Enter Information for New Clinic Patient",
                                         command=self.make_new_patient_form)
        self.new_patient_button.grid(row=6, column=0, sticky=W)

        self.new_patient_button = Button(self, text="Generate Clinic Letter", command=self.clinic_letter)
        self.new_patient_button.grid(row=7, column=0, sticky=W)

        self.new_endoscopy_button = Button(self, text="Endoscopy", command=self.make_endoscopy_form)
        self.new_endoscopy_button.grid(row=8, column=0, sticky=W)

        self.ct_button = Button(self, text="CT outcome", command=self.make_ct_form)
        self.ct_button.grid(row=9, column=0, sticky=W)

        self.mdt_button = Button(self, text="MDT Co-ordinator", command=self.mdt_coord)
        self.mdt_button.grid(row=7, column=1, sticky=W)

        self.ptl_button = Button(self, text="Patient Tracking List", command=self.ptl_list)
        self.ptl_button.grid(row=8, column=1, sticky=W)

    def make_new_patient_form(self):

        self.root3 = Toplevel(self.master)
        self.root3.title("Enter New Patient")
        self.referal = PatientForm(self.root3)

    def make_endoscopy_form(self):
        """creates for for recording endoscopy outcomes"""
        self.root3 = Toplevel(self.master)
        self.root3.title("Endoscopy Outcome")
        self.scope_episode = EndoscopyForm(self.root3)

    def make_ct_form(self):
        """creates for for recording endoscopy outcomes"""
        self.root8 = Toplevel(self.master)
        self.root8.title("CT Outcome")
        self.ct_episode = CtForm(self.root8)

    def admin_menu(self):
        """creates form for recording endoscopy outcomes"""
        self.root3 = Toplevel(self.master)
        self.root3.title("Administrative Functions")
        self.admin_episode = AdminForm(self.root3)

    def clinic_letter(self):
        """creates for for recording endoscopy outcomes"""
        self.root3 = Toplevel(self.master)
        self.root3.title("Clinic letter")
        self.clinic_letter = ClinicLetter(self.root3)

    def mdt_coord(self):
        """creates for for recording endoscopy outcomes"""
        self.root9 = Toplevel(self.master)
        self.root9.title("MDT Co-ordinator")
        self.mdt_form = MdtCoordinate(self.root9)

    def ptl_list(self):
        """creates ptl form"""
        self.root14 = Toplevel(self.master)
        self.root14.title("Patient Tracking List")
        self.ptl_list = Ptl(self.root14)
        self.ptl_list.ptl_form=True




class PatientForm(Frame):
    """Generates form to collect patient information in clinic and recommend appropriate investigation"""
    def __init__(self, master):
        super(PatientForm, self).__init__(master)
        self.grid()
        self.create_widgets()
        self.bowel_prep_outcome=[0,"","","","no","none"]

    def create_widgets(self):
        """Root function for generating form items"""
        Label(self, text="Colorectal Two Week Rule Triage Tool").grid(row=0, column=0, columnspan=4, sticky=W)
        # Enter patient demographics
        Label(self, text="Forename").grid(row=3, column=0, sticky=W)
        self.forename = Entry(self)
        self.forename.grid(row=3, column=1, sticky=W)
        Label(self, text="Surname").grid(row=3, column=2, sticky=W)
        self.surname = Entry(self)
        self.surname.grid(row=3, column=3, sticky=W)
        Label(self, text="Hosp. Numb").grid(row=4, column=0, sticky=W)
        self.hosp_no = Entry(self)
        self.hosp_no.grid(row=4, column=1, sticky=W)
        Label(self, text="DOB").grid(row=4, column=2, sticky=W)
        self.dob = DateEntry(self)
        self.dob.grid(row=4, column=3, sticky=W)
        Label(self, text="Sex").grid(row=4, column=4, sticky=E)
        self.sex = StringVar()
        self.sex.set(None)
        Radiobutton(self, text="Male", variable=self.sex, value="male").grid(row=4, column=5, sticky=W)
        Radiobutton(self, text="Female", variable=self.sex, value="female").grid(row=4, column=6, sticky=W)

        # create symptoms,history and signs checkboxes
        Label(self, text="Please tick the boxes for all applicable symptoms and findings").grid(row=8, column=0,
                                                                                                sticky=W, columnspan=4)
        Label(self, text="Symptoms").grid(row=10, column=0, sticky=W)
        self.fresh_blood = BooleanVar()
        Checkbutton(self, text="Fresh rectal bleeding", variable=self.fresh_blood).grid(row=11, column=0, sticky=W,
                                                                                        columnspan=2)
        self.dark_blood = BooleanVar()
        Checkbutton(self, text="Dark rectal bleeding, altered blood or mixed with stool",
                    variable=self.dark_blood).grid(row=12, column=0, sticky=W, columnspan=2)
        self.loose_stools = BooleanVar()
        Checkbutton(self, text="Loose or frequent stools", variable=self.loose_stools).grid(row=13, column=0, sticky=W,
                                                                                            columnspan=2)
        self.constipation = BooleanVar()
        Checkbutton(self, text="Constipation or less frequent stools", variable=self.constipation).grid(row=14,
                                                                                                        column=0,
                                                                                                        sticky=W,
                                                                                                        columnspan=2)

        self.lif_pain = BooleanVar()
        Checkbutton(self, text="Isolated left iliac fossa pain", variable=self.lif_pain).grid(row=15, column=0,
                                                                                              sticky=W, columnspan=2)

        self.abdo_pain = BooleanVar()
        Checkbutton(self, text="Other / diffuse abdominal pain ", variable=self.abdo_pain).grid(row=16, column=0,
                                                                                                sticky=W, columnspan=2)

        self.wt_loss = BooleanVar()
        Checkbutton(self, text="Unexplained Significant Weight Loss", variable=self.wt_loss).grid(row=17, column=0,
                                                                                                  sticky=W,
                                                                                                  columnspan=2)

        Label(self, text="History").grid(row=10, column=3, sticky=W)

        self.id_anaemia = BooleanVar()
        Checkbutton(self, text="Iron deficiency anaemia (low MCV,ferritin or iron)", variable=self.id_anaemia).grid(
            row=11, column=3, sticky=W, columnspan=2)

        self.fob = BooleanVar()
        Checkbutton(self, text="+ve Faecal Occult Blood test", variable=self.fob).grid(row=12, column=3, sticky=W,
                                                                                       columnspan=2)

        self.hist_neoplasia = BooleanVar()
        Checkbutton(self, text="History of colorectal adenomas or carcinoma", variable=self.hist_neoplasia).grid(row=13,
                                                                                                                 column=3,
                                                                                                                 sticky=W,
                                                                                                                 columnspan=2)

        self.prev_resect = BooleanVar()
        Checkbutton(self, text="Previous colonic or rectal resection", variable=self.prev_resect).grid(row=14, column=3,
                                                                                                       sticky=W,
                                                                                                       columnspan=2)

        Label(self, text="Examination Findings").grid(row=16, column=3, sticky=W)

        self.abdo_mass = BooleanVar()
        Checkbutton(self, text="Abdominal mass suspicious for tumour", variable=self.abdo_mass).grid(row=17, column=3,
                                                                                                     sticky=W,
                                                                                                     columnspan=2)

        self.rectal_mass = BooleanVar()
        Checkbutton(self, text="Palpable rectal mass", variable=self.rectal_mass).grid(row=18, column=3, sticky=W,
                                                                                       columnspan=3)

        # set up checkbuttons for co-morbidity
        Label(self, text="Co-morbidity").grid(row=20, column=0, sticky=W)
        Label(self, text="Does the patient have:").grid(row=32, column=0, sticky=W)

        self.pacemaker = BooleanVar()
        Checkbutton(self, text="A Pacemaker", variable=self.pacemaker).grid(row=23, column=0, sticky=W, columnspan=3)

        self.heart_valve = BooleanVar()
        Checkbutton(self, text="An artificial heart valve", variable=self.heart_valve).grid(row=24, column=0, sticky=W,
                                                                                            columnspan=3)

        # set up radiobuttons for diabetes status
        Label(self, text="Diabetes status").grid(row=25, column=0, sticky=W)
        self.diabetic = StringVar()
        self.diabetic.set(None)
        diab_status = ["not diabetic", "diet controlled", "tablet controlled", "insulin controlled"]
        column = 1
        for status in diab_status:
            Radiobutton(self, text=status, variable=self.diabetic, value=status).grid(row=25, column=column, sticky=W)
            column += 1
        # set up radiobuttons for anticoagulant status
        Label(self, text="Anticoagulants").grid(row=26, column=0, sticky=W)
        self.anticoag = StringVar()
        self.anticoag.set(None)
        anticoag_status = ["none or only aspirin", "warfarin", "clopidogrel", "dabigatrone", "apixiban", "riveroxiban"]
        column = 1
        for drug in anticoag_status:
            Radiobutton(self, text=drug, variable=self.anticoag, value=drug).grid(row=26, column=column, sticky=W)
            column += 1

        self.infect_disease = BooleanVar()
        Checkbutton(self, text="Does the patient have an infective disease", variable=self.infect_disease).grid(row=27,
                                                                                                                column=0,
                                                                                                                sticky=W,
                                                                                                                columnspan=4)

        Label(self, text="If so state which disease:").grid(row=27, column=1, sticky=W)
        self.which_inf_disease = Entry(self)
        self.which_inf_disease.grid(row=27, sticky=W, column=2)

        self.contrast_allergy = BooleanVar()
        Checkbutton(self, text="Does the patient have an allergy to X ray contrast",
                    variable=self.contrast_allergy).grid(row=28, column=0, sticky=W)

        Label(self, text="GFR").grid(row=29, column=0, sticky=W)
        self.gfr = Entry(self)
        self.gfr.grid(row=29, column=1, sticky=W)
        Label(self, text="If GFR <40 or unknown enter creatinine").grid(row=29, column=2, sticky=W, columnspan=2)
        self.creat = Entry(self)
        self.creat.grid(row=29, column=4)

        self.perf_status = IntVar()
        Label(self, text="Performance status").grid(row=30, column=0, sticky=W)
        self.perf = OptionMenu(self, self.perf_status, 0, 1, 2, 3, 4)
        self.perf.grid(row=30, column=1, sticky=W)

        self.frail = BooleanVar()
        Checkbutton(self,
                    text="Is the patient over 80 with significant frailty(eg unable to walk up stairs and likely to be poorly tolerant of colonoscopy",
                    variable=self.frail).grid(row=32, column=0, sticky=W, columnspan=6)

        Label(self, text="Comments (optional):").grid(row=31, column=0, sticky=W)
        self.comments = Entry(self)
        self.comments.grid(row=31, sticky=W, column=1, columnspan="4")

        # Creat submit button
        self.form_complete_button = Button(self, text="Form Complete", command=self.process_form)
        self.form_complete_button.grid(row=35, column=0, sticky=W)

        # function to process form

    def process_form(self):
        """Read form data in dictionary and generate symptom list"""
        self.prev_bad_hosp_numb_warn = False
        if not (self.hosp_no.get()).isnumeric():
            self.bad_hosp_numb_warn = Label(self, text="Please check and re-enter the hospital number")
            self.bad_hosp_numb_warn.grid(row=36, column=0, sticky=W)
            self.prev_bad_hosp_numb_warn = True
        else:
            if self.prev_bad_hosp_numb_warn == True:
                self.bad_hosp_numb_warn.destroy()
            self.unprocessed_dob = self.dob.get()
            self.form_data = {}
            self.variables = ["forename", "surname", "hosp_no", "dob", "sex", "fresh_blood", "dark_blood",
                              "loose_stools", "constipation", "lif_pain", "abdo-pain", "wt-loss", "id_anaemia", "fob",
                              "hist_neoplasia", "prev_resect", "abdo_mass",
                              "rectal_mass", "pacemaker", "heart_valve", "diabetic", "anticoag", "infect.disease",
                              "which_inf_disease", "contrast-allergy", "gfr", "creat", "perf_status", "frail"]
            self.data = [self.forename.get(), self.surname.get(), self.hosp_no.get(), self.dob.get(), self.sex.get(),
                         self.fresh_blood.get(), self.dark_blood.get(), self.loose_stools.get(),
                         self.constipation.get(), self.lif_pain.get(), self.abdo_pain.get(),
                         self.wt_loss.get(), self.id_anaemia.get(), self.fob.get(), self.hist_neoplasia.get(),
                         self.prev_resect.get(), self.abdo_mass.get(), self.rectal_mass.get(), self.pacemaker.get(),
                         self.heart_valve.get(), self.diabetic.get(), self.anticoag.get(),
                         self.infect_disease.get(), self.which_inf_disease.get(), self.contrast_allergy.get(),
                         self.gfr.get(), self.creat.get(), self.perf_status.get(), self.frail.get(),
                         self.comments.get()]

            self.form_data = dict(zip(self.variables, self.data))

            # reads symptoms into list
            self.symptom_list = []
            for symptom in self.form_data:
                if self.form_data[symptom] == True:
                    self.symptom_list.append(symptom)
            self.tests = self.determine_test(self.symptom_list)
            self.form_complete_button.destroy()
            # display recommended tests
            self.recommendation = ""
            Label(self, text="Suggested test(s):- ").grid(row=38, column=0, sticky=W)
            self.test_recommend = Text(self, width=75, height=1, wrap=WORD)
            self.test_recommend.grid(row=38, column=1, sticky=W, columnspan=3)
            self.test_recommend.delete(0.0, END)
            self.recommendation = " ".join(self.tests)
            self.test_recommend.insert(0.0, self.recommendation)

            # renal failure warning needs work

            # if "CT" in self.tests and int(self.form_data["gfr"])<40:
            # Label(self,text= "Warning: Renal impairment- If proceeding with CT, IV contrast contra-indicated").grid(row=39,column=0,sticky=W)
            self.manual_choose_tests_run = BooleanVar()  # used later for identifing widgets to be cleared
            self.manual_choose_tests_run = False
            self.accept_tests = Button(self, text="Accept Recommended Tests", command=self.accept_recommendation)
            self.choose_tests = Button(self, text="Choose Tests Manually", command=self.manual_choose_tests)
            self.accept_tests.grid(row=40, column=0, sticky=W)
            self.choose_tests.grid(row=40, column=1, sticky=W)

    def determine_test(self, symptoms):
        """"generates list of appropriate tests"""
        self.testlist = []
        if "frail" in symptoms:
            if "dark_blood" in symptoms or "loose_stools" in symptoms or "id_anaemia" in symptoms or "fob" in symptoms or "hist_neoplasia" in symptoms or "abdo-pain" in symptoms or "wt-loss" in symptoms:
                self.testlist.append("CT")
            if "fresh_blood" in symptoms or "dark_blood" in symptoms or "rectal_mass" in symptoms or "constipation" in symptoms:
                self.testlist.append("flexible sigmoidoscopy")
        else:
            if "dark_blood" in symptoms or "loose_stools" in symptoms or "id_anaemia" in symptoms or "fob" in symptoms or "hist_neoplasia" in symptoms:
                self.testlist.append("colonoscopy")
            elif "fresh_blood" in symptoms or "lif_pain" in symptoms or "rectal_mass" in symptoms or "constipation" in symptoms:
                self.testlist.append("flexible sigmoidoscopy")
            if "wt-loss" in symptoms or "abdo_mass" in symptoms or "abdo-pain" in symptoms in symptoms:
                self.testlist.append("CT")
            if "id_anaemia" in symptoms:
                self.testlist.append("gastroscopy")

        return self.testlist

    def accept_recommendation(self):
        """Accept recommended investigations"""
        self.chosen_tests = self.tests
        self.save_form()

    def manual_choose_tests(self):
        """generate checkbuttons to manually select tests"""
        self.choose_tests.destroy()
        self.accept_tests.destroy()

        self.manual_choose_tests_run = True
        self.select_test_label = Label(self, text="Select Test(s):-")
        self.select_test_label.grid(row=40, column=0, sticky=W)
        self.choose_flex_sigi = BooleanVar()
        self.choose_flex_sigi_button = Checkbutton(self, text="Flexible Sigmoidoscopy", variable=self.choose_flex_sigi)
        self.choose_flex_sigi_button.grid(row=40, column=1, sticky=W)
        self.choose_colonoscopy = BooleanVar()
        self.choose_colonoscopy_button = Checkbutton(self, text="Colonoscopy", variable=self.choose_colonoscopy)
        self.choose_colonoscopy_button.grid(row=40, column=2, sticky=W)
        self.choose_gastroscopy = BooleanVar()
        self.choose_gastroscopy_button = Checkbutton(self, text="Gastroscopy", variable=self.choose_gastroscopy)
        self.choose_gastroscopy_button.grid(row=40, column=3, sticky=W)
        self.choose_ct = BooleanVar()
        self.choose_ct_button = Checkbutton(self, text="CT", variable=self.choose_ct)
        self.choose_ct_button.grid(row=40, column=4, sticky=W)
        self.confirm_choose = Button(self, text="Confirm Selection", command=self.confirm_selection)
        self.confirm_choose.grid(row=41, column=0, sticky=W)

    def confirm_selection(self):
        """reads buttons for manually selected tests"""
        self.chosen_tests = []
        if self.choose_flex_sigi.get() == True:
            self.chosen_tests.append("flexible sigmoidoscopy")
        if self.choose_colonoscopy.get() == True:
            self.chosen_tests.append("colonoscopy")
        if self.choose_ct.get() == True:
            self.chosen_tests.append("CT")
        if self.choose_gastroscopy.get() == True:
            self.chosen_tests.append("gastroscopy")
        self.save_form()

    def save_form(self):
        """saves form data and closes data entry form"""
        # add recommended and selected tests to form dictionary-  superceeded since now uses database
        self.form_data["recommended_tests"] = self.tests
        self.form_data["tests_selected"] = self.chosen_tests
        # pickle form dictionary
        if self.form_data["hosp_no"] == "":
            self.form_data["hosp_no"] = "1"
        #self.pickle_file_name = "colo2wr pickle/" + self.form_data["hosp_no"]
        #self.save_pickle_form = open(self.pickle_file_name, "wb")
        #pickle.dump(self.form_data, self.save_pickle_form)
        #self.save_pickle_form.close()

        # self.save_to_database()

        self.check_need_bp()
        # check pickle
        # self.load_pickle_form=open(self.pickle_file_name, "rb")
        # self.check=pickle.load(self.load_pickle_form)
        # self.load_pickle_form.close()
        # print("pickle check", str(self.check))

    def check_need_bp(self):
        """checks wheter bowel prep needed"""

        self.bp_for_fsigi_label = Label(self,
                                        text="Should the flexible sigmoidoscopy be carried out with bowel prep or an enema?")
        self.bp_for_fsigi_bpbutton = Button(self, text="Bowel Prep", command=self.bp_now)
        self.bp_for_fsigi_enemabutton = Button(self, text="Enema", command=self.enema_now)
        self.bp_for_colonoscopy_label = Label(self, text="Bowel prep will be needed for colonoscopy")

        if "flexible sigmoidoscopy" in self.chosen_tests:
            self.bp_for_fsigi_label.grid(row=40, column=0, sticky="W")
            self.bp_for_fsigi_bpbutton.grid(row=40, column=1, sticky="W")
            self.bp_for_fsigi_enemabutton.grid(row=40, column=2, sticky="W")

        elif "colonoscopy" in self.chosen_tests:
            self.bp_for_colonoscopy_label.grid(row=40, column=0, sticky=W)
            self.bp_now()
        if self.manual_choose_tests_run:
            self.old_widgets = [self.select_test_label, self.choose_flex_sigi_button, self.choose_colonoscopy_button,
                                self.choose_gastroscopy_button, self.choose_ct_button, self.confirm_choose,
                                self.accept_tests, self.choose_tests]
        else:
            self.old_widgets = [self.accept_tests, self.choose_tests]
        for widget in self.old_widgets:
            widget.destroy()

        self.new_patient_button = Button(self, text="Save and Close", command=self.save_close)
        self.new_patient_button.grid(row=45, column=2, sticky=W)

    def bp_now(self):
        Button(self, text="Prescribe Bowel prep now?", command=self.make_bpf).grid(row=45, column=0, sticky=W)

    def enema_now(self):
        # need to store enema information
        self.enema = True

    def make_bpf(self):
        root2 = Toplevel(self.master)
        root2.title("Prescribe Bowel Prep")
        self.bpf1 = Bpf(root2)

    def save_close(self):
        """saves patient entry form data and closes current form"""
        self.save_to_database()
        app.most_recent_patient_numb = self.form_data["hosp_no"]
        app.root3.destroy()

    def save_to_database(self):
        """writes data from form into sqlite database"""
        self.list_for_db = []
        for item in self.data:
            if item == True:
                self.list_for_db.append(1)
            elif item == False:
                self.list_for_db.append(0)
            else:
                self.list_for_db.append(item)

        self.conn = sqlite3.connect("colotwr.db")
        self.curr = self.conn.cursor()
        self.curr.execute('''
        SELECT * FROM patient where hosp_no=?
        ''', (self.list_for_db[2],))
        self.patient_in_database = self.curr.fetchone()
        self.save_variable_tup = self.list_for_db[5:29]
        self.test_codes = {"colonoscopy": 1, "flexible sigmoidoscopy": 2, "gastroscopy": 3, "CT": 4, "CTC": 5}
        self.selected_test_codes = []
        for test in self.chosen_tests:
            self.selected_test_codes.append(self.test_codes[test])
        if self.patient_in_database is None:
            self.curr.execute('''
            INSERT INTO patient (hosp_no,forename,surname,dob,sex) VALUES (?,?,?,?,?)
            ''', (
            self.list_for_db[2], self.list_for_db[0], self.list_for_db[1], self.list_for_db[3], self.list_for_db[4],))
        self.curr.execute('''
        INSERT INTO event (hosp_no,fresh_blood, dark_blood, loose_stools, constipation, lif_pain, abdo_pain, wt_loss, id_anaemia, fob, hist_neoplasia, prev_resect, abdo_mass, rectal_mass, pacemaker, heart_valve, diabetic, anticoag, infect_disease, which_inf_disease, contrast_allergy, gfr, creat, perf_status, frail, ACE, diuretic, nsaid, prep_given, which_prep,user_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
        ''', (self.list_for_db[2], self.save_variable_tup[0], self.save_variable_tup[1], self.save_variable_tup[2],
              self.save_variable_tup[3], self.save_variable_tup[4], self.save_variable_tup[5],
              self.save_variable_tup[6], self.save_variable_tup[7], self.save_variable_tup[8],
              self.save_variable_tup[9], self.save_variable_tup[10], self.save_variable_tup[11],
              self.save_variable_tup[12], self.save_variable_tup[13], self.save_variable_tup[14],
              self.save_variable_tup[15], self.save_variable_tup[16], self.save_variable_tup[17],
              self.save_variable_tup[18], self.save_variable_tup[19], self.save_variable_tup[20],
              self.save_variable_tup[21], self.save_variable_tup[22], self.save_variable_tup[23],
              self.bowel_prep_outcome[1],self.bowel_prep_outcome[2],self.bowel_prep_outcome[3],self.bowel_prep_outcome[4],self.bowel_prep_outcome[5],app.user_name),)




        self.curr.execute('SELECT MAX(event_no)from(SELECT event_no FROM event WHERE hosp_no=?)',
                          (self.list_for_db[2],))
        self.event_no = self.curr.fetchone()
        self.curr.execute('INSERT INTO ptl(event_no,ptl_status,mdt_status) VALUES (?,?,?)',
                              (self.event_no[0], 1,0,))
        for code in self.selected_test_codes:
            self.curr.execute('INSERT INTO invest_from_event(event_no,invest_id) VALUES (?,?)',
                              (self.event_no[0], code,))
        self.curr.execute("""
        UPDATE event SET gfr=? WHERE event_no =?""",(self.bowel_prep_outcome[0],self.event_no[0],))    #puts gfr in database if set during bowel prep prescription rather than on clinic form
        self.conn.commit()
        self.conn.close()

class Bpf(Frame):
    """generates  bowel prep form"""
    def __init__(self, master):
        super(Bpf, self).__init__(master)
        self.grid()
        self.make_bp_widgets()
        self.medlist = []

    def make_bp_widgets(self):
        # check absolute contraindications-1 generate buttons
        Label(self, text="Please confirm that the patient does NOT have:").grid(row=1, column=0, sticky=W)
        self.obstruction = BooleanVar()
        self.c1 = Checkbutton(self, text="Gastrointestinal obstruction, ileus or perforation",
                              variable=self.obstruction).grid(row=2, column=0, sticky=W)
        self.ibd = BooleanVar()
        Checkbutton(self, text="Severe Inflammatory Bowel Disease", variable=self.ibd).grid(row=3, column=0, sticky=W)
        self.toxic_megacolon = BooleanVar()
        Checkbutton(self, text="Toxic Megacolon", variable=self.toxic_megacolon).grid(row=4, column=0, sticky=W)
        self.red_conc = BooleanVar()
        Checkbutton(self, text="Reduced Conscious Level", variable=self.red_conc).grid(row=5, column=0, sticky=W)
        self.hypersens = BooleanVar()
        Checkbutton(self, text="Hypersensitivity to any ingredients", variable=self.hypersens).grid(row=6, column=0,
                                                                                                    sticky=W)
        self.dysphagia = BooleanVar()
        Checkbutton(self, text="Dysphagia", variable=self.dysphagia).grid(row=7, column=0, sticky=W)
        self.ileostomy = BooleanVar()
        Checkbutton(self, text="An ileostomy", variable=self.ileostomy).grid(row=8, column=0, sticky=W)
        self.active_contra = []
        # Label(self,text="got to here").grid(row=9,column=0)
        Button(self, text="Confirm", command=self.confirm_contraindications).grid(row=10, column=0, sticky=W)

    def contralabel(self):
        if len(self.active_contra) > 0:
            no_active_contra = str(len(self.active_contra))
            self.contrawarning = Label(self,
                                       text="There appears to be " + no_active_contra + " absolute contraindications to bowel prep.")
            self.contrawarning.grid(row=11, column=0, sticky=W)
            self.contrawarning2 = Label(self,
                                        text="If this a mistake, tick the missing boxes now and press confirm-otherwise close this form and select tests not requiring bowel prep")
            self.contrawarning2.grid(row=12, column=0, sticky=W)
            # closebutton=Button(self,text="Close bowel prep form", command=self.destroy()).grid(row=13,column=0,sticky=W)
        else:
            self.contrawarning = Label(self,
                                       text="There appears to be no absolute contraindications to bowel prep.").grid(
                row=11, column=0, sticky=W)
            self.contrawarning2 = Label(self, text="  ")
            self.contrawarning2.grid(row=12, column=0)
            self.contrawarning2.destroy()
            self.renal_check()

    # check absolute contraindications-1 read and process buttons
    def confirm_contraindications(self):
        self.active_contra = []
        for contra in [self.obstruction, self.ibd, self.toxic_megacolon, self.red_conc, self.hypersens, self.dysphagia,
                       self.ileostomy]:
            current_contra = contra.get()
            if not current_contra:  # looks for unchecked boxes
                self.active_contra.append(current_contra)

        self.contralabel()

    def renal_check(self):
        """gets gfr from form_data dictionary-if not previously entered, creates entry dialogue"""
        self.entered_gfr = app.referal.form_data.get('gfr')
        if self.entered_gfr == "":
            Label(self, text="You have not entered the patient's eGFR yet-please enter it now").grid(row=12, column=0,
                                                                                                     sticky=W)
            self.new_gfr = Entry(self)
            self.new_gfr.grid(row=12, column=2)
            gfr_entry_button = Button(self, text="Enter", command=self.gfr_entry)
            gfr_entry_button.grid(row=12, column="3", sticky=W)
        else:
            self.display_gfr()

    def gfr_entry(self):
        """gets entered GFR an checks validity"""
        self.entered_gfr_new = self.new_gfr.get()
        self.not_a_number_gfr = Label(self, text="The GFR entry is not a valid number-try again")

        for digit in self.entered_gfr_new:
            if not digit in string.digits:
                self.not_a_number_gfr.grid(row=13, column=0)
        self.integer_gfr = int(self.entered_gfr_new)

        if self.integer_gfr < 0 or self.integer_gfr > 100:
            self.not_a_number_gfr.grid(row=13, column=0)
        else:
            self.make_medication_widgets()

    def display_gfr(self):
        """displays previously entered GFR and allows confirmation """

        self.prev_gfr_label = Label(self,
                                    text="You previously entered the patient's eGFR as " + self.entered_gfr + ".  Is this correct?")
        self.prev_gfr_label.grid(row=12, column=0, sticky=W)
        self.prev_gfr_yes_button = Button(self, text="Yes", command=self.confirm_gfr)
        self.prev_gfr_no_button = Button(self, text="No", command=self.deny_gfr)
        self.prev_gfr_yes_button.grid(row=12, column=1, sticky=W)
        self.prev_gfr_no_button.grid(row=12, column=2, sticky=W)

    def confirm_gfr(self):
        """callout function for yes button"""
        self.not_a_number_gfr = Label(self, text="The GFR entry is not a valid number-try again")

        for digit in self.entered_gfr:
            if not digit in string.digits:
                self.not_a_number_gfr.grid(row=13, column=0)
        self.integer_gfr = int(self.entered_gfr)
        if self.integer_gfr < 0 or self.integer_gfr > 100:
            self.not_a_number_gfr.grid(row=13, column=0)
        else:
            self.make_medication_widgets()

    def deny_gfr(self):
        """callout for no button"""
        self.prev_gfr_label.destroy()
        self.prev_gfr_yes_button.destroy()
        self.prev_gfr_no_button.destroy()
        self.reenter_gfr_label = Label(self, text="OK - Enter the correct value now")
        self.reenter_gfr_label.grid(row=12, column=0, sticky=W)
        self.new_gfr = Entry(self)
        self.new_gfr.grid(row=13, column=2)
        gfr_entry_button = Button(self, text="Enter", command=self.gfr_entry)
        gfr_entry_button.grid(row=13, column="3", sticky=W)

    def make_medication_widgets(self):
        """makes checkbutton widgets for entering medications"""
        # check absolute contraindications-1 generate buttons
        Label(self, text="Is the patient taking:").grid(row=14, column=0, sticky=W)
        self.ace = BooleanVar()
        Checkbutton(self, text="An ACE inhibitor", variable=self.ace).grid(row=15, column=0, sticky=W)
        self.diuretic = BooleanVar()
        Checkbutton(self, text="A Diuretic", variable=self.diuretic).grid(row=16, column=0, sticky=W)
        self.nsaid = BooleanVar()
        Checkbutton(self, text="An NSAID", variable=self.nsaid).grid(row=17, column=0, sticky=W)
        self.med_warning_prev_run = FALSE  # setup flag variable used later to allow deletion of messaged on medication change

        Button(self, text="Confirm", command=self.confirm_medication).grid(row=18, column=0, sticky=W)

    def confirm_medication(self):
        """callout for confirm button in make_medication_widgets to get medications"""
        self.ace_checked = self.ace.get()
        self.diuretic_checked = self.diuretic.get()
        self.nsaid_checked = self.nsaid.get()
        self.show_med_warning=False
        for med in ((self.ace_checked, "ace"), (self.diuretic_checked, "diuretic"), (self.nsaid_checked, "nsaid")):
            if med[0]:
                self.medlist.append(med[1])
                self.show_med_warning=True
            else:
                self.medlist.append("no")
        if self.show_med_warning:
            self.generate_med_warnings(self.medlist)
        else:
            if self.med_warning_prev_run:
                self.med_warning_box.destroy()
        self.choose_prep()

    def generate_med_warnings(self, medlist_for_warnings):
        "generates sdvice on medication stoppage and boxes to indicate stoppage"

        # lines to deal with eventuality of entry mistake and drugs being re-entered- list is passed to function as med
        self.med_warning_prev_run = TRUE


        self.med_warning_box = Text(self, width=75, height=9, wrap=WORD)
        self.med_warning_box.grid(row=19, column=0, columnspan=5, sticky=W)
        self.med_warning_message = "Stoppage of ACE inhibitors and NSAIDS is generally recommended in patients taking bowel prep (particularly picolax) on the day before taking the bowel prep recommencing 72 hours day the colonoscopy particularly in patients with poor renal function. Diuretics should if possible be omitted on the day of the bowel prep "
        self.bp_tab_warning = "If the patient has severe hypertension or heart failure or has had adverse effects from stopping cardiac or blood pressure medication in the past it would however be advisable not to sop these.  "
        self.nsaid_warning = "If the patient has severe arthritis is may not be feasible to stop the NSAID and this can be continued particularly if no concern about renal function"
        if "ace" in medlist_for_warnings or "diuretic" in medlist_for_warnings:
            self.med_warning_message += self.bp_tab_warning
        if "nsaid" in medlist_for_warnings:
            self.med_warning_message += self.nsaid_warning

        self.med_warning_box.insert(0.0, self.med_warning_message)
        self.choose_prep()

    def choose_prep(self):
        """displays checkboxes to chose type of bowel prep"""
        self.chosen_prep = StringVar(self)
        self.chosen_prep.set(None)
        Label(self, text="Select Bowel Prep:").grid(row=24, column=0, sticky=W)
        prep_options = ["Moviprep", "Kleenprep"]
        self.no_picolax = Label(self, text="Picolax is contra_indicated due to poor renal function")
        if self.integer_gfr >= 30:
            prep_options.append("Picolax")
        else:
            self.no_picolax.grid(row=25, column=0)

        rows = 26
        for prep in prep_options:
            self.prepbutton = Radiobutton(self, text=prep, variable=self.chosen_prep, value=prep)
            self.prepbutton.grid(row=rows, column=0, sticky=W)
            rows += 1
        self.prescribe_now_button=Button(self,text="Prescribe Now",command=self.complete_bp_prescription)
        self.prescribe_now_button.grid(row=30,column=0)

    def complete_bp_prescription(self):
        """gets selected bowel prep and saves to database - nb:will need additional code to print prescription of e-mail to pharmacy """

        self.selected_prep=self.chosen_prep.get()
        app.referal.bowel_prep_outcome=[self.integer_gfr,self.medlist[0], self.medlist[1], self.medlist[2], "yes", self.selected_prep]
        app.referal.bpf1.destroy()


class EndoscopyForm(Frame):
    """Generates form to record endoscopy outcomes"""
    def __init__(self, master):
        super(EndoscopyForm, self).__init__(master)
        self.grid()
        self.create_find_patient_widgets()

    def create_find_patient_widgets(self):
        """Root function for generating form items"""
        self.first_attempt = True  # sets flag used in destruction of file not found notice

        # widgets for hospital number entry
        Label(self, text="Patient information and outcome recording form").grid(row=0, column=0, columnspan=4, sticky=W)
        Label(self, text="Enter Patient Hospital Number").grid(row=3, column=0, sticky=W)
        self.hosp_no = Entry(self)
        self.hosp_no.grid(row=3, sticky=W, column=1)
        Button(self, text="Enter", command=self.patient_lookup).grid(row=3, column=2, sticky=W)

    def patient_lookup(self):
        """looks up patient database"""
        self.look_up_no = self.hosp_no.get()
        try:
            if not self.first_attempt:  # clears any previous form not found notification
                self.not_found.destroy()

            # following lines are superceeded - patient data now accessed from database
            # self.pickle_file_name = "colo2wr pickle/"+self.look_up_no
            # self.load_pickle_form=open(self.pickle_file_name, "rb")
            # self.endoscopy_patient_data=pickle.load(self.load_pickle_form)
            # self.load_pickle_form.close()


            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            SELECT COUNT(*) FROM patient WHERE hosp_no=?
            """, (self.look_up_no,))
            self.good_look_up_no = self.cur.fetchone()
            if self.good_look_up_no[0] > 0:
                self.cur.execute("""
                SELECT forename, surname, dob FROM patient where hosp_no=?
                """, (self.look_up_no,))
                self.endoscopy_patient_data = self.cur.fetchone()
                self.endoscopy_patient_found()
            else:
                self.not_found = Label(self, text="No patient found with this number- Check the number and try again")
                self.not_found.grid(row=4, column=0, sticky=W)
                self.first_attempt = False  # sets flag that not first attmpt -used to clear form not found notification
                self.look_up_no = None
                self.create_find_patient_widgets()
            self.conn.close()
        except:
            self.not_found = Label(self, text="There was a problem accessing the database")
            self.not_found.grid(row=4, column=0, sticky=W)
            self.first_attempt = False  # sets flag that not first attmpt -used to clear form not found notification
            self.look_up_no = None
            self.create_find_patient_widgets()

    def endoscopy_patient_found(self):
        self.full_patient_name = self.endoscopy_patient_data[0] + " " + self.endoscopy_patient_data[1]
        self.dob = self.endoscopy_patient_data[2]
        self.name_dob = Label(self, text=self.full_patient_name + "     ,DOB:" + self.dob)
        self.name_dob.grid(row=5, column=0, sticky=W)
        self.confirm_correct_label = Label(self, text="Is this the correct patient?")
        self.confirm_yes = Button(self, text="Yes", command=self.confirm_yes_process)
        self.confirm_no = Button(self, text="No", command=self.confirm_no_process)
        self.confirm_correct_label.grid(row=6, column=0, sticky=W)
        self.confirm_yes.grid(row=6, column=1, sticky=W)
        self.confirm_no.grid(row=6, column=2, sticky=W)

    def confirm_yes_process(self):
        self.create_rest_of_widgets()

    def confirm_no_process(self):
        self.confirm_no_message = Label(self, text="Ok-Try re-entering the hospital number")
        self.confirm_correct_label.destroy()
        self.confirm_yes.destroy()
        self.confirm_no.destroy()
        self.confirm_no_message.grid(row=6, column=0, sticky=W)

    def create_rest_of_widgets(self):
        """creates widgets to display patient info an outcome form"""
        self.confirm_correct_label.destroy()
        # self.confirm_yes.destroy()
        self.confirm_no.destroy()

        self.show_letter_button = Button(self, text="Display clinic letter", command=self.show_letter)
        self.show_letter_button.grid(row=7, column=0, sticky=W)

        # set up radiobuttons for endoscopy outcome
        Label(self, text="Endoscopy Outcome").grid(row=6, column=0, sticky=W)
        self.endoscopy_outcome = StringVar()
        self.endoscopy_outcome.set(None)
        self.outcome_choice = ["1. Completed procedure. No suspicion of cancer. No biopsies taken",
                               "2. Completed procedure. No suspicion of cancer. Random biopsies taken ",
                               "3. Completed procedure. No suspicion of cancer. Haemorrhoids banded",
                               "4. Polyps removed or biopsied. No strong suspicion of cancer",
                               "5. Colitis   (no evidence of carcinoma)",
                               "6 Incomplete colonoscopy-no suspicion of cancer to limit of examination",
                               "7. Polyp removed or biopsied.  Uncertain whether benign or malignant",
                               "8. Strong suspicion of carcinoma.",
                               "9. Other concerns regarding need for further investigation to exclude cancer including significant ongoing weight loss "]

        row = 11
        for outcome in self.outcome_choice:
            Radiobutton(self, text=outcome, variable=self.endoscopy_outcome, value=int(outcome[0])).grid(row=row,
                                                                                                         column=0,
                                                                                                         sticky=W)
            row += 1
        self.accept_outcome_button = Button(self, text="Confirm selected outcome", command=self.select_outcome)
        self.accept_outcome_button.grid(row=20, column=0, sticky=W)

    def show_letter(self):

        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""
            SELECT Count(*) from clinic_letters natural JOIN event WHERE hosp_no = ?
        """, (self.look_up_no,))
            self.letter_exists = self.cur.fetchone()
            if self.letter_exists[0] > 0:
                self.cur.execute('''SELECT letter FROM (event natural join clinic_letters) WHERE hosp_no=?''',
                                 (self.look_up_no,))
                self.clinic_letter_text = self.cur.fetchall()
            else:
                self.clinic_letter_text = "There is no clinic letter on file for this patient"

            self.cur.close()
        except TypeError:
            self.clinic_letter_text = "There is a problem accessing clinic letters"
            self.cur.close()
        self.clinic_letter = Text(self, wrap=WORD)
        self.clinic_letter.grid(row=10, column=0, sticky=W, rowspan=20, columnspan=5, )
        self.clinic_letter.insert(INSERT, self.clinic_letter_text)
        self.hide_letter_button = Button(self, text="Hide Clinic Letter", command=self.hide_letter)
        self.hide_letter_button.grid(row=7, column=1, sticky=W)

    def hide_letter(self):
        self.clinic_letter.destroy()
        self.hide_letter_button.destroy()

    def select_outcome(self):

        self.selected_chosen_endoscopy_outcome = self.endoscopy_outcome.get()

        try:
            self.conn = sqlite3.connect("endoscopy outcomes.db")
            self.curr = self.conn.cursor()
            self.curr.execute('''
            SELECT Instructions FROM outcomes where Outcome=?''', (self.selected_chosen_endoscopy_outcome,))
            self.instructions = self.curr.fetchone()
            self.curr.execute('''
            SELECT Letter FROM outcomes where Outcome=?''', (self.selected_chosen_endoscopy_outcome,))
            self.letter = self.curr.fetchone()
            self.curr.close()
        except:
            Label(self, text="There is a problem connecting to the database to display recommendations").grid(row=20,
                                                                                                              column=0,
                                                                                                              sticky=W)
            self.conn.close()
        self.display_instructions = Text(self, wrap=WORD, width=90, height=4)
        self.display_instructions.grid(row=22, column=0, sticky=W)
        self.display_instructions.insert(INSERT, self.instructions)
        Label(self,
              text="The following clinic letter will be sent to the GP and patient-You can alter it now if needed. Press the accept letter button when you are happy the letter is OK").grid(
            row=25, column=0, sticky=W)
        self.display_letter = Text(self, wrap=WORD, width=90, height=10)
        self.display_letter.grid(row=30, column=0, sticky=W)
        self.display_letter.insert(INSERT, self.letter)
        self.accept_letter_button = Button(self, text="Accept Letter", command=self.save_endoscopy_outcome_letter)
        self.accept_letter_button.grid(row=40, column=0, sticky=W)

    def save_endoscopy_outcome_letter(self):
        self.edited_endoscopy_letter = self.display_letter.get("1.0", "end")
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        SELECT MAX(event_no) FROM event WHERE hosp_no=?
        """, (self.look_up_no,))
        self.endoscopy_event_no = self.cur.fetchone()
        self.cur.execute("""
        SELECT COUNT(*) FROM investigation_outcomes WHERE event_no=?
        """, (self.endoscopy_event_no[0],))
        self.no_results_yet = self.cur.fetchone()
        if self.no_results_yet[0] == 0:
            self.cur.execute("""
            INSERT INTO investigation_outcomes (event_no, lgi_endoscopy_outcome,endoscopy_letter) VALUES (?,?,?)
            """, (self.endoscopy_event_no[0], self.selected_chosen_endoscopy_outcome, self.edited_endoscopy_letter,))
            self.conn.commit()
            self.conn.close()
            Label(self, text="Endoscopy outcome has been saved").grid(row=60, column=0, sticky=W)
        else:
            self.cur.execute("""
            SELECT COUNT(*) FROM investigation_outcomes WHERE event_no = ? and lgi_endoscopy_outcome BETWEEN 0 and 7
            """, (self.endoscopy_event_no[0],))
            self.no_prev_endoscopy_report = self.cur.fetchone()
            if self.no_prev_endoscopy_report[0] == 0:
                self.cur.execute("""
                UPDATE investigation_outcomes SET lgi_endoscopy_outcome=? WHERE event_no=?
            """, (self.selected_chosen_endoscopy_outcome, self.endoscopy_event_no[0],))
                self.cur.execute("""
                UPDATE investigation_outcomes SET endoscopy_letter=? WHERE event_no=?
            """, (self.edited_endoscopy_letter, self.endoscopy_event_no[0],))
                self.conn.commit()
                self.conn.close()
                Label(self, text="Endoscopy outcome has been saved").grid(row=30, column=0, sticky=W)
            else:
                self.cur.execute("""
                SELECT lgi_endoscopy_outcome FROM investigation_outcomes WHERE event_no=?
                """, (self.endoscopy_event_no[0],))

                self.prev_endoscopy_outcome = self.cur.fetchone()
                self.prev_endoscopy_warning = Label(self,
                                                    text="An outcome for this endoscopy appears to have been recorded already as outcome number %s Do you want to change it?" %
                                                         self.prev_endoscopy_outcome[0])
                self.prev_endoscopy_warning.grid(row=31, column=0, sticky=W)
                self.amend_endoscopy_outcome_button = Button(self, text="Amend Outcome",
                                                             command=self.amend_endoscopy_outcome)
                self.amend_endoscopy_outcome_button.grid(row=31, column=1, sticky=W)

    def amend_endoscopy_outcome(self):

        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        UPDATE investigation_outcomes SET lgi_endoscopy_outcome=? WHERE event_no=?
        """, (self.selected_chosen_endoscopy_outcome, self.endoscopy_event_no[0],))
        self.cur.execute("""
        UPDATE investigation_outcomes SET endoscopy_letter=? WHERE event_no=?
            """, (self.edited_endoscopy_letter, self.endoscopy_event_no[0],))
        self.conn.commit()
        self.conn.close()
        self.prev_endoscopy_warning.destroy()
        self.amend_endoscopy_outcome_button.destroy()
        Label(self, text="Endoscopy outcome has been updated").grid(row=30, column=0, sticky=W)


class CtForm(Frame):
    def __init__(self, master):
        super(CtForm, self).__init__(master)
        self.grid()
        self.create_find_patient_widgets()

    def create_find_patient_widgets(self):
        """Root function for generating form items"""
        self.first_attempt = True  # sets flag used in destruction of file not found notice

        # widgets for hospital number entry
        Label(self, text="Patient information and outcome recording form").grid(row=0, column=0, columnspan=4, sticky=W)
        Label(self, text="Enter Patient Hospital Number").grid(row=3, column=0, sticky=W)
        self.hosp_no = Entry(self)
        self.hosp_no.grid(row=3, sticky=W, column=1)
        Button(self, text="Enter", command=self.patient_lookup).grid(row=3, column=2, sticky=W)

    def patient_lookup(self):
        """looks up patient database"""
        self.look_up_no = self.hosp_no.get()
        try:
            if not self.first_attempt:  # clears any previous form not found notification
                self.not_found.destroy()

            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            SELECT COUNT(*) FROM patient WHERE hosp_no=?
            """, (self.look_up_no,))
            self.good_look_up_no = self.cur.fetchone()
            if self.good_look_up_no[0] > 0:
                self.cur.execute("""
                SELECT forename, surname, dob FROM patient where hosp_no=?
                """, (self.look_up_no,))
                self.ct_patient_data = self.cur.fetchone()
                self.conn.close()
                self.ct_patient_found()
            else:
                self.not_found = Label(self, text="No patient found with this number- Check the number and try again")
                self.not_found.grid(row=4, column=0, sticky=W)
                self.first_attempt = False  # sets flag that not first attmpt -used to clear form not found notification
                self.look_up_no = None
                self.create_find_patient_widgets()
            self.conn.close()
        except:
            self.not_found = Label(self, text="There was a problem accessing the database")
            self.not_found.grid(row=4, column=0, sticky=W)
            self.first_attempt = False  # sets flag that not first attmpt -used to clear form not found notification
            self.look_up_no = None
            self.create_find_patient_widgets()
            self.conn.close

    def ct_patient_found(self):
        self.full_patient_name = self.ct_patient_data[0] + " " + self.ct_patient_data[1]
        self.dob = self.ct_patient_data[2]
        self.name_dob = Label(self, text=self.full_patient_name + "     ,DOB:" + self.dob)
        self.name_dob.grid(row=5, column=0, sticky=W)
        self.confirm_correct_label = Label(self, text="Is this the correct patient?")
        self.confirm_yes = Button(self, text="Yes", command=self.confirm_yes_process)
        self.confirm_no = Button(self, text="No", command=self.confirm_no_process)
        self.confirm_correct_label.grid(row=6, column=0, sticky=W)
        self.confirm_yes.grid(row=6, column=1, sticky=W)
        self.confirm_no.grid(row=6, column=2, sticky=W)

    def confirm_yes_process(self):
        self.create_rest_of_widgets()

    def confirm_no_process(self):
        self.confirm_no_message = Label(self, text="Ok-Try re-entering the hospital number")
        self.confirm_correct_label.destroy()
        self.confirm_yes.destroy()
        self.confirm_no.destroy()
        self.confirm_no_message.grid(row=6, column=0, sticky=W)

    def create_rest_of_widgets(self):
        """creates widgets to display patient info an outcome form"""
        self.confirm_correct_label.destroy()
        # self.confirm_yes.destroy()
        self.confirm_no.destroy()

        self.show_letter_button = Button(self, text="Display clinic letter", command=self.show_letter)
        self.show_letter_button.grid(row=7, column=0, sticky=W)

        # set up radiobuttons for ct outcome
        Label(self, text="CT Outcome").grid(row=8, column=0, sticky=W)
        self.ct_outcome = StringVar()
        self.ct_outcome.set(None)
        self.ct_outcome_choice = ["1. No findings needing which require urgent attention.",
                                  "2. Suspicion of colorectal cancer",
                                  "3. Suspicion of other primary or secondary cancer",
                                  "4. Possible cancer -concern requiring MDT review.",
                                  "5. Indeterminate findings- Extra Imaging advised prior to MDT review",
                                  "6. Benign disease which requires urgent clinical attention."]

        row = 11
        for outcome in self.ct_outcome_choice:
            Radiobutton(self, text=outcome, variable=self.ct_outcome, value=int(outcome[0])).grid(row=row, column=0,
                                                                                                  sticky=W)
            row += 1
        self.accept_outcome_button = Button(self, text="Confirm selected outcome", command=self.save_ct_outcome)
        self.accept_outcome_button.grid(row=20, column=0, sticky=W)

    def show_letter(self):

        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""
            SELECT Count(*) from clinic_letters natural JOIN event WHERE hosp_no = ?
        """, (self.look_up_no,))
            self.letter_exists = self.cur.fetchone()
            if self.letter_exists[0] > 0:
                self.cur.execute('''SELECT letter FROM (event natural join clinic_letters) WHERE hosp_no=?''',
                                 (self.look_up_no,))
                self.clinic_letter_text = self.cur.fetchall()
            else:
                self.clinic_letter_text = "There is no clinic letter on file for this patient"

            self.cur.close()
        except TypeError:
            self.clinic_letter_text = "There is a problem accessing clinic letters"
            self.cur.close()
        self.clinic_letter = Text(self, wrap=WORD)
        self.clinic_letter.grid(row=10, column=0, sticky=W, rowspan=20, columnspan=5, )
        self.clinic_letter.insert(INSERT, self.clinic_letter_text)
        self.hide_letter_button = Button(self, text="Hide Clinic Letter", command=self.hide_letter)
        self.hide_letter_button.grid(row=7, column=1, sticky=W)

    def hide_letter(self):
        self.clinic_letter.destroy()
        self.hide_letter_button.destroy()

    def save_ct_outcome(self):
        self.ct_outome_raw = self.ct_outcome.get()
        self.selected_chosen_ct_outcome = int(self.ct_outome_raw[0])
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        SELECT MAX(event_no) FROM event WHERE hosp_no=?
        """, (self.look_up_no,))
        self.ct_event_no = self.cur.fetchone()
        self.cur.execute("""
        SELECT COUNT(*) FROM investigation_outcomes WHERE event_no=?
        """, (self.ct_event_no[0],))
        self.no_results_yet = self.cur.fetchone()
        if self.no_results_yet[0] == 0:
            self.cur.execute("""
            INSERT INTO investigation_outcomes (event_no,ct_outcome) VALUES (?,?)
            """, (self.ct_event_no[0], self.selected_chosen_ct_outcome,))
            self.conn.commit()
            self.conn.close()
            Label(self, text="CT outcome has been saved").grid(row=30, column=0, sticky=W)
        else:
            self.cur.execute("""
            SELECT COUNT(*) FROM investigation_outcomes WHERE event_no = ? and ct_outcome BETWEEN 1 and 7
            """, (self.ct_event_no[0],))
            self.no_prev_ct_report = self.cur.fetchone()
            if self.no_prev_ct_report[0] == 0:
                self.cur.execute("""
                UPDATE investigation_outcomes SET ct_outcome=? WHERE event_no=?
            """, (self.selected_chosen_ct_outcome, self.ct_event_no[0],))
                self.conn.commit()
                self.conn.close()
                Label(self, text="CT outcome has been saved").grid(row=30, column=0, sticky=W)
            else:
                self.cur.execute("""
                SELECT ct_outcome FROM investigation_outcomes WHERE event_no=?
                """, (self.ct_event_no[0],))
                self.prev_ct_outcome = self.cur.fetchone()
                self.prev_ct_warning = Label(self,
                                             text="An outcome for this CT appears to have been recorded already as outcome number %s Do you want to change it?" %
                                                  self.prev_ct_outcome[0])
                self.prev_ct_warning.grid(row=31, column=0, sticky=W)
                self.amend_ct_outcome_button = Button(self, text="Amend Outcome", command=self.amend_ct_outcome)
                self.amend_ct_outcome_button.grid(row=31, column=1, sticky=W)

    def amend_ct_outcome(self):

        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        UPDATE investigation_outcomes SET ct_outcome=? WHERE event_no=?
        """, (self.selected_chosen_ct_outcome, self.ct_event_no[0],))
        self.conn.commit()
        self.conn.close()
        self.prev_ct_warning.destroy()
        self.amend_ct_outcome_button.destroy()
        Label(self, text="CT outcome has been updated").grid(row=30, column=0, sticky=W)


class AdminForm(Frame):
    def __init__(self, master):
        super(AdminForm, self).__init__(master)
        self.grid()
        self.create_admin_widgets()

    def create_admin_widgets(self):
        Label(self, text="Administrative Functions").grid(row=0, column=0)
        """Root function for generating form items for admin form"""
        self.user_in_button = Button(self, text="Add or Edit User", command=self.add_edit_user)
        self.user_out_button = Button(self, text="Delete User", command=self.delete_user)
        self.delete_event_button = Button(self, text="Delete clinic event", command=self.delete_event)
        self.user_in_button.grid(row=1, column=0, sticky=W)
        self.user_out_button.grid(row=1, column=1, sticky=W)
        self.delete_event_button.grid(row=2, column=0, sticky=W)

    def add_edit_user(self):
        """creates new record in use) table"""
        self.root5 = Toplevel(self.master)
        self.root5.title("Add or Edit User")
        self.editing_user = ManageUser(self.root5)

    def delete_user(self):
        """changes user status to 0"""
        """creates new record in use) table"""
        self.root6 = Toplevel(self.master)
        self.root6.title("Delete User")
        self.editing_user = DeleteUser(self.root6)

    def delete_event(self):
        pass


class ManageUser(Frame):
    """Allows creation of new user or editing of existing user"""

    def __init__(self, master):
        super(ManageUser, self).__init__(master)
        self.grid()
        self.create_manage_user_widgets()

    def create_manage_user_widgets(self):
        self.new_user_button = Button(self, text="Create New User", command=self.create_new_user)
        self.edit_user_button = Button(self, text="Edit Existing User", command=self.edit_existing_user)
        self.new_user_button.grid(row=0, column=0, sticky=W)
        self.edit_user_button.grid(row=0, column=1, sticky=W)

    def create_new_user(self):
        self.new_user = True
        self.get_user_name()

    def edit_existing_user(self):
        self.new_user = False
        self.get_user_name()

    def get_user_name(self):
        self.uew_flag = False
        self.ude_flag = False
        self.user_name_label = Label(self, text="Enter a user name for a new user or an existing user you want to edit")
        self.user_name_label.grid(row=1, column=0, sticky=W)
        self.user_name_entry = Entry(self)
        self.user_name_entry.grid(row=1, column=1, sticky=W)
        self.user_name_button = Button(self, text="Enter", command=self.lookup_user)
        self.user_name_button.grid(row=1, column=2, sticky=W)

    def lookup_user(self):
        self.user_name_to_edit = self.user_name_entry.get()
        try:
            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            SELECT COUNT(*) from user where user_ID=?""", (self.user_name_to_edit,))
            self.user_exists = self.cur.fetchone()
            self.process_user()

        except TypeError:
            self.db_error_text = Label(self, text="There was a problem accessing the user database")
            self.db_error_text.grid(row=2, column=0, sticky=W)
            self.conn.close()
            self.retry = Button(self, text="Retry").grid(row=2, column=0, sticky=W)

    def process_user(self):
        if self.ude_flag:
            self.user_doesnt_exist_warning.destroy()
        if self.uew_flag:
            self.user_exists_warning.destroy()
        if self.new_user and self.user_exists[0] == 1:
            self.ude_flag = False
            self.user_exists_warning = Label(self, text="That user name exists-try a different user name")
            self.user_exists_warning.grid(row=2, column=0, sticky=W)
            self.conn.close()
            self.uew_flag = True  # indicates warning for distuction
        elif not self.new_user and self.user_exists[0] == 0:
            self.user_dosnt_exist_warning = Label(self,
                                                  text="That user name was not found - try re-entering a user name")
            self.user_dosnt_exist_warning.grid(row=2, column=0, sticky=W)
            self.conn.close()
            self.ude_flag = True  # indicates wrning for distruction
        elif self.new_user == False and self.user_exists[0] == 1:
            try:
                self.cur.execute("""
                SELECT * FROM user WHERE user_ID=?
                """, (self.user_name_to_edit,))
                self.user_data_to_edit = self.cur.fetchone()
                self.conn.close()
            except TypeError:
                self.db_error_text = Label(self, text="There was a problem accessing the user database")
                self.db_error_text.grid(row=3, column=0, sticky=W)
                self.conn.close()
        else:
            self.user_data_to_edit = ("", self.user_name_to_edit, "", "", "", "", "", "", "")

        self.user_name_label = Label(self, text="User Name")
        self.user_name_label.grid(row=5, column=0, sticky=W, )
        self.user_name_entry = Entry(self)
        self.user_name_entry.insert(END, self.user_data_to_edit[1])
        self.user_name_entry.grid(row=5, column=1)
        self.password_label = Label(self, text="Password")
        self.password_label.grid(row=6, column=0, sticky=W)
        self.password_entry = Entry(self)
        self.password_entry.insert(END, self.user_data_to_edit[2])
        self.password_entry.grid(row=6, column=1, sticky=W)
        self.first_name_label = Label(self, text="First Name")
        self.first_name_label.grid(row=7, column=0, sticky=W)
        self.first_name_entry = Entry(self)
        self.first_name_entry.insert(END, self.user_data_to_edit[5])
        self.first_name_entry.grid(row=7, column=1)
        self.last_name_label = Label(self, text="Last Name")
        self.last_name_label.grid(row=8, column=0, sticky=W)
        self.last_name_entry = Entry(self)
        self.last_name_entry.insert(END, self.user_data_to_edit[6])
        self.last_name_entry.grid(row=8, column=1)
        self.job_title_label = Label(self, text="Job Title")
        self.job_title_label.grid(row=9, column=0, sticky=W)
        self.job_title_entry = Entry(self)
        self.job_title_entry.insert(END, self.user_data_to_edit[7])
        self.job_title_entry.grid(row=9, column=1, sticky=W)

        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        if self.new_user:
            self.confirm_new_user_button = Button(self, text="Confirm new user", command=self.confirm_new_user)
            self.confirm_new_user_button.grid(row=10, column=0, sticky=W)
        else:
            self.edit_user_button = Button(self, text="Confirm Changes to User", command=self.confirm_edit_user)
            self.edit_user_button.grid(row=10, column=0, sticky=W)

    def confirm_new_user(self):
        self.un = self.user_name_entry.get()
        self.pw = self.password_entry.get()
        self.priv = 1
        self.admin = 0
        self.fn = self.first_name_entry.get()
        self.ln = self.last_name_entry.get()
        self.jt = self.job_title_entry.get()

        try:
            self.cur.execute("""
            INSERT into user (user_ID,password,privilege,admin,first_name,last_name,job_title) VALUES (?,?,?,?,?,?,?)
            """, (self.un, self.pw, self.priv, self.admin, self.fn, self.ln, self.jt,))
            self.conn.commit()
            self.conn.close()
            self.new_user_confirm = Label(self, text="New user successfully created")
            self.new_user_confirm.grid(row=11, column=0, sticky=W)

        except:
            self.conn.close()
            Label(self, text="There is a problem accessing the user database at present").grid(row=12, column=0,
                                                                                               sticky=W)

    def confirm_edit_user(self):
        self.un = self.user_name_entry.get()
        self.pw = self.password_entry.get()
        self.priv = 1
        self.admin = 0
        self.fn = self.first_name_entry.get()
        self.ln = self.last_name_entry.get()
        self.jt = self.job_title_entry.get()

        # try:
        self.cur.execute("""
        UPDATE user 
        SET user_ID=?,password=?,privilege=?,admin=?,first_name=?,last_name=?,job_title=?
        W    HERE user_ID=?
        """, (self.un, self.pw, self.priv, self.admin, self.fn, self.ln, self.jt, self.user_name_to_edit,))
        self.conn.commit()
        self.conn.close()
        self.edit_user_confirm = Label(self, text="User details successfully updated")
        self.edit_user_confirm.grid(row=11, column=0, sticky=W)
    # except:
    # self.conn.close()
    # Label(self, text="There is a problem accessing the user database at present").grid(row=12,column=0,sticky=W)


class DeleteUser(Frame):

    def __init__(self, master):
        super(DeleteUser, self).__init__(master)
        self.grid()
        self.create_delete_user_widgets()

    def create_delete_user_widgets(self):
        self.user_to_delete_label = Label(self, text=" User Name of User to be Deleted")
        self.user_to_delete_label.grid(row=0, column=0, sticky=W)
        self.user_to_delete_entry = Entry(self)
        self.user_to_delete_entry.grid(row=0, column=1, sticky=W)
        self.user_to_delete_button = Button(self, text="Enter", command=self.delete_user)
        self.user_to_delete_button.grid(row=0, column=2, sticky=W)

    def delete_user(self):
        self.user_to_delete = self.user_to_delete_entry.get()
        try:
            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            SELECT COUNT (*) FROM user WHERE user_ID=?
            """, (self.user_to_delete,))
            self.user_to_delete_exists = self.cur.fetchone()
        except:
            Label(self, text="Can't access user database").grid(row=1, column=0, sticky=W)
            Button(self, text="Try again", command=self.create_delete_user_widgets())

        if self.user_to_delete_exists[0] == 0:
            self.no_such_user_warning = Label(self, text="This user does not exist- try a different user name")
            self.no_such_user_warning.grid(row=1, column=0, sticky=W)
            self.conn.close()

        else:
            self.cur.execute("""
            SELECT first_name,last_name from user WHERE user_ID=?
            """, (self.user_to_delete,))
            self.name_of_user_from_db = self.cur.fetchone()
            self.conn.close()

        self.name_of_user_to_display = self.name_of_user_from_db[0] + " " + self.name_of_user_from_db[1]
        self.confirm_delete = Button(self, text="confirm delete %s" % (self.name_of_user_to_display),
                                     command=self.user_delete_confirmed)
        self.confirm_delete.grid(row=1, column=0, sticky=W)
        self.wrong_user = Button(self, text="No- Not that user", command=self.create_delete_user_widgets)
        self.wrong_user.grid(row=1, column=1, sticky=W)

    def user_delete_confirmed(self):
        try:
            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            DELETE FROM user WHERE USER_ID=?
            """, (self.user_to_delete,))
            self.conn.commit()
            self.conn.close()
            self.delete_confirmed = Label(self, text="User %s has been deleted" % (self.user_to_delete))
            self.delete_confirmed.grid(row=2, column=0, sticky=W)
        except:
            Label(self, text="Can't access user database").grid(row=2, column=0, sticky=W)
            Button(self, text="Try again", command=self.create_delete_user_widgets()).grid(row=2, column=0, sticky=W, )


class ClinicLetter(Frame):
    """Generates clinic letter based on information stored in database from clinic form and allows editing of letter. Defaults to clinic event just saved """
    def __init__(self, master):
        super(ClinicLetter, self).__init__(master)
        self.grid()
        self.create_clinic_letter_widgets()

    def create_clinic_letter_widgets(self):
        self.enter_number_label = Label(self, text="Enter patient number")
        self.enter_number_label.grid(row=1, column=0, sticky=W)
        self.enter_number = Entry(self)
        self.enter_number.grid(row=1, column=1, sticky=W)
        if app.most_recent_patient_numb != 0:
            self.enter_number.insert(END, app.most_recent_patient_numb)

        self.enter_hosp_numb_activate = Button(self, text="Enter", command=self.enter_hospital_number)
        self.enter_hosp_numb_activate.grid(row=2, column=0, sticky=W)

    def enter_hospital_number(self):
        self.hospital_number_entry = self.enter_number.get()
        self.conn = sqlite3.connect("colotwr.db")
        self.curr = self.conn.cursor()
        self.curr.execute('''
        SELECT * FROM patient where hosp_no=
        ?''', (self.hospital_number_entry,))
        try:
            self.patient_data_in_database = self.curr.fetchone()
        except TypeError:
            self.not_in_db = Label(self, text="There is no record for this patient. Try entering a different number")
            self.not_in_db.grid(row=4, column=0, sticky=W)
            self.enter_hosp_numb_activate.destroy()
            self.reenter_password = Button(self, text="Try Again", command=self.create_clinic_letter_widgets)
            self.reenter_password.grid(row=5, column=3, sticky=W)

        self.curr.execute('''
        SELECT * FROM event WHERE hosp_no = ? ORDER BY event_no DESC LIMIT 1
        ''', (self.hospital_number_entry,))
        try:
            self.event_data_in_database = self.curr.fetchone()
            self.event_number = self.event_data_in_database[0]
            self.get_data()
        except TypeError:
            self.not_in_db = Label(self, text="There is no record for this patient. Try entering a different number")
            self.not_in_db.grid(row=4, column=0, sticky=W)
            self.enter_hosp_numb_activate.destroy()
            self.reenter_password = Button(self, text="Try Again", command=self.create_clinic_letter_widgets)
            self.reenter_password.grid(row=5, column=3, sticky=W)

    def get_data(self):
        self.curr.execute('''
        SELECT investigation.invest FROM (investigation NATURAL JOIN invest_from_event) WHERE invest_from_event.event_no=?
        ''', (self.event_number,))
        try:
            self.investigation_ordered = self.curr.fetchall()
        except TypeError:
            self.investigation_ordered = ""
        self.curr.execute('''
        SELECT first_name, last_name, job_title FROM user WHERE user_ID=?
        ''', (app.user_name,))
        self.user_data = self.curr.fetchone()
        self.conn.commit()
        self.conn.close()
        self.enter_hosp_numb_activate.destroy()
        self.process_gender()

    def get_sex(self):
        """Callout for entry button for sex entry radioboxes"""
        self.sex_for_letter = self.sex_entry.get()
        self.get_sex_button.destroy()
        if self.sex_for_letter == "female":
            self.get_title()
        else:
            self.sex_for_letter = "male"
            self.title_for_letter = "Mr"
            self.pronoun_for_letter = "He"

            self.prepare_letter_text()

    def process_gender(self):
        """check if sex recorded in database - if not create entry checkboxes"""
        self.sex_for_letter = ""
        if self.patient_data_in_database[4] == "female":
            self.sex_for_letter = "female"
            self.get_title()
        elif self.patient_data_in_database[4] == "male":
            self.sex_for_letter = "male"
            self.title_for_letter = "Mr"
            self.pronoun_for_letter = "He"
            self.prepare_letter_text()
        else:
            self.gender_warning_text = Label(self,
                                             text="Patient's gender has not been previously entered- please enter now")
            self.gender_warning_text.grid(row=2, column=0, sticky=W)
            self.sex_entry = StringVar()
            self.sex_entry.set(None)
            Radiobutton(self, text="Male", variable=self.sex_entry, value="male").grid(row=2, column=1, sticky=E)
            Radiobutton(self, text="Female", variable=self.sex_entry, value="female").grid(row=2, column=2, sticky=W)
            self.get_sex_button = Button(self, text="Enter", command=self.get_sex)
            self.get_sex_button.grid(row=5, column=0, sticky=W)

    def get_title(self):
        self.pronoun_for_letter = "She"
        self.preferred_title = Label(self, text="Please specify preferred title")
        self.preferred_title.grid(row=5, column=0, sticky=W)
        self.title_entry = StringVar()
        self.title_entry.set(None)
        Radiobutton(self, text="Mrs", variable=self.title_entry, value="Mrs").grid(row=6, column=0, sticky=W)
        Radiobutton(self, text="Miss", variable=self.title_entry, value="Miss").grid(row=7, column=0, sticky=W)
        Radiobutton(self, text="Ms", variable=self.title_entry, value="Ms").grid(row=8, column=0, sticky=W)
        self.get_title_button = Button(self, text="Enter", command=self.activate_get_title)
        self.get_title_button.grid(row=9, column=0, sticky=W)

    def activate_get_title(self):
        self.title_for_letter = self.title_entry.get()
        self.prepare_letter_text()

    def prepare_letter_text(self):
        self.lower_pronoun = self.pronoun_for_letter.lower()
        self.symptoms = {1: "passage of fresh blood per rectum", 2: "passage of dark blood per rectum",
                         3: "loose stools", 4: "constipation", 5: "left iliac fossa pain", 6: "abdominal_pain",
                         7: "weight loss"}
        self.history = {1: "iron deficiency anaemia", 2: "a positive faecal occult blood test",
                        3: "a history of colonic neoplasia", 4: "a previous colorectal resection"}
        self.exam = {1: "an abdominal mass", 2: "a rectal_mass"}
        self.comorbidity = {1: "has a pacemaker", 2: "has an artificial heart valve", 3: "is diabetic",
                            4: "is on an anticoagulant"}
        self.symptom_list_for_letter = []
        self.history_for_letter = []
        self.exam_for_letter = []
        self.comorb_for_letter = []
        for symptom in range(2, 9):
            if self.event_data_in_database[symptom] == 1:
                self.symptom_list_for_letter.append(self.symptoms.get(symptom - 1))
        for history in range(9, 13):
            if self.event_data_in_database[history] == 1:
                self.history_for_letter.append(self.history.get(history - 8))
        for exam_finding in range(13, 15):
            if self.event_data_in_database[exam_finding] == 1:
                self.exam_for_letter.append(self.exam.get(exam_finding - 12))
        for co_morb in range(15, 17):
            if self.event_data_in_database[co_morb] == 1:
                if co_morb < 17:
                    self.comorb_for_letter.append((self.comorbidity.get(co_morb - 14)))
        if self.event_data_in_database[17] not in ["None", "not diabetic"]:
            self.comorb_for_letter.append("is a diabetic({})".format(self.event_data_in_database[17]))
        if self.event_data_in_database[18] not in ["None", "none or only aspirin"]:
            self.comorb_for_letter.append("is on an anti-coagulant({})".format(self.event_data_in_database[18]))

        self.new_paragraph = "\n\n"

        self.letter_text1 = "Dear Dr,\n\nThank you for referring {} {} under the colorectal two week rule. ".format(
            self.title_for_letter, self.patient_data_in_database[2])

        self.letter_text2 = "{} reports ".format(self.pronoun_for_letter)

        if len(self.symptom_list_for_letter) == 0:
            self.letter_text2 += "no symptoms.  "
        elif len(self.symptom_list_for_letter) == 1:
            self.letter_text2 += self.symptom_list_for_letter[0]
            self.letter_text2 += ".  "
        else:
            for item in range(0, (len(self.symptom_list_for_letter) - 1)):
                self.letter_text2 += self.symptom_list_for_letter[item]
                self.letter_text2 += ","
            self.letter_text2 += "and "
            self.letter_text2 += self.symptom_list_for_letter[(len(self.symptom_list_for_letter) - 1)]
            self.letter_text2 += ".  "

        self.letter_text3 = "{} has ".format(self.pronoun_for_letter)

        if len(self.history_for_letter) == 0:
            if len(self.comorb_for_letter) == 0:
                self.letter_text3 += "no significant medical history.  "
            else:
                self.letter_text3 += "some significant co_morbidity.  "
        elif len(self.history_for_letter) == 1:
            self.letter_text3 += self.history_for_letter[0]
            self.letter_text3 += ".  "
        else:
            for item in range(0, (len(self.history_for_letter) - 1)):
                self.letter_text3 += self.history_for_letter[item]
                self.letter_text3 += ","
            self.letter_text3 += "and "
            self.letter_text3 += self.history_for_letter[(len(self.history_for_letter) - 1)]
            self.letter_text3 += ".  "

        self.letter_text4 = ""
        if len(self.comorb_for_letter) != 0:
            self.letter_text4 = "{} has ".format(self.pronoun_for_letter)
            if len(self.comorb_for_letter) == 1:
                self.letter_text4 += self.comorb_for_letter[0]
                self.letter_text4 += ".  "
            else:
                for item in range(0, (len(self.comorb_for_letter) - 1)):
                    self.letter_text4 += self.comorb_for_letter[item]
                    self.letter_text4 += ","
                self.letter_text4 += "and "
                self.letter_text4 += self.comorb_for_letter[(len(self.comorb_for_letter) - 1)]
                self.letter_text4 += ".  "

        if len(self.exam_for_letter) == 0:
            self.letter_text5 = "Examination was unremarkable"
        elif len(self.exam_for_letter) == 1:
            self.letter_text5 = "Examination revealed {}.".format(self.exam_for_letter[0])
        else:
            self.letter_text5 = "Examination revealed {} and {}.".format(self.exam_for_letter[0],
                                                                         self.exam_for_letter[1])

        self.letter_text6 = ""
        if self.event_data_in_database[19] == 1:  # infectious disease
            self.letter_text6 = "{} has {}.  ".format(self.pronoun_for_letter, self.event_data_in_database[20])

        self.letter_text7 = ""
        if self.event_data_in_database[21] == 1:
            self.letter_text7 = "{} has a previously documented reaction to X ray contrast medium.  ".format(
                self.pronoun_for_letter)

        self.right_colonic_symptoms = False
        if len(self.history_for_letter) != 0 or (
                "passage of dark blood per rectum" in self.symptom_list_for_letter) or (
                "loose stools" in self.symptom_list_for_letter):
            self.right_colonic_symptoms = True

        self.letter_text8 = ""
        if self.event_data_in_database[
            25] == 1 and self.right_colonic_symptoms:  # for frail patients with possible right colonic symptoms:
            self.letter_text8 = "Although {} {} has some symptoms and history raising the possibility of right colonic disease, I think {} would have difficulty tolerating a colonoscopy.  ".format(
                self.title_for_letter, self.patient_data_in_database[2], self.lower_pronoun)

        if len(self.investigation_ordered) != 0:
            self.letter_text9 = "I have arranged "  # document investigations ordered
            if len(self.investigation_ordered) == 1:
                self.letter_text9 += "a " + self.investigation_ordered[0][0]

            else:
                for item in range(0, (len(self.investigation_ordered) - 1)):
                    self.letter_text9 += "a " + self.investigation_ordered[item][0]
                    self.letter_text9 += ","
                self.letter_text9 += "and a "
                self.letter_text9 += self.investigation_ordered[(len(self.investigation_ordered) - 1)][0]
        self.letter_text9 += " on an urgent basis and will be in touch once the results are available"
        self.letter_text10 = "Yours sincerely,\n\n\n\n{} {}\n{}".format(self.user_data[0], self.user_data[1],
                                                                        self.user_data[2])
        self.letter_text = self.letter_text1 + self.new_paragraph + self.letter_text2 + self.letter_text3 + self.letter_text4 + self.letter_text6 + self.letter_text7 + self.new_paragraph + self.letter_text5 + self.new_paragraph + self.letter_text8 + self.letter_text9 + self.new_paragraph + self.letter_text10
        self.draft_letter = Text(self, wrap=WORD)
        self.draft_letter.grid(row=10, column=0, sticky=W, rowspan=20, columnspan=5, )
        self.draft_letter.insert(INSERT, self.letter_text)

        self.draft_letter_instructions = Label(self, text="Make any changes needed then press Accept")
        self.draft_letter_instructions.grid(row=31, column=0, sticky=W)
        self.accept_letter = Button(self, text="Accept", command=self.save_letter)
        self.accept_letter.grid(row=32, column=0, sticky=W)

    def save_letter(self):
        self.edited_letter = self.draft_letter.get("1.0", "end")
        self.conn = sqlite3.connect("colotwr.db")
        self.curr = self.conn.cursor()
        try:
            self.curr.execute('INSERT INTO clinic_letters (event_no,letter) VALUES (?,?)',
                              (self.event_number, self.edited_letter,))
        except:
            self.curr.execute('UPDATE clinic_letters SET letter=? WHERE event_no =?',
                              (self.edited_letter, self.event_number,))
        self.save_clinic_letter_confirm = Label(self, text="Letter Saved")
        self.save_clinic_letter_confirm.grid(row=50, column=0, sticky=W)
        self.conn.commit()
        self.conn.close()



class Memorybutton(Button):
    """Generates button widget with variable to indicate which event button relates to -inherits from TKINTER Button class"""
    def __init__(self, master, text, event_no):
        super(Memorybutton, self, ).__init__(master)
        self.config(text=text)
        self.event_no_store = int()
        self.event_no_store = event_no

    def return_button_no(self):
        return self.event_no_store


class MdtCoordinate(Frame):
    """Generates form for mdt co-ordinator to show new patients with investigations showing potential cancers which can be sellected and added to list of patints for mdt discussion or show patients already waiting for discussion"""
    def __init__(self, master,):
        super(MdtCoordinate, self).__init__(master)
        self.grid()
        self.table_exists=False
        self.note_exists=False
        self.ptl_form=False
        self.lookup=[]
        self.create_widgets()

    def create_widgets(self):
        """Root function for generating form items"""

        self.abnormal_ix_button = Button(self, text="View Potential Cancer Patients", command=self.abnormal_ix)
        self.abnormal_ix_button.grid(row=0, column=0, sticky=W)
        self.patients_for_mdt_button = Button(self, text="View Patients Awaiting MDT discussion",
                                       command=self.patients_for_mdt)
        self.patients_for_mdt_button.grid(row=0, column=4, sticky=W)

    def abnormal_ix(self):

        if self.table_exists:
            self.mdt_table.destroy()
        self.table_exists=True
        self.mdt_common_headers()
        self.header7 = Label(self.mdt_table, text="View Letter")
        self.header7.grid(row=1, column=6, sticky=W)
        self.header8 = Label(self.mdt_table, text="Add MDT")
        self.header8.grid(row=1, column=7, sticky=W)
        self.header9 = Label(self.mdt_table, text="Stop Track")
        self.header9.grid(row=1, column=8, sticky=W)

        if not self.ptl_form:
            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            SELECT event_no From investigation_outcomes natural join ptl WHERE  ptl_status=1 AND mdt_status=0 AND lgi_endoscopy_outcome BETWEEN 7 AND 8 OR ptl_status=1 AND mdt_status=0 AND ct_outcome BETWEEN 2 AND 4 
            """)
            self.possible_cancer_events = self.cur.fetchall()
            self.lookup = []
            for number in range(0, len(self.possible_cancer_events)):
                self.lookup.append(self.possible_cancer_events[number][0])
            self.conn.close()
        else:
            self.lookup=self.ptl_lookup
        self.mdt_data = self.read_common_data(self.lookup)
        for patient in range(0, len(self.mdt_data)):
            for data_item in range(0, 6):
                self.entry = Label(self.mdt_table, text=self.mdt_data[patient][data_item], borderwidth=0, width=10)
                self.entry.grid(row=patient + 3, column=data_item, sticky=NSEW, padx=1, pady=1)
        self.make_button_names(self.lookup)

    def read_common_data(self, patients_to_lookup):
        """Accepts the list of event numbers for patients to appear on table, reads database data for all of these and returns all of these as an array"""
        self.mdt_form_data_array = []
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        for event in patients_to_lookup:

            self.cur.execute("""
            SELECT hosp_no,forename,surname,dob from patient NATURAL JOIN event WHERE event_no=?
            """, (event,))
            self.mdt_patient = self.cur.fetchone()
            self.cur.execute("""
            SELECT COUNT(event_no) from investigation_outcomes WHERE event_no =?""",(event,))#prevents error if no outcomes recorded yet
            self.has_an_ix = self.cur.fetchone()
            if self.has_an_ix[0] > 0:
                self.cur.execute("""
                SELECT lgi_endoscopy_outcome, ct_outcome FROM investigation_outcomes WHERE event_no=?
                """, (event,))
                self.mdt_ix_outcomes = self.cur.fetchone()
            else:
                self.mdt_ix_outcomes = (0,0)
            self_data_for_mdt_table = []
            for read_data in range(0, 4):
                self_data_for_mdt_table.append(self.mdt_patient[read_data])
            for read_data in range(0, 2):
                self_data_for_mdt_table.append(self.mdt_ix_outcomes[read_data])

            self.mdt_form_data_array.append(self_data_for_mdt_table)
        self.conn.close
        return self.mdt_form_data_array

    def make_button_names(self, lookup, called_from_abnormal_results=True):
        self.accept_buttons=[]
        self.reject_buttons=[]
        self.accept_button_variables={}
        self.reject_button_variables={}

        for make_button_no in range(0, len(lookup)):
            self.mdt_letters = Memorybutton(self.mdt_table, text="Letter", event_no=make_button_no)
            self.mdt_letters.config(
                command=lambda x=self.mdt_letters.return_button_no(): self.letters_for_mdt(x))
            self.mdt_letters.grid(row=make_button_no + 3, column=6, padx=1,pady=1, sticky=NSEW)
            if called_from_abnormal_results:
                self.accept_button_variables[make_button_no] = BooleanVar()
                self.mdt_accept=Checkbutton(self.mdt_table, variable=self.accept_button_variables[make_button_no])
                self.mdt_accept.grid(row=make_button_no + 3, column=7,padx=1,pady=1, sticky=NSEW)
                self.accept_buttons.append(self.mdt_accept)
                self.reject_button_variables[make_button_no] = BooleanVar()
                self.mdt_reject = Checkbutton(self.mdt_table, variable=self.reject_button_variables[make_button_no])
                self.mdt_reject.grid(row=make_button_no + 3, column=8,padx=1,pady=1, sticky=NSEW)
                self.reject_buttons.append(self.mdt_reject)
            else:
                self.mdt_note_button = Memorybutton(self.mdt_table, text="MDT Note", event_no=make_button_no)
                self.mdt_note_button.config(
                command=lambda y=self.mdt_note_button.return_button_no(): self.note_for_mdt(y))#unresolved bug- note object can only be called once
                self.mdt_note_button.grid(row=make_button_no + 3, column=7, padx=1,pady=1, sticky=NSEW)

        if called_from_abnormal_results:
            self.read_mdt_accept_reject_buttons=Button(self.mdt_table, text="Accept Selections",command=self.read_mdt_form)
            self.read_mdt_accept_reject_buttons.grid(row=len(lookup)+4,column=7,columnspan=2,sticky=W)

    def letters_for_mdt(self,button_no):
        """displays letters on mdt co-ordinator form"""

        self.root10 = Toplevel(self.master)
        self.root10.title("Letters")
        self.letter_for_mdt = PopupLetter(self.root10)
        self.letter_for_mdt.setvariables(self.lookup,button_no)

    def note_for_mdt(self,note_button_no):
        if self.note_exists:
            self.note_for_mdt_popup.destroy()
        self.note_exists=True
        self.root11 = Toplevel(self.master)
        self.root11.title("Note")
        self.note_for_mdt_popup = PopupNote(self.root11)
        self.note_for_mdt_popup.note_setvariables(self.lookup,note_button_no)
        #self.make_button_names(self.lookup,called_from_abnormal_results=False)

    def patients_for_mdt(self):
        if self.table_exists:
            self.mdt_table.destroy()
        self.table_exists = True
        self.mdt_common_headers()
        self.header7 = Label(self.mdt_table, text="View Letter")
        self.header7.grid(row=1, column=6, sticky=NSEW)
        self.header8 = Label(self.mdt_table, text="MDT Note")
        self.header8.grid(row=1, column=7, sticky=NSEW)
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        SELECT event_no From ptl WHERE mdt_status=1
        """)
        self.mdt_patients = self.cur.fetchall()
        self.lookup = []
        for number in range(0, len(self.mdt_patients)):
            self.lookup.append(self.mdt_patients[number][0])
        self.mdt_data = self.read_common_data(self.lookup)



        for patient in range(0, len(self.mdt_data)):
            for data_item in range(0, 6):
                self.entry = Label(self.mdt_table, text=self.mdt_data[patient][data_item], borderwidth=0, width=10)
                self.entry.grid(row=patient + 3, column=data_item, sticky=NSEW, padx=1, pady=1)
        self.make_button_names(self.lookup,called_from_abnormal_results=False)

    def read_mdt_form(self):

        self.list_of_patients_for_mdt=[]
        self.list_of_patients_to_reject=[]
        for selection in range(0,len(self.lookup)):
            if self.accept_button_variables[selection].get():
                self.patient_chosen_for_mdt = self.lookup[selection]
                self.list_of_patients_for_mdt.append(self.patient_chosen_for_mdt)
            if self.reject_button_variables[selection].get():
                self.patient_reject = self.lookup[selection]
                self.list_of_patients_to_reject.append(self.patient_reject)
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        for patient in self.list_of_patients_for_mdt:
            self.cur.execute("""
            UPDATE ptl SET mdt_status=1 WHERE event_no=?
            """, (patient,))
        for patient in self.list_of_patients_to_reject:
            self.cur.execute("""
            UPDATE ptl SET ptl_status=0 WHERE event_no=?
            """, (patient,))

        self.conn.commit()
        self.conn.close()
        self.abnormal_ix()

    def mdt_common_headers(self):
        self.mdt_table = Frame(self, background="black")
        self.mdt_table.grid(row=1, column=0, sticky=NSEW)
        self.header1 = Label(self.mdt_table, text="Hosp No")
        self.header1.grid(row=1, column=0, sticky=NSEW)
        self.header2 = Label(self.mdt_table, text="Forename")
        self.header2.grid(row=1, column=1, sticky=NSEW)
        self.header3 = Label(self.mdt_table, text="Surname")
        self.header3.grid(row=1, column=2, sticky=NSEW)
        self.header4 = Label(self.mdt_table, text="D.O.B")
        self.header4.grid(row=1, column=3, sticky=NSEW)
        self.header5 = Label(self.mdt_table, text="Endoscopy")
        self.header5.grid(row=1, column=4, sticky=NSEW)
        self.header6 = Label(self.mdt_table, text="CT")
        self.header6.grid(row=1, column=5, sticky=NSEW)
        return

class PopupLetter(Frame):
    "shows available cinic and endoscpy letters"
    def __init__(self, master):
        super(PopupLetter, self).__init__(master)
        self.lookup_list = []
        self.button_no = 0
        self.look_up_no = 0
        self.grid()

    def setvariables(self,lookup,button):
        self.lookup_list = lookup
        self.button_no=button
        self.look_up_no=self.lookup_list[self.button_no]
        self.show_letter()

    def show_letter(self):
        #self.lookup_up_no=self.lookup_list[self.button_no]
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""
            SELECT Count(*) from clinic_letters WHERE event_no = ?
        """, (self.look_up_no,))
            self.letter_exists = self.cur.fetchone()
            if self.letter_exists[0] > 0:
                self.cur.execute('''SELECT letter FROM clinic_letters WHERE event_no=?''',
                                 (self.look_up_no,))
                self.clinic_letter_text = self.cur.fetchall()

            else:
                self.clinic_letter_text = "There is no clinic letter on file for this patient"
            self.cur.execute("""
            SELECT Count(endoscopy_letter) from investigation_outcomes WHERE event_no = ?
            """, (self.look_up_no,))
            self.letter_exists = self.cur.fetchone()
            if self.letter_exists[0] > 0:
                self.cur.execute('''SELECT endoscopy_letter FROM investigation_outcomes WHERE event_no=?''',
                                 (self.look_up_no,))
                self.endoscopy_letter_text = self.cur.fetchall()


            else:
                self.endoscopy_letter_text = "There is currently no endoscopy letter on file for this patient"
            self.cur.execute("""
            SELECT Count(ct_letter) from investigation_outcomes WHERE event_no = ?
        """, (self.look_up_no,))
            self.letter_exists = self.cur.fetchone()
            if self.letter_exists[0] > 0:
                self.cur.execute('''SELECT ct_letter FROM investigation_outcomes WHERE event_no=?''',
                                 (self.look_up_no,))
                self.ct_letter_text = self.cur.fetchall()
            else:
                self.ct_letter_text = "There is currently no CT letter on file for this patient"

            self.conn.close()
        except TypeError:
            self.clinic_letter_text = "There is a problem accessing clinic letters"
            self.endoscopy_letter_text=""
            self.ct_letter_text=""
            self.conn.close()
        self.popup_text=str(self.clinic_letter_text[0][0]) + "\n" + str(self.endoscopy_letter_text[0][0])+ "\n" + str(self.ct_letter_text[0][0])
        self.clinic_letter = Text(self, wrap=WORD)
        self.clinic_letter.grid(row=10, column=0, sticky=W, rowspan=20, columnspan=5, )
        self.clinic_letter.insert(INSERT, self.popup_text)

class PopupNote(Frame):
    """generates notepad to add notes for mdt discussion and recover saved notes for viewing and editing"""
    def __init__(self, master):
        super(PopupNote, self).__init__(master)
        self.note_lookup_list = []
        self.note_button_no = 0
        self.note_look_up_no = 0
        self.grid()

    def note_setvariables(self,lookup,button):
        self.note_lookup_list = lookup
        self.note_button_no = button
        self.note_look_up_no = self.note_lookup_list[self.note_button_no]
        self.show_note()

    def show_note(self):
        #self.lookup_up_no=self.lookup_list[self.button_no]
        self.mdt_note = Text(self, wrap=WORD)
        self.mdt_note.grid(row=0, column=0, sticky=W, rowspan=20, columnspan=5, )

        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        try:
            self.cur.execute("""
            SELECT Count(comment_for_mdt) from ptl WHERE event_no = ?
        """, (self.note_look_up_no,))
            self.note_exists = self.cur.fetchone()
            if self.note_exists[0] > 0:
                self.cur.execute('''SELECT comment_for_mdt FROM ptl WHERE event_no=?''',
                                 (self.note_look_up_no,))
                self.mdt_note_text = self.cur.fetchall()
                note=self.mdt_note_text[0][0]
                self.mdt_note.insert(INSERT, note)
        except TypeError:
            self.mdt_note_db_error_text = "There is a problem accessing clinic letters"
        finally:
            self.cur.close()
        self.save_note_close_button=Button(self,text="Save Note and Close",command=self.save_note_close)
        self.save_note_close_button.grid(row=21,column=0,sticky=W)

    def save_note_close(self):
        self.edited_note = self.mdt_note.get("1.0", "end")

        try:
            self.conn = sqlite3.connect("colotwr.db")
            self.cur = self.conn.cursor()
            self.cur.execute("""
            UPDATE ptl SET comment_for_mdt=? WHERE event_no =?""",(self.edited_note,self.note_look_up_no,))
            self.conn.commit()
        except TypeError:
            self.mdt_note_db_error_text = "There is a problem accessing clinic letters"
        finally:
            self.conn.close()
        app.mdt_form.patients_for_mdt()
        app.mdt_form.root11.destroy()

class Ptl(MdtCoordinate):
    """Generates patient tracking list (all patients on tracking regardless of investigation status)- inherits from MDT coordinator class but adds new search function"""
    def __init__(self, master):
        super(Ptl, self).__init__(master)
        self.grid()
        self.table_exists=False
        self.note_exists=False
        self.ptl_form=True
        self.lookup_ptl_patients()

    def lookup_ptl_patients(self):
        self.abnormal_ix_button.destroy()#parent class runs function to generate buttons from its __init__-can't stp this so this unneeded buutons
        self.patients_for_mdt_button.destroy()
        self.conn = sqlite3.connect("colotwr.db")
        self.cur = self.conn.cursor()
        self.cur.execute("""
        SELECT event_no From ptl WHERE ptl_status=1
        """)
        self.ptl_patients = self.cur.fetchall()
        self.ptl_lookup = []
        for number in range(0, len(self.ptl_patients)):
            self.ptl_lookup.append(self.ptl_patients[number][0])
        self.abnormal_ix()




# main
root = Tk()
root.title("Colorectal 2WR")
app = MainMenu(root)

root.mainloop()
