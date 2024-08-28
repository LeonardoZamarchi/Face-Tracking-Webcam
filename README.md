# Rastreamento de Rosto com OpenCV

## Visão Geral

Este projeto implementa um sistema de rastreamento de rostos usando OpenCV em Python. O script captura vídeo da webcam, detecta rostos usando cascatas Haar, e em seguida rastreia o rosto detectado usando o tracker CSRT. O rosto rastreado é exibido em um quadro de vídeo recortado e redimensionado, mantendo a proporção original para evitar distorções. A saída pode ser usada como entrada para webcams virtuais para integração com plataformas de videoconferência como Google Meet.

## Funcionalidades

- **Detecção de Rosto:** Usa cascatas Haar para detectar rostos em tempo real.
- **Rastreamento de Rosto:** Após detectar um rosto, o sistema rastreia o rosto usando o tracker CSRT, garantindo que o rosto permaneça centralizado mesmo quando se move.
- **Preservação da Proporção:** Mantém a proporção original durante o recorte e redimensionamento para evitar distorções.
- **Suporte a Webcam Virtual:** O vídeo processado pode ser transmitido para uma webcam virtual para uso em software de videoconferência.

## Requisitos

- Python 3.12
- OpenCV (com módulos contrib)

## Instalação

1. **Clone o repositório:**
    ```bash
    git clone https://github.com/LeonardoZamarchi/Face-Tracking-Webcam.git
    cd Face-Tracking-Webcam
    ```

2. **Instale os pacotes Python necessários:**
    ```bash
    pip install opencv-python opencv-contrib-python numpy
    ```

3. **(Opcional) Instale o v4l2loopback para suporte a webcam virtual no Linux:**
    ```bash
    sudo apt-get install v4l2loopback-dkms
    sudo modprobe v4l2loopback devices=1 video_nr=10 card_label="VirtualCam" exclusive_caps=1
    ```

## Uso

1. **Execute o script:**
    ```bash
    python rastreamento_rosto.py
    ```

2. **Para usar a saída como uma webcam virtual:**
   - Certifique-se de que você tem o v4l2loopback (Linux) ou uma configuração de câmera virtual (Windows/macOS).
   - Modifique o script para enviar a saída para a webcam virtual (instruções fornecidas no script).

3. **Pressione 'q' para sair da aplicação.**

## Configuração

- **Método de Rastreamento:** O script usa CSRT por padrão, mas outros trackers como KCF podem ser usados para melhor performance, com algum custo na precisão.
- **Fator de Recorte:** Ajuste o `crop_factor` no script para controlar a quantidade de área ao redor do rosto que será exibida. Valores mais altos mostram mais da área ao redor.
- **Dimensões do Quadro:** O script ajusta automaticamente as dimensões da saída para manter a proporção original.

## Exemplo

O comando a seguir executa o script com as configurações padrão:
```bash
python rastreamento_rosto.py
