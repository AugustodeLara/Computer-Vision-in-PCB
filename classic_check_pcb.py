import cv2
import matplotlib.pyplot as plt
import os

# Ler a imagem do PCB de referência
imagem_referencia = cv2.imread('SUA_IMAGEM_DE_REFERÊNCIA_AQUI')

# Exibir a imagem original do PCB de referência
plt.figure(figsize=(10,6))
plt.imshow(imagem_referencia, cmap="gray")

# Ler a imagem do PCB de referência em escala de cinza
imagem_referencia_cinza = cv2.imread('SUA_IMAGEM_DE_REFERÊNCIA_AQUI', 0)

# Exibir a imagem do PCB de referência em escala de cinza
plt.figure(figsize=(10,6))
plt.imshow(imagem_referencia_cinza, cmap="gray")

# Redimensionar a imagem do PCB de referência
imagem_referencia_redimensionada = cv2.resize(imagem_referencia_cinza, (750, 450))

# Exibir a imagem do PCB de referência redimensionada em escala de cinza
plt.figure(figsize=(10,6))
plt.imshow(imagem_referencia_redimensionada, cmap="gray")

# Aplicar desfoque Gaussiano na imagem antes da binarização
imagem_referencia_desfocada = cv2.GaussianBlur(imagem_referencia_redimensionada, (3,3), 0)

# Exibir a imagem desfocada
plt.figure(figsize=(10,6))
plt.imshow(imagem_referencia_desfocada, cmap="gray")

# Binarização adaptativa (média)
limiar_adaptativo_referencia = cv2.adaptiveThreshold(imagem_referencia_desfocada, 255,
                                                    cv2.ADAPTIVE_THRESH_MEAN_C,
                                                    cv2.THRESH_BINARY, 15, 5)

# Exibir a imagem binarizada
plt.figure(figsize=(10,6))
plt.imshow(limiar_adaptativo_referencia, cmap="gray")

# Ler a imagem do PCB de teste
imagem_teste = cv2.imread('/SUA_IMAGEM_DE_TESTE_AQUI')

# Exibir a imagem original do PCB de teste
plt.figure(figsize=(10,6))
plt.imshow(imagem_teste, cmap="gray")

# Ler a imagem do PCB de teste em escala de cinza
imagem_teste_cinza = cv2.imread('SUA_IMAGEM_DE_TESTE_AQUI', 0)

# Redimensionar a imagem do PCB de teste
imagem_teste_redimensionada = cv2.resize(imagem_teste_cinza, (750, 450))

# Exibir a imagem do PCB de teste redimensionada em escala de cinza
plt.figure(figsize=(10,6))
plt.imshow(imagem_teste_redimensionada, cmap="gray")

# Aplicar desfoque Gaussiano na imagem de teste antes da binarização
imagem_teste_desfocada = cv2.GaussianBlur(imagem_teste_redimensionada, (3,3), 0)

# Binarização adaptativa (média) na imagem de teste
limiar_adaptativo_teste = cv2.adaptiveThreshold(imagem_teste_desfocada, 255,
                                               cv2.ADAPTIVE_THRESH_MEAN_C,
                                               cv2.THRESH_BINARY, 15, 5)

# Exibir a imagem binarizada de teste
plt.figure(figsize=(10,6))
plt.imshow(limiar_adaptativo_teste, cmap="gray")

# Subtração de imagem (imagem de referência - imagem de teste)
imagem_subtraida = cv2.subtract(limiar_adaptativo_referencia, limiar_adaptativo_teste)

# Exibir a imagem resultante após a subtração
plt.figure(figsize=(10,6))
plt.imshow(imagem_subtraida)

# Desfoque mediano para eliminar o ruído de fundo
imagem_final = cv2.medianBlur(imagem_subtraida, 5)

# Exibir o resultado final binário para mostrar os defeitos na imagem
plt.figure(figsize=(10,6))
plt.imshow(imagem_final, cmap="gray")

# Copiar a imagem original para sobrepor as caixas vermelhas e circunferências
img_com_caixas_circulos = imagem_referencia.copy()

# Redimensionar as coordenadas dos contornos de volta à escala original
fator_escala_x = imagem_referencia.shape[1] / imagem_final.shape[1]
fator_escala_y = imagem_referencia.shape[0] / imagem_final.shape[0]

# Ajustar tamanho e cor das caixas vermelhas
largura_caixa = 3
cor_caixa = (0, 0, 255)  # Vermelho intenso

# Desenhar caixas vermelhas ao redor dos contornos na imagem original
for contorno in contornos:
    x, y, w, h = cv2.boundingRect(contorno)

    # Ajustar tamanho (aumentar um pouco)
    x -= 5
    y -= 5
    w += 10
    h += 10

    x = int(x * fator_escala_x)
    y = int(y * fator_escala_y)
    w = int(w * fator_escala_x)
    h = int(h * fator_escala_y)

    cv2.rectangle(img_com_caixas_circulos, (x, y), (x + w, y + h), cor_caixa, largura_caixa)

# Exibir a imagem original com as caixas vermelhas e circunferências
plt.figure(figsize=(10, 6))
plt.imshow(img_com_caixas_circulos)
plt.show()

