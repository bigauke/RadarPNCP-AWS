import os
print("Testando Chrome com bypass de Autoplay...")
os.system('start chrome "https://www.youtube.com/watch?v=nUCodt4zVw4&autoplay=1" --autoplay-policy=no-user-gesture-required')
print("Comando enviado pro Chrome!")
