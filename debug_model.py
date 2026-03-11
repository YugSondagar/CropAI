import torch
import torch.nn as nn

# Try to load the model and see the actual error
model_path = "models/plant_disease_model.pth"

# First, let's check what's in the file
print("Loading state dict...")
try:
    state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=False)
    print("State dict keys:", list(state_dict.keys())[:10])
except Exception as e:
    print(f"Error: {e}")
    
    # Try loading with weights_only=True
    try:
        print("Trying with weights_only=True...")
        state_dict = torch.load(model_path, map_location=torch.device('cpu'), weights_only=True)
        print("Keys:", list(state_dict.keys())[:10])
    except Exception as e2:
        print(f"Error with weights_only=True: {e2}")
