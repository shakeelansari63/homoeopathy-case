conda create -p ${PWD}/venv python=3.10 && \
source $(dirname $(which activate))/../etc/profile.d/conda.sh && \
conda activate ${PWD}/venv && \
pip install -r requirements.txt