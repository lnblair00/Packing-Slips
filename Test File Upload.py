# To run app: streamlit run "C:\\Users\\LaurynBlair\\OneDrive - Mercury Rising Ltd\\Inventory Management\\Test File Upload.py"

import streamlit as st
import requests
import base64
import time
# ----------------------------
# GitHub Setup
# ----------------------------
GITHUB_TOKEN = "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"  # replace with your token
REPO = "lnblair00/Packing-Slips"    # replace with your repo
BRANCH = "main"
API_URL = f"https://api.github.com/repos/{REPO}/contents"

# ----------------------------
# Functions
# ----------------------------
def ensure_po_folder(po_number):
   """
   Ensure a folder exists in GitHub for the given PO number.
   Creates a .keep file if folder is new.
   """
   path = f"packing_slips/{po_number}/.keep"
   url = f"{API_URL}/{path}"
   headers = {"Authorization": f"token {GITHUB_TOKEN}"}
   r = requests.get(url, headers=headers)
   if r.status_code == 200:
       return f"https://github.com/{REPO}/tree/{BRANCH}/packing_slips/{po_number}"
   else:
       # Create .keep file to force folder creation
       content = base64.b64encode(b"").decode("utf-8")
       data = {
           "message": f"Create folder for {po_number}",
           "content": content,
           "branch": BRANCH
       }
       r = requests.put(url, headers=headers, json=data)
       if r.status_code in [200, 201]:
           return f"https://github.com/{REPO}/tree/{BRANCH}/packing_slips/{po_number}"
       else:
           st.error(f"GitHub error: {r.text}")
           return None
# ----------------------------
# Streamlit UI
# ----------------------------
st.title("📁 Create PO Folder in GitHub")
po_number = st.text_input("Enter PO Number (e.g. PO-01234):")
if st.button("Create / Open Folder"):
   if not po_number.strip():
       st.error("Please enter a PO number.")
   else:
       folder_url = ensure_po_folder(po_number.strip())
       if folder_url:
           st.success(f"✅ Folder ready for {po_number.strip()}")
           # Auto-open in a new browser tab
           st.markdown(
               f"<script>window.open('{folder_url}', '_blank');</script>",
               unsafe_allow_html=True
           )
           # Refresh Streamlit page
           st.rerun()
