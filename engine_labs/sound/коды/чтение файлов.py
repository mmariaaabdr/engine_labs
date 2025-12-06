# Если использовали files.upload()
from google.colab import files
import io

uploaded = files.upload()

# Чтение данных из содержимого файлов
data1 = np.loadtxt(io.BytesIO(uploaded['data_1_попытка1 обычный воздух.txt']))
data2 = np.loadtxt(io.BytesIO(uploaded['data_0_попытка1 обычный воздух.txt']))
