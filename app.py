import streamlit as st
import requests

st.set_page_config(page_title="Invoice-PO Reconciliation Agent", layout="centered")
st.title("🧾 Purchase Invoice Reconciliation Agent")

BACKEND_URL = "http://127.0.0.1:8000/reconcile"

st.write("Upload a **Purchase Invoice** and its corresponding **Purchase Order (PO)** to check for mismatches.")

invoice_file = st.file_uploader("Upload Invoice (PDF)", type=["pdf"])
po_file = st.file_uploader("Upload Purchase Order (PDF)", type=["pdf"])

if st.button("🔍 Reconcile"):
    if not invoice_file or not po_file:
        st.warning("Please upload both files.")
    else:
        files = {
            "invoice": (invoice_file.name, invoice_file, "application/pdf"),
            "po": (po_file.name, po_file, "application/pdf"),
        }

        with st.spinner("Processing..."):
            response = requests.post(BACKEND_URL, files=files)
            if response.status_code == 200:
                result = response.json()
                st.subheader("✅ Reconciliation Result")
                st.json(result)

                if result.get("mismatches"):
                    st.error("❌ Mismatches found:")
                    for m in result["mismatches"]:
                        st.write(f"**{m['field']}** → Invoice: `{m['invoice_value']}` | PO: `{m['po_value']}`")

                    if "ai_summary" in result:
                        st.info(f"💡 AI Summary: {result['ai_summary']}")
                else:
                    st.success("✅ All fields matched successfully.")
            else:
                st.error(f"Error: {response.text}")
