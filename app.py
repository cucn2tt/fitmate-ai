import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import date
from PIL import Image
import io

import config
from utils.calories import get_calorie_info
from utils.file_ops import save_record, load_data, get_recent_data, get_today_record
from utils.deepseek_client import chat as deepseek_chat
from utils.doubao_client import analyze_food
from prompts.training import build_training_prompt
from prompts.diet import build_diet_prompt
from prompts.body_analysis import build_analysis_prompt
from prompts.current_meal import build_current_meal_prompt

st.set_page_config(page_title="FitMate AI", page_icon="💪", layout="wide")

# ── Sidebar ──────────────────────────────────
with st.sidebar:
    st.title("💪 FitMate AI")
    st.caption("智能健身规划与饮食管理")

    page = st.radio(
        "导航",
        ["每日记录", "训练计划", "饮食计划", "拍照识食", "体脂分析", "历史数据"],
        label_visibility="collapsed",
    )

    st.divider()
    st.caption(f"📅 {date.today()}")

    with st.expander("⚙️ 个人画像"):
        profile = config.USER_PROFILE.copy()
        profile["weight"] = st.number_input("体重(kg)", 40.0, 150.0, float(profile["weight"]), 0.1)
        profile["goal"] = st.selectbox("目标", ["减脂", "增肌"], index=0 if profile["goal"] == "减脂" else 1)
        profile["level"] = st.selectbox("训练水平", ["新手", "中级", "高级"], index=1)
        profile["workout_time"] = st.slider("训练时间(分钟)", 15, 90, profile["workout_time"], 5)
        profile["location"] = st.selectbox("场地", ["居家", "健身房"], index=0 if profile["location"] == "居家" else 1)
        profile["restrictions"] = st.text_input("饮食限制", profile["restrictions"], placeholder="如：不吃猪肉")

    st.divider()
    st.caption("Made with ❤️ + DeepSeek + 豆包")


# ── 每日记录 ─────────────────────────────────
if page == "每日记录":
    st.header("📝 每日记录")

    today_record = get_today_record()

    col1, col2 = st.columns(2)
    with col1:
        default_weight = today_record["体重"] if today_record else profile["weight"]
        weight = st.number_input("体重 (kg)", 30.0, 200.0, default_weight, 0.1, key="rec_weight")
    with col2:
        default_waist = today_record["腰围"] if today_record else 75.0
        waist = st.number_input("腰围 (cm)", 40.0, 150.0, default_waist, 0.1, key="rec_waist")

    notes = st.text_input("备注（可选）", placeholder="例：今天感觉状态不错")

    if st.button("💾 保存记录", use_container_width=True):
        save_record(str(date.today()), weight, waist, notes)
        st.success("保存成功！")
        st.rerun()

    if today_record:
        st.info(f"今日已记录：体重 {today_record['体重']}kg | 腰围 {today_record['腰围']}cm")


# ── 训练计划 ─────────────────────────────────
elif page == "训练计划":
    st.header("🏋️ 训练计划")

    if st.button("🎲 生成今日训练计划", use_container_width=True):
        with st.spinner("DeepSeek 正在为你生成训练计划..."):
            prompt = build_training_prompt(profile)
            plan = deepseek_chat(prompt, "你是专业健身教练，输出简洁专业的训练计划。")
            st.session_state["training_plan"] = plan

    if "training_plan" in st.session_state:
        st.markdown(st.session_state["training_plan"])


# ── 饮食计划 ─────────────────────────────────
elif page == "饮食计划":
    st.header("🍽️ 饮食计划")

    cal_info = get_calorie_info(profile)
    with st.expander("📊 热量计算详情"):
        st.write(f"基础代谢(BMR)：{cal_info['bmr']} kcal")
        st.write(f"每日消耗(TDEE)：{cal_info['tdee']} kcal")
        st.write(f"目标摄入：{cal_info['target_calories']} kcal")

    if st.button("🎲 生成今日饮食计划", use_container_width=True):
        with st.spinner("DeepSeek 正在为你生成饮食计划..."):
            prompt = build_diet_prompt(profile, cal_info["target_calories"])
            plan = deepseek_chat(prompt, "你是专业营养师，输出简洁实用的饮食计划。")
            st.session_state["diet_plan"] = plan

    if "diet_plan" in st.session_state:
        st.markdown(st.session_state["diet_plan"])


# ── 拍照识食 ─────────────────────────────────
elif page == "拍照识食":
    st.header("📸 拍照识食")

    uploaded = st.file_uploader("上传食物照片", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

    if uploaded:
        image = Image.open(uploaded)
        st.image(image, caption="已上传", width=300)

        if st.button("🔍 识别食物", use_container_width=True):
            img_bytes = io.BytesIO()
            image.save(img_bytes, format="JPEG")

            with st.spinner("豆包视觉模型识别中..."):
                result = analyze_food(img_bytes.getvalue())

            if result.get("parse_error"):
                st.warning("模型返回格式异常，原始结果如下：")
                st.text(result.get("raw_response", ""))
            else:
                st.subheader("🍽️ 识别结果")
                dishes = result.get("dishes", [])
                total_cal = result.get("total_calories", 0)

                df = pd.DataFrame(dishes)
                df.columns = ["菜品", "热量(kcal)"]
                st.table(df)
                st.metric("合计热量", f"{total_cal} kcal")

                cal_info = get_calorie_info(profile)
                remaining = round(cal_info["target_calories"] - total_cal, 1)
                st.metric("今日剩余预算", f"{remaining} kcal",
                          delta=f"-{total_cal}" if total_cal > 0 else None)

                with st.spinner("DeepSeek 生成补救建议..."):
                    remedy_prompt = build_current_meal_prompt(dishes, total_cal, remaining)
                    remedy = deepseek_chat(remedy_prompt)
                    st.info(f"💡 {remedy}")


# ── 体脂分析 ─────────────────────────────────
elif page == "体脂分析":
    st.header("📈 体脂趋势分析")

    recent = get_recent_data(7)
    if recent.empty:
        st.warning("暂无数据，请先在「每日记录」中录入体重和腰围。")
    else:
        weight_list = recent["体重"].tolist()
        waist_list = recent["腰围"].tolist()

        if st.button("🔍 分析趋势", use_container_width=True):
            with st.spinner("DeepSeek 正在分析..."):
                prompt = build_analysis_prompt(weight_list, waist_list)
                analysis = deepseek_chat(prompt, "你是健身数据分析师，输出简洁专业的分析。")
                st.session_state["body_analysis"] = analysis

        if "body_analysis" in st.session_state:
            st.markdown(st.session_state["body_analysis"])

        # 简易趋势图
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=recent["日期"], y=recent["体重"], mode="lines+markers", name="体重(kg)"))
        fig.add_trace(go.Scatter(x=recent["日期"], y=recent["腰围"], mode="lines+markers", name="腰围(cm)", yaxis="y2"))
        fig.update_layout(
            height=300, margin=dict(l=0, r=0, t=10, b=0),
            yaxis=dict(title="体重(kg)"),
            yaxis2=dict(title="腰围(cm)", overlaying="y", side="right"),
            legend=dict(orientation="h", y=1.1),
        )
        st.plotly_chart(fig, use_container_width=True)


# ── 历史数据 ─────────────────────────────────
elif page == "历史数据":
    st.header("📊 历史数据")

    df = load_data()
    if df.empty:
        st.warning("暂无数据")
    else:
        tab1, tab2, tab3 = st.tabs(["图表", "数据", "统计"])

        with tab1:
            col1, col2 = st.columns(2)
            with col1:
                fig_w = go.Figure()
                fig_w.add_trace(go.Scatter(x=df["日期"], y=df["体重"], mode="lines+markers",
                                           line=dict(color="#FF6B6B"), name="体重"))
                fig_w.update_layout(title="体重变化", height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_w, use_container_width=True)

            with col2:
                fig_wa = go.Figure()
                fig_wa.add_trace(go.Scatter(x=df["日期"], y=df["腰围"], mode="lines+markers",
                                            line=dict(color="#4ECDC4"), name="腰围"))
                fig_wa.update_layout(title="腰围变化", height=300, margin=dict(l=0, r=0, t=30, b=0))
                st.plotly_chart(fig_wa, use_container_width=True)

        with tab2:
            st.dataframe(df.sort_values("日期", ascending=False), use_container_width=True, hide_index=True)

        with tab3:
            if len(df) >= 2:
                w_change = round(df["体重"].iloc[-1] - df["体重"].iloc[0], 1)
                wa_change = round(df["腰围"].iloc[-1] - df["腰围"].iloc[0], 1)
                c1, c2 = st.columns(2)
                c1.metric("总体重变化", f"{w_change} kg", delta=f"{w_change}")
                c2.metric("总腰围变化", f"{wa_change} cm", delta=f"{wa_change}")
            else:
                st.caption("录入2天以上数据后显示统计")
