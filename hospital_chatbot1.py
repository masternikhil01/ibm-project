import tkinter as tk
from tkinter import ttk
import pandas as pd

# Load the dataset
df = pd.read_csv('hospital_data.csv')

class PatientChatbotApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Patient Info Chatbot")
        
        # Set up the main frame
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Setup chat history text area
        self.chat_history = tk.Text(self.main_frame, height=15, width=50, wrap=tk.WORD, state=tk.DISABLED)
        self.chat_history.grid(row=0, column=0, columnspan=2, pady=5)
        
        # Setup entry field for user input
        self.entry_field = ttk.Entry(self.main_frame, width=40)
        self.entry_field.grid(row=1, column=0, pady=5, padx=5)
        
        # Setup send button
        self.send_button = ttk.Button(self.main_frame, text="Send", command=self.send_message)
        self.send_button.grid(row=1, column=1, pady=5)
        
    def send_message(self):
        user_message = self.entry_field.get()
        if user_message:
            self.append_to_chat("You: " + user_message)
            response = self.get_chatbot_response(user_message)
            self.append_to_chat("Bot: " + response)
            self.entry_field.delete(0, tk.END)
            
    def append_to_chat(self, message):
        self.chat_history.config(state=tk.NORMAL)
        self.chat_history.insert(tk.END, message + "\n")
        self.chat_history.config(state=tk.DISABLED)
        self.chat_history.yview(tk.END)
        
    def get_chatbot_response(self, message):
        # Convert message to lowercase for consistent processing
        message = message.lower()
        
        # Look for the keyword "patient" in the message
        if "patient" in message and "name" in message:
            try:
                # Extract patient name from the message
                patient_name = message.replace("tell me about patient name", "").strip()
                
                if patient_name:
                    patient_info = self.get_patient_info_by_name(patient_name)
                    if patient_info:
                        return (f"Patient Name: {patient_info['Name']}\n"
                                f"Room Number: {patient_info['RoomNumber']}\n"
                                f"Disease: {patient_info['Disease']}\n"
                                f"Admission Date: {patient_info['AdmissionDate']}\n"
                                f"Discharge Date: {patient_info['DischargeDate']}")
                    else:
                        return "Patient not found."
                else:
                    return "Patient name not specified in the message."
            except Exception as e:
                return f"An error occurred: {str(e)}"
        else:
            return "Sorry, I didn't understand that. Please include 'patient name' in your query."
    
    def get_patient_info_by_name(self, patient_name):
        # Search for patient by name
        patient = df[df['Name'].str.lower() == patient_name.lower()]
        if not patient.empty:
            patient = patient.iloc[0]
            return {
                "Name": patient['Name'],
                "RoomNumber": patient['RoomNumber'],
                "Disease": patient['Disease'],
                "AdmissionDate": patient['AdmissionDate'],
                "DischargeDate": patient['DischargeDate']
            }
        else:
            return None

# Create the main window
root = tk.Tk()
app = PatientChatbotApp(root)
root.mainloop()
