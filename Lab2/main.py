import os

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.colors import ListedColormap
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler

# Настройка стиля графиков и папок
sns.set_style("whitegrid")
FIG = "reports/figures"     # куда сохраняем рисунки
PROC = "data/processed"     # куда сохраняем обработанные данные
os.makedirs(FIG, exist_ok=True)
os.makedirs(PROC, exist_ok=True)

# Палитра статусов: 0 = норма (зелёный), 1 = выброс (красный), 2 = пропуск (чёрный)
CMAP = ListedColormap(["#2ecc71", "#e74c3c", "#000000"])


def savefig(fig, name):
    """Сохраняет рисунок в папку reports/figures."""
    fig.tight_layout()
    fig.savefig(f"{FIG}/{name}", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print("  +", name)


def iqr_bounds(s):
    """Считает нижнюю и верхнюю границы выбросов методом IQR."""
    q1 = s.quantile(0.25)    # нижний квартиль (25-й перцентиль)
    q3 = s.quantile(0.75)    # верхний квартиль (75-й перцентиль)
    iqr = q3 - q1            # межквартильный размах
    low = q1 - 1.5 * iqr     # нижняя граница (1.5 — стандартный множитель)
    high = q3 + 1.5 * iqr    # верхняя граница
    return low, high


def is_outlier(s):
    """Возвращает True/False для каждой строки: является ли значение выбросом."""
    low, high = iqr_bounds(s)
    result = (s < low) | (s > high)   # True, если меньше low или больше high
    result = result.fillna(False)     # пропуск (NaN) выбросом не считаем
    return result


def status_matrix(df, num_cols):
    """Строит таблицу статусов: 0 = норма, 1 = выброс, 2 = пропуск."""
    # Создаём таблицу такого же размера, заполненную нулями
    s = pd.DataFrame(0, index=df.index, columns=num_cols, dtype=int)

    for col in num_cols:
        # В строках, где пропуск, ставим 2
        s.loc[df[col].isnull(), col] = 2
        # В строках, где выброс, ставим 1
        s.loc[is_outlier(df[col]), col] = 1

    return s


# ============ 1. Импорт датасета ============
df = pd.read_csv("data/train.csv")

# Собираем список числовых столбцов
num_cols = list(df.select_dtypes("number").columns)
# Id и DistrictId — это идентификаторы, а не признаки, поэтому убираем их
num_cols.remove("Id")
num_cols.remove("DistrictId")

print("Размер датасета:", df.shape)

print("\nПропуски (в каких столбцах и сколько):")
for col in df.columns:
    n = int(df[col].isnull().sum())   # количество пропусков в столбце
    if n > 0:
        print(f"  {col}: {n}")

print("\nВыбросы до очистки:")
for col in num_cols:
    n = int(is_outlier(df[col]).sum())  # количество выбросов в столбце
    print(f"  {col}: {n}")


# ============ 2. Очистка: пропуски и выбросы ============
df_clean = df.copy()   # копируем, чтобы не менять исходные данные

# 2.1. Заполняем пропуски
for col in df_clean.columns:
    if df_clean[col].isnull().any():   # если в столбце есть хотя бы один пропуск
        if pd.api.types.is_numeric_dtype(df_clean[col]):
            # Число -> заполняем медианой (средним "по середине")
            df_clean[col] = df_clean[col].fillna(df_clean[col].median())
        else:
            # Текст -> заполняем модой (самым частым значением)
            df_clean[col] = df_clean[col].fillna(df_clean[col].mode()[0])

# 2.2. Исправляем HouseYear
# Часть значений записана как дата ДДММГГГГ (20052011 = 20.05.2011).
# Остаток от деления на 10000 берёт последние 4 цифры — то есть год.
df_clean["HouseYear"] = df_clean["HouseYear"] % 10000

# 2.3. Устраняем выбросы (capping)
# Каждое значение "зажимаем" в границы IQR: меньше low -> low, больше high -> high
for col in num_cols:
    low, high = iqr_bounds(df_clean[col])
    df_clean[col] = np.clip(df_clean[col], low, high)

# Проверяем, что всё исправлено
print("\nПропусков после очистки:", int(df_clean.isnull().sum().sum()))
print("Выбросов после очистки:")
for col in num_cols:
    print(f"  {col}: {int(is_outlier(df_clean[col]).sum())}")


# ============ 3. Графики «до / после» ============

# 3.1. Тепловая карта пропусков и выбросов (слева ДО, справа ПОСЛЕ)
fig, ax = plt.subplots(1, 2, figsize=(16, 6))

# .T переворачивает таблицу: признаки по вертикали, строки по горизонтали
sns.heatmap(status_matrix(df, num_cols).T, cmap=CMAP, vmin=0, vmax=2,
            cbar=False, xticklabels=False, ax=ax[0])
ax[0].set_title("ДО обработки")

sns.heatmap(status_matrix(df_clean, num_cols).T, cmap=CMAP, vmin=0, vmax=2,
            cbar=False, xticklabels=False, ax=ax[1])
ax[1].set_title("ПОСЛЕ обработки")

fig.suptitle("Тепловая карта пропусков и выбросов")
savefig(fig, "01_heatmap_missing_outliers.png")

# 3.2. График распределения (гистограмма + кривая KDE)
fig, ax = plt.subplots(1, 2, figsize=(12, 4))

sns.histplot(df["Price"], kde=True, bins=50, color="#e74c3c", ax=ax[0])
ax[0].set_title("Price — ДО очистки")
ax[0].grid(alpha=0.3)

sns.histplot(df_clean["Price"], kde=True, bins=50, color="#2ecc71", ax=ax[1])
ax[1].set_title("Price — ПОСЛЕ очистки")
ax[1].grid(alpha=0.3)

fig.suptitle("График распределения Price (гистограмма + KDE)")
savefig(fig, "02_distribution_price.png")

# 3.3. BoxPlot (ящик с усами)
fig, ax = plt.subplots(1, 2, figsize=(10, 5))

sns.boxplot(y=df["Price"], color="#e74c3c", ax=ax[0])
ax[0].set_title("Price — ДО очистки")
ax[0].grid(alpha=0.3)

sns.boxplot(y=df_clean["Price"], color="#2ecc71", ax=ax[1])
ax[1].set_title("Price — ПОСЛЕ очистки")
ax[1].grid(alpha=0.3)

fig.suptitle("BoxPlot Price до и после устранения выбросов")
savefig(fig, "03_boxplot_price.png")

# 3.4. Столбчатые диаграммы категориальных признаков
fig, ax = plt.subplots(2, 2, figsize=(12, 8))
ax = ax.ravel()   # превращаем сетку 2x2 в плоский список из 4 осей

cat_cols = ["Ecology_2", "Ecology_3", "Shops_2", "Rooms"]
for i in range(4):
    col = cat_cols[i]
    values = df[col]
    if col == "Rooms":
        values = values.astype(int)   # число комнат: 1.0 -> 1

    counts = values.value_counts()    # сколько раз встречается каждое значение
    counts.plot.bar(ax=ax[i], color="#3498db")
    ax[i].set_title(col)
    ax[i].set_ylabel("Количество")

fig.suptitle("Столбчатые диаграммы категориальных признаков")
savefig(fig, "04_categorical_barplots.png")


# ============ 4. Новые признаки + кодирование ============
df_feat = df_clean.copy()

# 4.1. Генерация новых признаков (нужно не меньше двух)
# .clip(lower=1) заменяет 0 на 1, чтобы не делить на ноль
df_feat["Square_per_Room"] = df_feat["Square"] / df_feat["Rooms"].clip(lower=1)
df_feat["Kitchen_Ratio"] = df_feat["KitchenSquare"] / df_feat["Square"]
df_feat["Floor_Ratio"] = df_feat["Floor"] / df_feat["HouseFloor"].clip(lower=1)
df_feat["Is_New_Building"] = (df_feat["HouseYear"] >= 2000).astype(int)  # 1 или 0

# 4.2. Текстовые (категориальные) столбцы = все нечисловые
text_cols = []
for col in df_feat.columns:
    if not pd.api.types.is_numeric_dtype(df_feat[col]):
        text_cols.append(col)

# Удаляем столбцы, где всего одно значение (например Country)
for col in text_cols:
    if df_feat[col].nunique() <= 1:
        df_feat = df_feat.drop(columns=[col])

# Делим столбцы: мало значений -> OHE, много значений -> Label Encoding
ohe_cols = []
label_cols = []
for col in text_cols:
    if df_feat[col].nunique() <= 20:
        ohe_cols.append(col)
    else:
        label_cols.append(col)

# 4.3. OHE-кодирование (One-Hot Encoding): каждый вариант -> отдельный столбец 0/1
df_enc = pd.get_dummies(df_feat, columns=ohe_cols)

# 4.4. Label Encoding: каждое значение -> целое число
for col in label_cols:
    le = LabelEncoder()
    df_enc[col] = le.fit_transform(df_enc[col].astype(str))

# DistrictId — числовой, но это категория (номер района), кодируем так же
le = LabelEncoder()
df_enc["DistrictId"] = le.fit_transform(df_enc["DistrictId"].astype(str))

# Id — просто номер строки, удаляем
df_enc = df_enc.drop(columns=["Id"])

print("\nНовые признаки: Square_per_Room, Kitchen_Ratio, Floor_Ratio, Is_New_Building")
print("Размер после кодирования:", df_enc.shape)


# ============ 5. Стандартизация и нормализация ============
# Не масштабируем: DistrictId (категория) и Is_New_Building (уже 0/1)
no_scale = {"DistrictId", "Is_New_Building"}

scale_cols = []
for col in df_enc.columns:
    if pd.api.types.is_numeric_dtype(df_enc[col]) and col not in no_scale:
        scale_cols.append(col)

# Стандартизация: среднее = 0, стандартное отклонение = 1
df_std = df_enc.copy()
scaler = StandardScaler()
df_std[scale_cols] = scaler.fit_transform(df_enc[scale_cols])

# Нормализация: все значения в диапазоне от 0 до 1
df_norm = df_enc.copy()
scaler = MinMaxScaler()
df_norm[scale_cols] = scaler.fit_transform(df_enc[scale_cols])

print("\nСтандартизация (Price mean=0, std=1):", round(float(df_std["Price"].mean()), 3))
print("Нормализация (Price min=0, max=1):",
      round(float(df_norm["Price"].min()), 3),
      round(float(df_norm["Price"].max()), 3))


# ============ 6. Дополнительные графики ============

# 6.1. Корреляционная тепловая карта
corr_cols = ["Rooms", "Square", "LifeSquare", "KitchenSquare",
             "Floor", "HouseFloor", "HouseYear", "Price"]

fig, ax = plt.subplots(figsize=(9, 7))
sns.heatmap(df_enc[corr_cols].corr(), annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
ax.set_title("Корреляционная тепловая карта")
savefig(fig, "06_correlation_heatmap.png")

# 6.2. Сравнение масштабирования (гистограммы Price в трёх вариантах)
fig, ax = plt.subplots(1, 3, figsize=(15, 4))

sns.histplot(df_enc["Price"], kde=True, bins=50, color="#3498db", ax=ax[0])
ax[0].set_title("Price — исходный")
ax[0].grid(alpha=0.3)

sns.histplot(df_std["Price"], kde=True, bins=50, color="#3498db", ax=ax[1])
ax[1].set_title("Price — стандартизация")
ax[1].grid(alpha=0.3)

sns.histplot(df_norm["Price"], kde=True, bins=50, color="#3498db", ax=ax[2])
ax[2].set_title("Price — нормализация")
ax[2].grid(alpha=0.3)

fig.suptitle("Сравнение масштабирования (Price)")
savefig(fig, "07_scaling_price.png")


# ============ 7. Сохранение результатов ============
df_clean.to_csv(f"{PROC}/data_clean.csv", index=False)
df_enc.to_csv(f"{PROC}/data_encoded.csv", index=False)
df_std.to_csv(f"{PROC}/data_standardized.csv", index=False)
df_norm.to_csv(f"{PROC}/data_normalized.csv", index=False)

print("\nГотово. Данные сохранены в data/processed/, графики в reports/figures/.")
