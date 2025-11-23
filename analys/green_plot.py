import numpy as np
import matplotlib.pyplot as plt
import imageio
from cycler import cycler

def readIntensity(photoName, plotName, lamp, surface):
    photo = imageio.v2.imread(photoName)
    background = photo[460:840 ,760:965, 0:3].swapaxes(0, 1)
    cut = photo[460:840 ,760:965, 0:3].swapaxes(0, 1)
    rgb = np.mean(cut, axis=(0))
    luma = 0.2989 * rgb[:, 0] + 0.5866 * rgb[:, 1] + 0.1144 * rgb[:, 2]

    plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b'])))
    fig = plt.figure(figsize=(10, 5), dpi=200)
    plt.title('Интенсивность отражённого излучения\n' + '{} / {}'.format(lamp, surface))
    plt.xlabel('Относительный номер пикселя')
    plt.ylabel('Яркость')
    plt.plot(rgb, label=['r', 'g', 'b'])
    plt.plot(luma, 'w', label='I')
    plt.legend()
    plt.imshow(background, origin='lower')
    plt.savefig(plotName)
    plt.show()
    return luma

intensity = readIntensity(
    photoName='green.jpg',   # Имя файла с изображением
    plotName='plot_green.png',      # Имя файла для сохранения графика
    lamp='Лампа накаливания', # Тип лампы
    surface='Зеленая бумага'   # Тип поверхности
)