import re

def parse_invoice_text(text: str) -> dict:
    """
    Extract important fields from an invoice using basic regex rules.
    """
    data = {}

    # Normalize text
    text = text.replace('\n', ' ').replace('\r', ' ').strip()

    # Example regex patterns (can refine later)
    invoice_no = re.search(r'(Invoice\s*(No\.?|Number)[:\s]*)([A-Za-z0-9\-]+)', text, re.IGNORECASE)
    po_no = re.search(r'(PO\s*(No\.?|Number)[:\s]*)([A-Za-z0-9\-]+)', text, re.IGNORECASE)
    total_amount = re.search(r'(Total|Amount\s*Due)[:\s]*\$?([\d,]+\.\d{2})', text, re.IGNORECASE)
    date = re.search(r'(Date)[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})', text)

    if invoice_no:
        data["Invoice Number"] = invoice_no.group(3)
    if po_no:
        data["PO Number"] = po_no.group(3)
    if total_amount:
        data["Total Amount"] = total_amount.group(2)
    if date:
        data["Date"] = date.group(2)

    return data


def parse_po_text(text: str) -> dict:
    """
    Extract important fields from a Purchase Order document.
    """
    data = {}

    text = text.replace('\n', ' ').replace('\r', ' ').strip()

    po_no = re.search(r'(PO\s*(No\.?|Number)[:\s]*)([A-Za-z0-9\-]+)', text, re.IGNORECASE)
    vendor = re.search(r'(Vendor|Supplier)[:\s]*([A-Za-z0-9\s&]+)', text, re.IGNORECASE)
    total = re.search(r'(Total|Amount)[:\s]*\$?([\d,]+\.\d{2})', text, re.IGNORECASE)
    date = re.search(r'(Date)[:\s]*([0-9]{2}/[0-9]{2}/[0-9]{4})', text)

    if po_no:
        data["PO Number"] = po_no.group(3)
    if vendor:
        data["Vendor Name"] = vendor.group(2).strip()
    if total:
        data["Total Amount"] = total.group(2)
    if date:
        data["Date"] = date.group(2)

    return data
