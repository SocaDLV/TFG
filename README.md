Arxius utilitzats en el muntatge del treball de fi de grau (TFG), realitzat a la RTU, Riga.

A CORREGIR/FER:

- Es carreguen les imatges de manera rara: test_0, test_1, test_10, test_100, test_1000, test_1001 ...  ✅
- Adaptar "TensorFlowV2_IntelNCS2.py" per a que pase de 0-999 clases a una de les 200 del Tiny. Vorer bibliografia nº36 + arxius words.txt i wnids.txt ✅
- Organitzar en carpetes el GitHub, una carpeta per model de inferencia,i dins,una per plataforma. ✅
- Instalar OpenVINO en la RP2 + provar codi del IntelNCS2 ahi (checkear Python 3.9.0) (No fucniona pq OpenVINO necesita un Python de 64-bits) ✅
- Run al main.py del entrenament de MobileNetV2, avore si es completa correctament ✅
- Com entrenar MobileNetV2 amb imatges de 64x64 no funciona, escalarles a 94x94. REDUIR tamany de la carpeta de entrenament xq sinó plena la RAM. ✅
