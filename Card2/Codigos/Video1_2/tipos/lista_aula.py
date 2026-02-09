nums = [1, 2, 3]
print(type(nums))

nums.append(3)  # adicione elementos na lista
nums.append(4)
nums.append(500)
print(len(nums))  # o "len" lê o tamanho da lista

print(2 in nums)

# A terceira posição recebera o valor 100 (Se inicia na posição 0)
nums[3] = 100
nums.insert(0, -200)  # A posição 0 recebera o valor -200[5]
print(nums[-1])  # Mostra o ultimo valor
print(nums[-2])  # Mostra o penúltimo valor

print(nums)
