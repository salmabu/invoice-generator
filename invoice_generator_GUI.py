import pandas as pd
from fpdf import FPDF
from datetime import datetime
import PySimpleGUI as sg

def generate_invoice(filename):
    try:
        df = pd.read_csv(filename, encoding='latin1')

        df["Item Total"] = df["Quantity"] * df["Price"]
        invoice_total = df["Item Total"].sum()

        client_name = df["Client Name"].iloc[0]
        invoice_file = f"invoice_{client_name}.pdf"
        invoice_date = datetime.now().strftime("%Y-%m-%d")

        pdf = FPDF()
        pdf.add_page()
        pdf.set_font("Arial", size=12)

        pdf.set_font("Arial", 'B', 16)
        pdf.cell(200, 10, txt="INVOICE", ln=True, align='C')

        pdf.set_font("Arial", size=12)
        pdf.cell(100, 10, txt=f"Client: {client_name}", ln=True)
        pdf.cell(100, 10, txt=f"Date: {invoice_date}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", 'B', 12)
        pdf.cell(60, 10, "Item", border=1)
        pdf.cell(30, 10, "Qty", border=1)
        pdf.cell(30, 10, "Price", border=1)
        pdf.cell(40, 10, "Total", border=1)
        pdf.ln()

        pdf.set_font("Arial", size=12)
        for _, row in df.iterrows():
            pdf.cell(60, 10, str(row["Item"]), border=1)
            pdf.cell(30, 10, str(row["Quantity"]), border=1)
            pdf.cell(30, 10, f"${row['Price']}", border=1)
            pdf.cell(40, 10, f"${row['Item Total']}", border=1)
            pdf.ln()

        pdf.ln(5)
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(120, 10, "Total Invoice:", border=0)
        pdf.cell(40, 10, f"${invoice_total}", border=1)

        pdf.output(invoice_file)
        return f"✅ Invoice saved as {invoice_file}"

    except FileNotFoundError:
        return f"❌ File '{filename}' not found. Please try again."
    except Exception as e:
        return f"❌ Error: {str(e)}"


# GUI layout
layout = [
    [sg.Text("Select the CSV file for invoice generation:")],
    [sg.InputText(key="-FILE-"), sg.FileBrowse(file_types=(("CSV Files", "*.csv"),))],
    [sg.Button("Generate Invoice"), sg.Button("Exit")],
    [sg.Multiline(size=(60,10), key="-OUTPUT-", disabled=True)]
]

window = sg.Window("Invoice Generator", layout)

while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Exit":
        break
    if event == "Generate Invoice":
        filename = values["-FILE-"]
        result = generate_invoice(filename)
        window["-OUTPUT-"].update(result)

window.close()
