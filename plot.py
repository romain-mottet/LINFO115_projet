import matplotlib.pyplot as plt

plt.rcParams["figure.figsize"] = [7.50, 3.50]
plt.rcParams["figure.autolayout"] = True

x = [0, 0.25, 0.5, 0.75, 1]
y = [0, 2489, 9226, 18255, 33493]

plt.title('Evolution of triadic closures over quartiles')
plt.ylabel('Number of triadic closure')
plt.xlabel('Quartiles')

fig = plt.plot(x, y, "-o")

plt.savefig('triadic_closure.png')
plt.show()