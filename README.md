# Segmentação de Agachamento com MediaPipe e OpenCV

Este projeto detecta automaticamente as fases de **subida** e **descida** em vídeos de agachamento, utilizando **MediaPipe**.

Objetivos:
- **Segmentação de repetições** em trechos individuais salvos em `.mp4`
- **Exportação de dados em CSV** contendo:
  - Distância entre quadril e joelho  
  - Fase do movimento (**Subida** ou **Descida**)  
  - Número da repetição e série  

---

```bash
git clone https://github.com/seu-usuario/agachamento-segmentacao.git
cd agachamento-segmentacao

# Crie e ative o ambiente virtual
python -m venv venv
source venv/bin/activate   # Linux / Mac
venv\Scripts\activate      # Windows

# Instale as dependências
pip install -r requirements.txt
