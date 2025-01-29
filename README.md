# PsychometricLLaMA: Controlled Generation of Psychometric Test Items

This repository contains a supporting Google Colab notebook for a LLaMA 2 13B adapter, trained as part of my master's thesis published in the Springer BestMasters series.
The model specializes in generating psychological test items with controlled parameters including:
- Construct name and definition
- Sub-construct and definition
- Difficulty level*
- Inversion status

\* Note: My master's thesis indicates this parameter does not significantly influence actual item difficulty.

## Getting Started

### 1. Try the Model
To use the interactive Gradio app:
1. Accept the model terms at:
    - https://huggingface.co/bgilles/PsychometricLLaMA
    - https://huggingface.co/meta-llama/Llama-2-13b-hf
2. Get your Hugging Face account token
3. Insert your token in the notebook's "SECRET" section

### 2. Explore the Methodology
The repository includes most files used in the study, with some limitations:
- Training dataset is partially available (complete dataset couldn't be shared)
- Curated item-set from studies and IPIP items are included
- Some German comments remain untranslated
- Large adapter files (>100MB) are not on GitHub

**Need Help?** For questions, data access, or detailed explanations, reach out via:
- GitHub Issues
- LinkedIn: https://www.linkedin.com/in/björn-gilles/

