def compare_invoice_po(invoice_data: dict, po_data: dict) -> dict:
    """
    Compare invoice and PO fields to detect mismatches.
    """
    result = {
        "status": "Matched",
        "mismatches": []
    }

    # Define which fields should be compared
    compare_fields = ["PO Number", "Total Amount", "Date"]

    for field in compare_fields:
        inv_val = invoice_data.get(field)
        po_val = po_data.get(field)

        if inv_val and po_val and inv_val != po_val:
            result["status"] = "Mismatch Found"
            result["mismatches"].append({
                "field": field,
                "invoice_value": inv_val,
                "po_value": po_val,
                "note": f"{field} mismatch: Invoice({inv_val}) ≠ PO({po_val})"
            })
        elif inv_val is None:
            result["mismatches"].append({
                "field": field,
                "invoice_value": "Missing",
                "po_value": po_val or "N/A",
                "note": f"Missing {field} in Invoice"
            })
            result["status"] = "Incomplete Invoice"

    return result
