import pandas as pd


if __name__ == "__main__":
    c_elegans_df = pd.read_csv("../data/C_elegans_CRISPR_sgRNA_Database_Responses_Anon_30mers.csv")
    
    c_elegans_df.columns = ["Timestamp", "Experimenter", "sgRNA", "sgRNA length", "Gene target", "30mer", "30mer length", "GuideSoftware", "Success", "WormsInjected",
        "SuccessfulInjections", "InjectorExperienceLevel", "DNA", "Promoter", "Cas9Form", "ScreeningMethod", 
        "RepairMechanism", "Comments"]
    c_elegans_df["WormsInjected"] = c_elegans_df["WormsInjected"].str.extract(r"^(\d+)", expand=False).astype(int)
        
    c_elegans_df["SuccessRate"] = c_elegans_df["SuccessfulInjections"] / c_elegans_df["WormsInjected"]
    c_elegans_df["SuccessRate"] = c_elegans_df["SuccessRate"].fillna(0)

    c_elegans_df["sgRNA"] = c_elegans_df["sgRNA"].str.split(", ").apply(lambda x: x[0]).str.upper()
    c_elegans_df["30mer"] = c_elegans_df["30mer"].str.upper()
    c_elegans_df["Cas9Form"] = c_elegans_df["Cas9Form"].str.upper()
    c_elegans_df["Experimenter"] = c_elegans_df["Experimenter"].apply(str)
    
    c_elegans_df["GuideSoftware"] = ['Yes' if cell not in ("Yes", "No") else cell 
        for cell in c_elegans_df["GuideSoftware"]]

    c_elegans_df = c_elegans_df.drop(axis=1, labels=["Timestamp", "30mer length", "Comments"])

    c_elegans_df.to_csv("../results/cleaned_c_elegans_30mers.csv", index=False)