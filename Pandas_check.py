import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import networkx as nx

# Funzione per caricare e analizzare i dataset
def analyze_dataset(file_path, name):
    df = pd.read_csv(file_path, skipinitialspace=True)
    print(f"\n{name} Info:")
    print(df.info())
    print(f"\nValori nulli in {name}:\n", df.isnull().sum())
    print(f"\nPercentuale di valori nulli in {name}:\n", df.isnull().mean() * 100)
    print(f"\nColonne in {name}:\n", df.columns)
    print(f"\nDati duplicati in {name}: {df.duplicated().sum()}")
    return df

# Funzione per individuare chiavi primarie
def identify_primary_keys(df, name):
    unique_counts = df.nunique()
    potential_keys = unique_counts[unique_counts == len(df)].index.tolist()
    print(f"\nPotenziali chiavi primarie in {name}:", potential_keys)
    for col in potential_keys:
        if df[col].duplicated().any():
            print(f"La colonna {col} in {name} non può essere una chiave primaria a causa di duplicati.")

# Funzione per visualizzare distribuzioni numeriche
def visualize_numerical_distributions(df, name):
    numerical_cols = df.select_dtypes(include=['float64', 'int64']).columns
    for col in numerical_cols:
        plt.figure(figsize=(10, 4))
        sns.boxplot(x=df[col])
        plt.title(f'{name} - Distribuzione di {col}')
        plt.show()

# Funzione per analisi dei dati mancanti
def visualize_missing_data(df, name):
    missing_counts = df.isnull().sum()
    missing_percentage = (missing_counts / len(df)) * 100
    print(f"\nDati mancanti in {name}:\n", pd.DataFrame({'Missing Values': missing_counts, 'Percentage': missing_percentage}))
    plt.figure(figsize=(10, 6))
    sns.heatmap(df.isnull(), cbar=False, cmap='viridis')
    plt.title(f"{name} - Heatmap dei dati mancanti")
    plt.show()

# Funzione per analisi delle cardinalità
def cardinality_analysis(df1, df2, key):
    df1_unique = df1[key].nunique()
    df2_unique = df2[key].nunique()
    if df1_unique == len(df1) and df2_unique == len(df2):
        return "Uno a Uno (1:1)"
    elif df1_unique == len(df1):
        return "Uno a Molti (1:N)"
    elif df2_unique == len(df2):
        return "Molti a Uno (N:1)"
    else:
        return "Molti a Molti (M:N)"

# Caricamento e analisi dei dataset
Vehicles = analyze_dataset("D:/1_LDS/Vehicles.csv", "Vehicles")
Crashes = analyze_dataset("D:/1_LDS/Crashes.csv", "Crashes")
People = analyze_dataset("D:/1_LDS/People.csv", "People")

# Identificazione chiavi primarie
identify_primary_keys(Vehicles, "Vehicles")
identify_primary_keys(Crashes, "Crashes")
identify_primary_keys(People, "People")

# Visualizzazioni
visualize_numerical_distributions(Vehicles, "Vehicles")
visualize_missing_data(Vehicles, "Vehicles")

# Analisi delle cardinalità
print("Cardinalità tra Vehicles e Crashes per RD_NO:", cardinality_analysis(Vehicles, Crashes, 'RD_NO'))
print("Cardinalità tra Crashes e People per RD_NO:", cardinality_analysis(Crashes, People, 'RD_NO'))

# Creazione del grafo delle relazioni
G = nx.DiGraph()
G.add_edges_from([
    ('Vehicles', 'Crashes', {'label': 'RD_NO, VEHICLE_ID'}),
    ('Crashes', 'People', {'label': 'RD_NO'}),
])
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10)
edge_labels = nx.get_edge_attributes(G, 'label')
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)
plt.title('Relazioni tra i Dataset')
plt.show()
