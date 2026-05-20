import os
import csv
from datetime import date

import pandas as pd

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
DATA_FILE = os.path.join(DATA_DIR, "fitmate_data.csv")

HEADERS = ["日期", "体重", "腰围", "备注"]


def ensure_data_file():
    """确保数据文件存在，不存在则创建"""
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(HEADERS)


def save_record(record_date: str, weight: float, waist: float, notes: str = ""):
    """追加一条记录到CSV"""
    ensure_data_file()
    with open(DATA_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([record_date, weight, waist, notes])


def load_data() -> pd.DataFrame:
    """加载全部数据"""
    ensure_data_file()
    df = pd.read_csv(DATA_FILE)
    if not df.empty:
        df["日期"] = pd.to_datetime(df["日期"])
        df = df.sort_values("日期")
    return df


def get_recent_data(days: int = 7) -> pd.DataFrame:
    """获取最近N天数据"""
    df = load_data()
    if df.empty:
        return df
    cutoff = pd.Timestamp(date.today()) - pd.Timedelta(days=days - 1)
    return df[df["日期"] >= cutoff]


def get_today_record() -> dict | None:
    """获取今日记录，若不存在返回None"""
    df = load_data()
    if df.empty:
        return None
    today_str = str(date.today())
    today_rows = df[df["日期"].dt.strftime("%Y-%m-%d") == today_str]
    if today_rows.empty:
        return None
    row = today_rows.iloc[-1]
    return {
        "日期": today_str,
        "体重": float(row["体重"]),
        "腰围": float(row["腰围"]),
        "备注": str(row.get("备注", "")),
    }
