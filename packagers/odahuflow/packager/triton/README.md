Required files:
- model file/directory with fixed naming:
    - TensorRT: model.plan
    - TensorFlow SavedModel: model.savedmodel/...
    - TensorFlow Grafdef: model.graphdef 
    - ONNX: model.onnx file or directory
    - TorchScript: model.pt
    - Caffe 2 Netdef: model.netdef + init_model.netdef

- config.pbtxt except for:
    - TensorRT
    - TF SavedModel
    - ONNX
    

## Triton Pipeline

1. Project structure in VCS:
    - `MLproject`
    - `train_conda.yaml`
    - `train.py`
    - `data/` (directory with any addtitional files to inject into training artifact)
        - `model.py`
        - `conda.yaml`
        - `config.pbtxt`
1. MLproject trainer 
    - executes main entrypoint of MLproject. All files that need to be packed into 
    training artifact must be saved in `/output`. For Triton scenario model file name must
    match Triton's expectations.
    - creates simple manifest in `/output` (e.g. `odahuflow.model.yaml`) that stores model name and version
    - copies all files from `data` directory to `/output` directory
    - move all the content of `/output` into directory provided as `--target` parameter to Tekton step 
1. Triton packager
    - expects input directory (download and unzipped by setup step) to contain:
        - model file(s) (e.g. `model.pt` for TorchScript backend)
        - `odahuflow.model.yaml` (can be optional to simplify packing pre-trained model;
        use name `model` and version `1` if omitted)
        - `config.pbtxt` (Triton config; optional for some backends)
        - `conda.yaml` (for Python backend only)
    - Build file hierarchy expected by Triton:
        - `{model_name}/`
            - `{model_version}/`
                - model file(s)...
            - `config.pbtxt`
    - Render Dockerfile basing on detected model backend:
        - for Python backend (`model.py` found) install miniconda and model's dependencies
    - Build Docker image and write it to `result.json` to push it on result-step

