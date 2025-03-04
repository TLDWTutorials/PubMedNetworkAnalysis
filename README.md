# 🔎 Author-Based Co-Authorship Network Using PubMed and Python 🚀  

This project **fetches publications from PubMed for specified authors**, builds a **co-authorship network**, and **visualizes it interactively** using Pyvis (in Python). The network highlights **searched authors in red** and **co-authors in blue**.  

## 📌 Features  
✅ Searches **specific authors** in PubMed  
✅ Collects **their co-authors** from all publications  
✅ Builds an **interactive co-authorship network**  
✅ Saves results as an **HTML file for exploration**  

---  

## 🔑 Setup  

### 1️⃣ Add Your Authors  
Modify this list in the script:  
```
searched_authors = [
    "Suraiya Rasheed",
    "Bryan Holland"
]
```
Replace them with your author names.  

### 2️⃣ Run the script  
```
python author_network.py
```
This will:  
- Fetch **all publications** for the authors  
- Identify **co-authorship connections**  
- Generate `author_network.html`  

---  

## 📊 Output Files  
`author_network.html` → **Interactive co-authorship network**  
(Optional) You can extend this to export data as CSV  

---  

## 📈 Visualization  
After running, open:  
```
author_network.html
```
This will display an **interactive co-authorship network**.  
🟥 **Searched Authors** = **Red**  
🟦 **Co-Authors** = **Blue**  

---  

## 🛠 Customization  

### Change the number of articles fetched:  
Modify:  
```
fetch_pubmed_ids_by_author(author, max_results=50)
```
Increase `max_results` for more data.  

### Adjust co-authorship filtering:  
Modify:  
```
if weight > 1:  # Only keep meaningful collaborations
```
Change `1` to a higher number for stronger connections.  

---  

## 📜 License  
This project is **MIT Licensed** – feel free to use and modify.  

---  

💡 **Developed by TLDW_Tutorials**  
