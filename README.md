# PsychometricLLaMA for controlled generation of psychometric test items

This Repository contains a supporting Google Colab notebook for a LLaMA 2 13B adapter trained in the scope of my master's thesis published in the Springer BestMasters series.
It primary purpose is the controlled generation of psychological test items based on the inputs: construct-name, definition, sub-construct, definition, difficulty*, inversion.

* Has shown to not affect the actual item-difficulty.

# How to use this repository
1. Try out the model using the gradio app notebook. For that to work you need to accept the conditions at: https://huggingface.co/bgilles/PsychometricLLaMA ; https://huggingface.co/meta-llama/Llama-2-13b-hf ; and input a hugging face account token into the area marked with "SECRET"

2. Have a look at the studies methodology. Most files that were used in creating the study are published here. There are some limitations and it is a bit chaotic. For once, many scripts will not fully run, because I was not allowed to upload the complete dataset I used for training. My curated item-set from studies and the open sourced IPIP items are included. Also I did not get around to translate all German comments to English. I also could not upload all adapter files, since GitHub only allows files smaller than 100 MB.

*If you want to reproduce parts of the process, have questions or want access to some other adapter files, please reach out to me on GitHub or LinkedIn https://www.linkedin.com/in/bj%C3%B6rn-gilles/ . I am happy to explain in detail or provide data.*

