# 🕳️ **What Can Potholes Tell Us About Chicago?**

## 📝 **Project Description**

This project explores how Chicago’s pothole data reflects social and demographic inequalities, using interactive visualizations to uncover patterns in infrastructure and community vulnerability.

<p align="center">
  <img src="https://github.com/user-attachments/assets/92f22f71-6771-4f32-a8e7-7b96fbbaa82e" alt="Visualization Image">
</p>

<br>

---

## ✨ **Context**

This dashboard provides insights into how infrastructure issues align with socioeconomic and demographic factors across Chicago neighborhoods.

<br>

---

## 📂 **Dataset**

- **311 Service Requests**: Pothole complaints reported in Chicago.
- **ZIP Code Boundaries**: Geographic data mapping Chicago neighborhoods.
- **Demographics**: Population data by race and age for each ZIP Code.
- **COVID-19 Community Vulnerability Index (CCVI)**: Scores indicating neighborhood vulnerability to health and socioeconomic challenges.

<br>

---

## 🎨 **Visualization**

<p align="center">
  <img src="https://github.com/user-attachments/assets/92f22f71-6771-4f32-a8e7-7b96fbbaa82e" alt="Visualization Image" width="800">
</p>

<br>

---

## 💻 **Technologies and Tools**

- **Altair**: For creating interactive visualizations.  
- **Pandas**: For data preprocessing and manipulation.  
- **GeoJSON**: For geographic data visualization.  
- **Viridis Color Scale**: For accessible, colorblind-friendly palettes.

<br>


---

## 🚀 **How to Use**

### **Option 1: Run with Google Colab (Recommended)**
1. Upload the **chicago_potholes.ipynb** notebook to Google Colab
   
2. Update Altair:
   
   If you’re running the project in Google Colab, update your Altair version to avoid compatibility issues. Run the following line of code in a Colab cell:
   ```bash
   pip install -U altair vega_datasets
   ```

   After running this, go to **Runtime > Restart Runtime** in the Colab menu.

3. Run the Notebook:
   
   Execute all cells in the notebook to generate visualizations and analyze data.

---

### **Option 2: Run with Jupyter Notebook**
1. Clone and open the repository:  
   ```bash
   git clone https://github.com/Minko82/Chicago-Potholes-Visualizations.git
   cd Chicago-Potholes-Visualizations/notebook
   ```

2. Launch the Notebook:

   ```bash
   jupyter notebook chicago_potholes.ipynb
   ```
   
---

### **Option 3: Run with Python Command Line**

1. Clone and open the repository:  
   ```bash
   git clone https://github.com/Minko82/Chicago-Potholes-Visualizations.git
   cd Chicago-Potholes-Visualizations/scripts
   ```

2. Run desired Python scripts from the Command Line:
   ```bash
   python final_version.py
   ```
