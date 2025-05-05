import pickle
try:
    similarity = pickle.load(open('similarity.pkl', 'rb'))
    print("Successfully loaded similarity.pkl")
    print("Type:", type(similarity))
    print("Shape:", similarity.shape if hasattr(similarity, 'shape') else "No shape attribute")
except Exception as e:
    print("Error:", e)