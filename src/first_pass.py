import pandas as pd


if __name__ == "__main__":
    c_elegans_df = pd.read_csv("../data/C_elegans_CRISPR_sgRNA_Database_Responses.csv")
    
    c_elegans_df.columns = ["Timestamp", "sgRNA", "GeneTarget", "GuideSoftware", "Success", "WormsInjected",
        "SuccessfulInjections", "InjectorExperienceLevel", "DNA", "Promoter", "Cas9Form", "ScreeningMethod", 
        "RepairMechanism", "Comments"]
    c_elegans_df["WormsInjected"] = c_elegans_df["WormsInjected"].str.extract(r"^(\d+)").astype(int)
        
    c_elegans_df["SuccessRate"] = c_elegans_df["SuccessfulInjections"] / c_elegans_df["WormsInjected"]
    c_elegans_df["SuccessRate"] = c_elegans_df["SuccessRate"].fillna(0)
    
    c_elegans_df["sgRNAlength"] = c_elegans_df["sgRNA"].apply(len)
    c_elegans_df["sgRNA"] = c_elegans_df["sgRNA"].str.split(", ").apply(lambda x: x[0]).str.upper()
    
    c_elegans_df["GuideSoftware"] = ['Yes' if cell not in ("Yes", "No") else cell 
        for cell in c_elegans_df["GuideSoftware"]]
