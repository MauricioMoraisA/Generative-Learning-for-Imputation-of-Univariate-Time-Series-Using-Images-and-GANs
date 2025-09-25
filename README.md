# Generative-Learning-for-Imputation-of-Univariate-Time-Series-Using-Images-and-GANs  

This repository contains the files and codes necessary for the functions and templates used.  

## 📂 Dataset Generation
👉 Note: **step 0** is only necessary if you want to start from scratch, from the acquisition of the dataset.
If you prefer, the **dataset is already ready** along with the **pre-trained models** at the following link:  

🔗 [Dataset and Pre-trained Models (Google Drive)](https://drive.google.com/drive/folders/1TxXLhLJ9l-PaWw_u-7lOiWHprSVV3HQY?usp=sharing)  

### Steps:  
0. (Optional) Use **pretreatment.ipynb** to adjust the dataset.  
1. Run **Classtsimagestl.py**.  
2. Run **split_folds.py**.  
3. Delete all subfolders in `input` and `label`, except those corresponding to the folds (already created).  
4. You will now have a dataset with missing value rates ranging from **10% to 40%**.  
5. Correct the dataset paths in each model notebook, if necessary, for both training and testing.  

## 📘 Notebook Structure
- Notebooks with the **model name** → used for **training**.
- Notebooks with the **model name + test** → used for **testing**.   

## 🗂️ Folder Structure after Training  
During training, the following hierarchy will be created:  

```
saved_model/
    └── model/
        └── channels (1 to 3)/
            └── folds (1 to 5)/
```

## 📊 Results Structure after Testing  
Each test notebook generates the folder:  

```
results/
    └── model/
        └── result_<n_channel>_<rate>_<fold>.csv
```

📌 Example of saved file:  
```
result_1_10_1.csv
```

## 🛠️ Processing Results  
There are two specific notebooks for **processing results**:  
- They gather all generated `.csv` files and save them in consolidated files, such as:  
  - `result_full_1c_dc.csv` (for DCGAN),  
  - and so on for the other models.  

## 📈 Figures and Visualizations  
The other figures and analyses can be found directly in the **test notebooks**. 

Translated with DeepL.com (free version)
