lockdow = False
grana = 30

# se cumprir todas primeira condições saida "Em casa", se não "Uhuuu"
status = 'Em casa' if lockdow or grana <= 100 else 'Uhuuu'

print(f'O status e: {status}')

