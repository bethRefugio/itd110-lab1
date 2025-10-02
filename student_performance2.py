import io
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

st.markdown("""
<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@flaticon/flaticon-uicons/css/all/all.min.css">
<link rel='stylesheet' href='https://cdn-uicons.flaticon.com/3.0.0/uicons-thin-rounded/css/uicons-thin-rounded.css'>
<link rel='stylesheet' href='https://cdn-uicons.flaticon.com/3.0.0/uicons-solid-rounded/css/uicons-solid-rounded.css'>
""", unsafe_allow_html=True)
# Page Config with custom theme
st.set_page_config(
    page_title="ITD105: Student Performance Analysis Dashboard",
    page_icon="assets/analysis.png",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for enhanced styling
st.markdown("""
<style>
    
    /* Style all sidebar buttons */
    div.stButton > button {
        background-color: #6495ED;  /* button background */
        color: white;               /* text color */
        border-radius: 8px;         /* rounded corners */
        border: none;               /* remove border */
        font-weight: bold;
        transition: 0.3s;
    }

    div.stButton > button:hover {
        background-color: #155a8a;  /* hover color */
        color: #fff;
    }
    .stMultiSelect div[data-baseweb="tag"] {
        background-color: #6495ED;  /* background color */
        color: white;               /* text color */
        border-radius: 6px;         /* rounded corners */
        padding: 2px 8px;
        font-weight: bold;
    }
    /* Change hover color of chips */
    .stMultiSelect div[data-baseweb="tag"]:hover {
        background-color: #155a8a;  /* darker on hover */
        color: #fff;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        background-color: #e8f4f8;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #2ecc71;
        margin: 1rem 0;
        color: #333;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    .stTabs [data-baseweb="tab"] {
        height: 3rem;
        padding: 0 2rem;
        background-color: #f0f2f6;
        border-radius: 0.5rem 0.5rem 0 0;
            color: #555;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1f77b4;
        color: white;
    }
    div[data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Title
st.markdown("<h1 style='text-align: center;'>Student Performance Analysis Dashboard</h1>", unsafe_allow_html=True)
st.markdown("""
<div style='text-align: center; padding: 1rem; background-color: #a8e4a0; border-radius: 0.5rem; margin-bottom: 2rem;'>
    <p style='font-size: 1.1rem; color: #555;'>
        <strong>ITD105 Course Project</strong> - Comprehensive Data Analysis using Streamlit
    </p>
    <p style='font-size: 0.9rem; color: #777;'>
        Explore student performance patterns, correlations, and insights through interactive visualizations
    </p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# File uploader
st.subheader("📁 Upload Dataset")
uploaded_file = st.file_uploader("Upload CSV file here:", type="csv", help="Upload the student performance dataset")

if uploaded_file is not None:
    
    # Load dataset
    df = pd.read_csv(uploaded_file, delimiter=';')
    df['Average_Grade'] = ((df['G1'] + df['G2'] + df['G3']) / 3).round(2)
    
    # Performance categories
    def categorize_performance(grade):
        if grade >= 16:
            return 'Excellent'
        elif grade >= 14:
            return 'Good'
        elif grade >= 10:
            return 'Average'
        else:
            return 'Needs Improvement'
    
    df['Performance_Category'] = df['G3'].apply(categorize_performance)
    
    # Sidebar Configuration
    st.sidebar.markdown("## 🎛️ Dashboard Controls")
    st.sidebar.markdown("---")
    
    # About Section
    with st.sidebar.expander("ℹ️ About This Dashboard", expanded=False):
        st.markdown("""
        **Purpose:** Analyze student academic performance and identify key factors influencing success.
        
        **Features:**
        - Interactive filtering and data exploration
        - Correlation analysis
        - Performance visualizations
        - Statistical insights
        
        **Dataset:** Portuguese student performance data including demographics, social factors, and academic records.
        """)
    
    st.sidebar.markdown("### 🔍 Filter Options")
    
    # School Filter
    school_filter = st.sidebar.multiselect(
        "🏫 Select School:",
        options=df['school'].unique(),
        default=df['school'].unique(),
        help="Filter by school: GP (Gabriel Pereira) or MS (Mousinho da Silveira)"
    )
    
    # Sex Filter
    sex_filter = st.sidebar.multiselect(
        "👤 Select Gender:",
        options=df['sex'].unique(),
        default=df['sex'].unique(),
        help="Filter by student gender"
    )
    
    # Age Filter
    age_filter = st.sidebar.slider(
        "📅 Age Range:",
        min_value=int(df['age'].min()),
        max_value=int(df['age'].max()),
        value=(int(df['age'].min()), int(df['age'].max())),
        help="Select age range for analysis"
    )
    
    # Address Filter
    address_filter = st.sidebar.multiselect(
        "🏘️ Address Type:",
        options=df['address'].unique(),
        default=df['address'].unique(),
        help="U = Urban, R = Rural"
    )
    
    # Parental Education Filter
    st.sidebar.markdown("**👨‍👩‍👧 Parental Education:**")
    col1, col2 = st.sidebar.columns(2)
    with col1:
        medu_filter = st.slider(
            "Mother's Edu:",
            min_value=int(df['Medu'].min()),
            max_value=int(df['Medu'].max()),
            value=(int(df['Medu'].min()), int(df['Medu'].max())),
            help="0=none, 1=4th grade, 2=5-9th, 3=secondary, 4=higher"
        )
    with col2:
        fedu_filter = st.slider(
            "Father's Edu:",
            min_value=int(df['Fedu'].min()),
            max_value=int(df['Fedu'].max()),
            value=(int(df['Fedu'].min()), int(df['Fedu'].max())),
            help="0=none, 1=4th grade, 2=5-9th, 3=secondary, 4=higher"
        )
    
    # Study Time Filter
    studytime_filter = st.sidebar.slider(
        "📚 Study Time (weekly):",
        min_value=int(df['studytime'].min()),
        max_value=int(df['studytime'].max()),
        value=(int(df['studytime'].min()), int(df['studytime'].max())),
        help="1: <2hrs, 2: 2-5hrs, 3: 5-10hrs, 4: >10hrs"
    )
    
    # Failures Filter
    failures_filter = st.sidebar.slider(
        "❌ Past Failures:",
        min_value=int(df['failures'].min()),
        max_value=int(df['failures'].max()),
        value=(int(df['failures'].min()), int(df['failures'].max())),
        help="Number of past class failures"
    )
    
    # Absences Filter
    absences_filter = st.sidebar.slider(
        "📅 Absences:",
        min_value=int(df['absences'].min()),
        max_value=int(df['absences'].max()),
        value=(int(df['absences'].min()), int(df['absences'].max())),
        help="Number of school absences"
    )
    
    # Internet Access Filter
    internet_filter = st.sidebar.multiselect(
        "🌐 Internet Access:",
        options=df['internet'].unique(),
        default=df['internet'].unique(),
        help="Filter by internet access at home"
    )
    
    # Apply Filters
    filtered_df = df[
        (df['school'].isin(school_filter)) &
        (df['sex'].isin(sex_filter)) &
        (df['age'] >= age_filter[0]) & (df['age'] <= age_filter[1]) &
        (df['address'].isin(address_filter)) &
        (df['Medu'] >= medu_filter[0]) & (df['Medu'] <= medu_filter[1]) &
        (df['Fedu'] >= fedu_filter[0]) & (df['Fedu'] <= fedu_filter[1]) &
        (df['studytime'] >= studytime_filter[0]) & (df['studytime'] <= studytime_filter[1]) &
        (df['failures'] >= failures_filter[0]) & (df['failures'] <= failures_filter[1]) &
        (df['absences'] >= absences_filter[0]) & (df['absences'] <= absences_filter[1]) &
        (df['internet'].isin(internet_filter))
    ]
    
    st.sidebar.markdown("---")
    st.sidebar.metric("📊 Filtered Records", f"{len(filtered_df)} / {len(df)}")
    st.sidebar.progress(len(filtered_df) / len(df))
    
    # Reset Filters Button
    if st.sidebar.button("🔄 Reset All Filters", use_container_width=True):
        st.rerun()
    
    # Main Content Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📊 Overview", 
        "📈 Performance Analysis", 
        "🔍 Correlations & Insights",
        "📋 Data Exploration",
        "❓ Key Questions"
    ])
    
    # ==================== TAB 1: OVERVIEW ====================
    with tab1:
        st.header("📊 Dataset Overview")
        
        # Key Metrics Row 1
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "👥 Total Students",
                f"{len(filtered_df)}",
                delta=f"{len(filtered_df) - len(df)} from total",
                help="Number of students in filtered dataset"
            )
        
        with col2:
            avg_final = filtered_df['G3'].mean()
            st.metric(
                "📝 Avg Final Grade (G3)",
                f"{avg_final:.2f} / 20",
                delta=f"{avg_final - df['G3'].mean():.2f} vs total",
                help="Average final grade (G3)"
            )
        
        with col3:
            avg_study = filtered_df['studytime'].mean()
            st.metric(
                "📚 Avg Study Time",
                f"{avg_study:.2f} / 4",
                delta=f"{avg_study - df['studytime'].mean():.2f} vs total",
                help="Average weekly study time"
            )
        
        with col4:
            pass_rate = (filtered_df['G3'] >= 10).sum() / len(filtered_df) * 100
            st.metric(
                "✅ Pass Rate",
                f"{pass_rate:.1f}%",
                help="Percentage of students with G3 >= 10"
            )
        
        # Key Metrics Row 2
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric(
                "🏫 School Split",
                f"GP: {(filtered_df['school'] == 'GP').sum()}",
                delta=f"MS: {(filtered_df['school'] == 'MS').sum()}",
                help="Distribution across schools"
            )
        
        with col2:
            st.metric(
                "👥 Gender Split",
                f"F: {(filtered_df['sex'] == 'F').sum()}",
                delta=f"M: {(filtered_df['sex'] == 'M').sum()}",
                help="Gender distribution"
            )
        
        with col3:
            avg_absences = filtered_df['absences'].mean()
            st.metric(
                "📅 Avg Absences",
                f"{avg_absences:.1f}",
                delta=f"{avg_absences - df['absences'].mean():.1f} vs total",
                help="Average number of absences"
            )
        
        with col4:
            failure_rate = (filtered_df['failures'] > 0).sum() / len(filtered_df) * 100
            st.metric(
                "❌ Students with Failures",
                f"{failure_rate:.1f}%",
                help="Percentage with past failures"
            )
        
        st.markdown("---")
        
        # Data Preview
        st.subheader('📋 Activity B: Data Preview')
        
        # Display options
        col1, col2 = st.columns([3, 1])
        with col1:
            num_rows = st.slider("Number of rows to display:", 5, 50, 10)
        with col2:
            show_all_cols = st.checkbox("Show all columns", value=False)
        
        if show_all_cols:
            st.dataframe(filtered_df.head(num_rows), use_container_width=True)
        else:
            display_cols = ['school', 'sex', 'age', 'address', 'studytime', 'failures', 
                          'absences', 'G1', 'G2', 'G3', 'Average_Grade', 'Performance_Category']
            st.dataframe(filtered_df[display_cols].head(num_rows), use_container_width=True)
        
        st.markdown("""
        <div class='insight-box'>
        <strong>📋 Dataset Insights:</strong>
        <ul>
            <li>Each row represents a <strong>unique student</strong> with academic and personal characteristics</li>
            <li>Key features include <strong>demographics</strong> (age, sex, address), <strong>family background</strong> (parental education, jobs), and <strong>academic performance</strong> (G1, G2, G3 grades)</li>
            <li>The data provides a comprehensive view of factors influencing student success</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Dataset Information and Missing Values
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('🔍 Activity C.1: Dataset Information')
            
            # Create a summary dataframe
            info_data = {
                'Column': filtered_df.columns,
                'Non-Null Count': [filtered_df[col].count() for col in filtered_df.columns],
                'Dtype': [filtered_df[col].dtype for col in filtered_df.columns]
            }
            info_df = pd.DataFrame(info_data)
            
            st.dataframe(info_df, use_container_width=True, height=300)
            
            st.markdown(f"""
            <div class='insight-box'>
            <strong>🔍 Data Structure:</strong>
            <ul>
                <li><strong>Total Columns:</strong> {len(filtered_df.columns)}</li>
                <li><strong>Total Rows:</strong> {len(filtered_df)}</li>
                <li><strong>Numerical Features:</strong> {len(filtered_df.select_dtypes(include=[np.number]).columns)}</li>
                <li><strong>Categorical Features:</strong> {len(filtered_df.select_dtypes(exclude=[np.number]).columns)}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.subheader('✅ Activity C.2: Missing Values')
            
            missing_df = pd.DataFrame({
                'Column': filtered_df.columns,
                'Missing Values': filtered_df.isnull().sum(),
                'Percentage': (filtered_df.isnull().sum() / len(filtered_df) * 100).round(2)
            })
            
            st.dataframe(missing_df, use_container_width=True, height=300)
            
            missing_count = filtered_df.isnull().sum().sum()
            st.markdown(f"""
            <div class='insight-box'>
            <strong>✅ Data Quality:</strong>
            <ul>
                <li><strong>Total Missing Values:</strong> {missing_count}</li>
                <li><strong>Status:</strong> {"🎉 Excellent - No missing values!" if missing_count == 0 else "⚠️ Some missing values detected"}</li>
                <li><strong>Reliability:</strong> {"High data integrity for analysis" if missing_count == 0 else "May need data cleaning"}</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Summary Statistics
        st.subheader('📊 Activity D: Summary Statistics')
        
        st.dataframe(filtered_df.describe(), use_container_width=True)
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>📈 Statistical Overview:</strong>
        <ul>
            <li><strong>Grade Range:</strong> G3 scores range from {filtered_df['G3'].min():.0f} to {filtered_df['G3'].max():.0f} (out of 20)</li>
            <li><strong>Average Performance:</strong> Mean final grade is {filtered_df['G3'].mean():.2f}/20</li>
            <li><strong>Age Distribution:</strong> Students aged {filtered_df['age'].min()}-{filtered_df['age'].max()} years (median: {filtered_df['age'].median():.0f})</li>
            <li><strong>Study Patterns:</strong> Average study time is {filtered_df['studytime'].mean():.2f}/4 scale</li>
            <li><strong>Attendance:</strong> Mean absences: {filtered_df['absences'].mean():.1f} (range: {filtered_df['absences'].min()}-{filtered_df['absences'].max()})</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
    
    # ==================== TAB 2: PERFORMANCE ANALYSIS ====================
    with tab2:
        st.header("📈 Performance Analysis")
        
        # Grade Distribution
        st.subheader("📊 Grade Distribution Overview")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Performance Category Distribution
            perf_dist = filtered_df['Performance_Category'].value_counts()
            fig_perf_cat = px.pie(
                values=perf_dist.values,
                names=perf_dist.index,
                title='Performance Category Distribution',
                color_discrete_sequence=px.colors.sequential.RdBu,
                hole=0.4
            )
            fig_perf_cat.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_perf_cat, use_container_width=True)
        
        with col2:
            # Grade Comparison: G1, G2, G3
            grade_means = pd.DataFrame({
                'Grade Period': ['G1', 'G2', 'G3'],
                'Average Score': [
                    filtered_df['G1'].mean(),
                    filtered_df['G2'].mean(),
                    filtered_df['G3'].mean()
                ]
            })
            
            fig_grade_prog = px.bar(
                grade_means,
                x='Grade Period',
                y='Average Score',
                title='Average Grades Across Periods',
                color='Average Score',
                color_continuous_scale='viridis',
                text='Average Score'
            )
            fig_grade_prog.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            fig_grade_prog.update_layout(yaxis_range=[0, 20])
            st.plotly_chart(fig_grade_prog, use_container_width=True)
        
        st.markdown("---")
        
        # Activity G: Interactive Scatter Plots
        st.subheader('🎯 Activity G: Interactive Performance Visualizations')
        
        # Grade Progression
        st.write("**📈 Grade Progression: G1 vs G2 vs G3**")
        fig_grades = px.scatter(
            filtered_df,
            x='G1',
            y='G2',
            size='G3',
            color='G3',
            title='Grade Progression Analysis',
            hover_data=['school', 'sex', 'age', 'studytime', 'failures', 'absences', 'Average_Grade'],
            labels={'G1': 'First Period Grade', 'G2': 'Second Period Grade', 'G3': 'Final Grade'},
            color_continuous_scale='turbo'
        )
        fig_grades.add_trace(go.Scatter(
            x=[0, 20],
            y=[0, 20],
            mode='lines',
            name='Perfect Correlation',
            line=dict(color='red', dash='dash')
        ))
        fig_grades.update_layout(height=500)
        st.plotly_chart(fig_grades, use_container_width=True)
        
        corr_g1_g2 = filtered_df['G1'].corr(filtered_df['G2'])
        corr_g2_g3 = filtered_df['G2'].corr(filtered_df['G3'])
        corr_g1_g3 = filtered_df['G1'].corr(filtered_df['G3'])
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>🎯 Grade Progression Insights:</strong>
        <ul>
            <li><strong>G1-G2 Correlation:</strong> {corr_g1_g2:.3f} - {"Strong" if abs(corr_g1_g2) > 0.7 else "Moderate"} consistency</li>
            <li><strong>G2-G3 Correlation:</strong> {corr_g2_g3:.3f} - {"Strong" if abs(corr_g2_g3) > 0.7 else "Moderate"} final performance predictability</li>
            <li><strong>G1-G3 Correlation:</strong> {corr_g1_g3:.3f} - Early grades {"strongly" if abs(corr_g1_g3) > 0.7 else "moderately"} predict final outcomes</li>
            <li><strong>Key Insight:</strong> Students with strong G1 scores tend to maintain or improve performance</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Study Time vs Performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📚 Study Time vs. Average Performance**")
            fig_study = px.scatter(
                filtered_df,
                x='studytime',
                y='Average_Grade',
                color='sex',
                title='Study Time Impact on Grades',
                hover_data=['school', 'age', 'failures', 'absences'],
                labels={'studytime': 'Study Time Level', 'Average_Grade': 'Average Grade'},
                trendline="ols"
            )
            st.plotly_chart(fig_study, use_container_width=True)
        
        with col2:
            # Study time by performance category
            study_perf = filtered_df.groupby('studytime')['Average_Grade'].mean().reset_index()
            fig_study_bar = px.bar(
                study_perf,
                x='studytime',
                y='Average_Grade',
                title='Average Grade by Study Time Level',
                labels={'studytime': 'Study Time (1:<2h, 2:2-5h, 3:5-10h, 4:>10h)', 'Average_Grade': 'Avg Grade'},
                color='Average_Grade',
                color_continuous_scale='blues',
                text='Average_Grade'
            )
            fig_study_bar.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig_study_bar, use_container_width=True)
        
        correlation_study = filtered_df['studytime'].corr(filtered_df['Average_Grade'])
        st.markdown(f"""
        <div class='insight-box'>
        <strong>📚 Study Time Analysis:</strong>
        <ul>
            <li><strong>Correlation:</strong> {correlation_study:.3f} - {"Positive" if correlation_study > 0 else "Negative"} relationship</li>
            <li><strong>Trend:</strong> {"More study time generally leads to better grades" if correlation_study > 0.2 else "Weak relationship - study quality matters more than quantity"}</li>
            <li><strong>Efficiency:</strong> Some high-performing students achieve excellent grades with moderate study time</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Absences vs Performance
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**📅 Absences vs. Performance**")
            fig_absences = px.scatter(
                filtered_df,
                x='absences',
                y='Average_Grade',
                color='Performance_Category',
                title='Impact of Absences on Grades',
                hover_data=['school', 'sex', 'age', 'studytime'],
                labels={'absences': 'Number of Absences', 'Average_Grade': 'Average Grade'},
                trendline="ols"
            )
            st.plotly_chart(fig_absences, use_container_width=True)
        
        with col2:
            # Failures impact
            st.write("**❌ Past Failures vs. Final Grade**")
            fig_failures = px.box(
                filtered_df,
                x='failures',
                y='G3', 
                color='failures',
                title='Impact of Past Failures on Final Grade',
                labels={'failures': 'Number of Past Failures', 'G3': 'Final Grade'},
                color_discrete_sequence=px.colors.sequential.Reds
            )

            st.plotly_chart(fig_failures, use_container_width=True)
        
        corr_absence = filtered_df['absences'].corr(filtered_df['Average_Grade'])
        high_absence = filtered_df['absences'].quantile(0.75)
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>📅 Attendance & Performance:</strong>
        <ul>
            <li><strong>Absence Correlation:</strong> {corr_absence:.3f} - {"Negative" if corr_absence < 0 else "Positive"} impact</li>
            <li><strong>High Absence Threshold:</strong> >{high_absence:.0f} absences significantly impacts performance</li>
            <li><strong>Failures Impact:</strong> Students with past failures show lower average final grades</li>
            <li><strong>Intervention:</strong> Monitor students with >10 absences or any past failures</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Demographic Analysis
        st.subheader("👥 Demographic Performance Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # School comparison
            school_perf = filtered_df.groupby(['school', 'sex'])['Average_Grade'].mean().reset_index()
            fig_school = px.bar(
                school_perf,
                x='school',
                y='Average_Grade',
                color='sex',
                title='Average Grade by School and Gender',
                labels={'school': 'School', 'Average_Grade': 'Average Grade'},
                barmode='group',
                text='Average_Grade'
            )
            fig_school.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig_school, use_container_width=True)
        
        with col2:
            # Address type impact
            address_perf = filtered_df.groupby(['address', 'sex'])['Average_Grade'].mean().reset_index()
            fig_address = px.bar(
                address_perf,
                x='address',
                y='Average_Grade',
                color='sex',
                title='Average Grade by Address Type and Gender',
                labels={'address': 'Address (U=Urban, R=Rural)', 'Average_Grade': 'Average Grade'},
                barmode='group',
                text='Average_Grade'
            )
            fig_address.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig_address, use_container_width=True)
        
        # Parental education impact
        st.write("**👨‍👩‍👧 Parental Education Impact**")
        
        col1, col2 = st.columns(2)
        with col1:
            medu_perf = filtered_df.groupby('Medu')['Average_Grade'].mean().reset_index()
            fig_medu = px.line(
                medu_perf,
                x='Medu',
                y='Average_Grade',
                title="Mother's Education vs. Student Performance",
                labels={'Medu': "Mother's Education Level", 'Average_Grade': 'Avg Grade'},
                markers=True
            )
            st.plotly_chart(fig_medu, use_container_width=True)
        
        with col2:
            fedu_perf = filtered_df.groupby('Fedu')['Average_Grade'].mean().reset_index()
            fig_fedu = px.line(
                fedu_perf,
                x='Fedu',
                y='Average_Grade',
                title="Father's Education vs. Student Performance",
                labels={'Fedu': "Father's Education Level", 'Average_Grade': 'Avg Grade'},
                markers=True
            )
            st.plotly_chart(fig_fedu, use_container_width=True)
    
    # ==================== TAB 3: CORRELATIONS & INSIGHTS ====================
    with tab3:
        st.header("🔍 Correlations & Detailed Insights")
        
        # Activity E: Correlation Heatmap
        st.subheader("🔥 Activity E: Correlation Heatmap")
        
        numeric_df = filtered_df.select_dtypes(include=[np.number])
        corr = numeric_df.corr()
        
        # Interactive correlation heatmap with Plotly
        fig_corr = px.imshow(
            corr,
            text_auto='.2f',
            aspect='auto',
            title='Correlation Heatmap of Numeric Features',
            color_continuous_scale='RdBu_r',
            zmin=-1,
            zmax=1
        )
        fig_corr.update_layout(height=700)
        st.plotly_chart(fig_corr, use_container_width=True)
        
        # Find strong correlations
        strong_corr_pairs = []
        for i in range(len(corr.columns)):
            for j in range(i+1, len(corr.columns)):
                corr_val = corr.iloc[i, j]
                if abs(corr_val) > 0.5:
                    strong_corr_pairs.append((corr.columns[i], corr.columns[j], corr_val))
        
        strong_corr_pairs.sort(key=lambda x: abs(x[2]), reverse=True)
        
        st.markdown("### 🔍 Top Correlations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**🔴 Strongest Positive Correlations:**")
            positive_corrs = [x for x in strong_corr_pairs if x[2] > 0][:5]
            for feat1, feat2, val in positive_corrs:
                st.write(f"- **{feat1}** ↔ **{feat2}**: {val:.3f}")
        
        with col2:
            st.markdown("**🔵 Strongest Negative Correlations:**")
            negative_corrs = [x for x in strong_corr_pairs if x[2] < 0][:5]
            if negative_corrs:
                for feat1, feat2, val in negative_corrs:
                    st.write(f"- **{feat1}** ↔ **{feat2}**: {val:.3f}")
            else:
                st.write("No strong negative correlations found")
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>📊 Correlation Analysis Insights:</strong>
        <ul>
            <li><strong>Academic Consistency:</strong> G1, G2, and G3 show very strong positive correlations (>0.8)</li>
            <li><strong>Parental Education:</strong> Mother's and Father's education levels are correlated</li>
            <li><strong>Behavioral Patterns:</strong> Daily and weekend alcohol consumption are correlated</li>
            <li><strong>Performance Predictors:</strong> Early grades (G1) are strong predictors of final outcomes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Pair Plot Section
        st.subheader("🔗 Pair Plot Analysis")
        
        numeric_columns = [col for col in numeric_df.columns if col != 'Average_Grade']
        
        col1, col2 = st.columns([3, 1])
        with col1:
            selected_features = st.multiselect(
                "Select features for pair plot (2-5 recommended):",
                numeric_columns,
                default=['G1', 'G2', 'G3', 'studytime'][:min(4, len(numeric_columns))]
            )
        
        with col2:
            color_by = st.selectbox(
                "Color by:",
                ['sex', 'school', 'address', 'Performance_Category'],
                index=0
            )
        
        if len(selected_features) >= 2:
            fig_pair = px.scatter_matrix(
                filtered_df,
                dimensions=selected_features,
                color=color_by,
                title=f"Pair Plot: {', '.join(selected_features)} (colored by {color_by})",
                height=700
            )
            fig_pair.update_traces(diagonal_visible=False, showupperhalf=False)
            st.plotly_chart(fig_pair, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>🔗 Pair Plot Insights:</strong>
            <ul>
                <li><strong>Matrix View:</strong> Each cell shows relationship between two variables</li>
                <li><strong>Color Patterns:</strong> Reveals how different groups perform across features</li>
                <li><strong>Linear Relationships:</strong> Straight-line patterns indicate strong correlations</li>
                <li><strong>Clusters:</strong> Grouped points suggest categorical differences in behavior</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.info("Please select at least 2 features to generate the pair plot.")
        
        st.markdown("---")
        
        # Feature Importance Analysis
        st.subheader("⭐ Feature Importance for Final Grade (G3)")
        
        # Calculate correlations with G3
        g3_correlations = numeric_df.corr()['G3'].sort_values(ascending=False)
        g3_correlations = g3_correlations[g3_correlations.index != 'G3']  # Remove G3 itself
        
        fig_importance = px.bar(
            x=g3_correlations.values,
            y=g3_correlations.index,
            orientation='h',
            title='Feature Correlations with Final Grade (G3)',
            labels={'x': 'Correlation Coefficient', 'y': 'Feature'},
            color=g3_correlations.values,
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0
        )
        fig_importance.update_layout(height=600)
        st.plotly_chart(fig_importance, use_container_width=True)
        
        top_positive = g3_correlations.nlargest(5)
        top_negative = g3_correlations.nsmallest(5)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**✅ Top Positive Predictors:**")
            for feat, val in top_positive.items():
                st.write(f"- **{feat}**: {val:.3f}")
        
        with col2:
            st.markdown("**⚠️ Top Negative Predictors:**")
            for feat, val in top_negative.items():
                st.write(f"- **{feat}**: {val:.3f}")
    
    # ==================== TAB 4: DATA EXPLORATION ====================
    with tab4:
        st.header("📋 Data Exploration")
        
        # Activity F: Boxplot
        st.subheader("📦 Activity F: Boxplot Visualization")
        
        # Select features for boxplot
        available_features = numeric_df.columns.tolist()
        selected_box_features = st.multiselect(
            "Select features to visualize (max 10):",
            available_features,
            default=['G1', 'G2', 'G3', 'studytime', 'absences', 'failures'][:min(6, len(available_features))]
        )
        
        if selected_box_features:
            # Create normalized boxplot
            fig_box = go.Figure()
            
            for col in selected_box_features:
                if filtered_df[col].max() != filtered_df[col].min():
                    normalized = (filtered_df[col] - filtered_df[col].min()) / (filtered_df[col].max() - filtered_df[col].min())
                else:
                    normalized = filtered_df[col] * 0
                
                fig_box.add_trace(go.Box(
                    y=normalized,
                    name=col,
                    boxmean='sd'
                ))
            
            fig_box.update_layout(
                title='Normalized Boxplot of Selected Features',
                yaxis_title='Normalized Values (0-1)',
                height=500,
                showlegend=True
            )
            st.plotly_chart(fig_box, use_container_width=True)
            
            st.markdown("""
            <div class='insight-box'>
            <strong>📦 Boxplot Analysis:</strong>
            <ul>
                <li><strong>Box:</strong> Contains middle 50% of data (IQR)</li>
                <li><strong>Line in Box:</strong> Median value</li>
                <li><strong>Whiskers:</strong> Extend to 1.5×IQR</li>
                <li><strong>Dots:</strong> Outliers beyond whiskers</li>
                <li><strong>Insight:</strong> Grades show normal distribution; absences/failures are right-skewed</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Distribution Analysis
        st.subheader("📊 Distribution Analysis")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Histogram
            hist_feature = st.selectbox(
                "Select feature for histogram:",
                numeric_df.columns.tolist(),
                index=numeric_df.columns.tolist().index('G3') if 'G3' in numeric_df.columns else 0
            )
            
            fig_hist = px.histogram(
                filtered_df,
                x=hist_feature,
                color='sex',
                title=f'Distribution of {hist_feature}',
                marginal='box',
                nbins=20
            )
            st.plotly_chart(fig_hist, use_container_width=True)
        
        with col2:
            # Violin plot
            violin_feature = st.selectbox(
                "Select feature for violin plot:",
                numeric_df.columns.tolist(),
                index=numeric_df.columns.tolist().index('Average_Grade') if 'Average_Grade' in numeric_df.columns else 0
            )
            
            fig_violin = px.violin(
                filtered_df,
                y=violin_feature,
                x='sex',
                color='sex',
                box=True,
                title=f'Violin Plot: {violin_feature} by Gender'
            )
            st.plotly_chart(fig_violin, use_container_width=True)
        
        st.markdown("---")
        
        # Categorical Analysis
        st.subheader("🏷️ Categorical Feature Analysis")
        
        categorical_cols = ['school', 'sex', 'address', 'famsize', 'Pstatus', 'Mjob', 'Fjob', 
                           'reason', 'guardian', 'schoolsup', 'famsup', 'paid', 'activities',
                           'nursery', 'higher', 'internet', 'romantic']
        
        selected_cat = st.selectbox(
            "Select categorical feature for detailed analysis:",
            categorical_cols,
            index=0
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Count distribution
            cat_counts = filtered_df[selected_cat].value_counts().reset_index()
            cat_counts.columns = [selected_cat, 'count']
            
            fig_cat_count = px.bar(
                cat_counts,
                x=selected_cat,
                y='count',
                title=f'Distribution of {selected_cat}',
                color='count',
                color_continuous_scale='viridis',
                text='count'
            )
            fig_cat_count.update_traces(textposition='outside')
            st.plotly_chart(fig_cat_count, use_container_width=True)
        
        with col2:
            # Performance by category
            cat_perf = filtered_df.groupby(selected_cat)['Average_Grade'].mean().reset_index()
            cat_perf = cat_perf.sort_values('Average_Grade', ascending=False)
            
            fig_cat_perf = px.bar(
                cat_perf,
                x=selected_cat,
                y='Average_Grade',
                title=f'Average Grade by {selected_cat}',
                color='Average_Grade',
                color_continuous_scale='RdYlGn',
                text='Average_Grade'
            )
            fig_cat_perf.update_traces(texttemplate='%{text:.2f}', textposition='outside')
            st.plotly_chart(fig_cat_perf, use_container_width=True)
        
        # Summary statistics
        st.write(f"**📈 Statistical Summary by {selected_cat}:**")
        
        summary_stats = filtered_df.groupby(selected_cat).agg({
            'Average_Grade': ['count', 'mean', 'std', 'min', 'max'],
            'studytime': 'mean',
            'failures': 'mean',
            'absences': 'mean',
            'G3': 'mean'
        }).round(2)
        
        summary_stats.columns = ['Count', 'Mean_Grade', 'Std_Grade', 'Min_Grade', 'Max_Grade', 
                                 'Avg_StudyTime', 'Avg_Failures', 'Avg_Absences', 'Avg_G3']
        
        st.dataframe(summary_stats, use_container_width=True)
        
        st.markdown("---")
        
        # Advanced Filters and Custom Analysis
        st.subheader("🔬 Custom Analysis Builder")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            x_axis = st.selectbox("X-axis:", numeric_df.columns.tolist(), index=0)
        with col2:
            y_axis = st.selectbox("Y-axis:", numeric_df.columns.tolist(), 
                                 index=1 if len(numeric_df.columns) > 1 else 0)
        with col3:
            color_var = st.selectbox("Color by:", 
                                    ['None', 'sex', 'school', 'address', 'Performance_Category'],
                                    index=1)
        
        color_param = None if color_var == 'None' else color_var
        
        fig_custom = px.scatter(
            filtered_df,
            x=x_axis,
            y=y_axis,
            color=color_param,
            size='G3',
            title=f'Custom Analysis: {x_axis} vs {y_axis}',
            hover_data=['school', 'sex', 'age', 'Average_Grade'],
            trendline="ols" if color_param is None else None
        )
        st.plotly_chart(fig_custom, use_container_width=True)
    
    # ==================== TAB 5: KEY QUESTIONS ====================
    with tab5:
        st.header("❓ Key Questions & Answers")
        
        st.markdown("""
        This section addresses the key analytical questions from the lab exercise.
        """)
        
        # Question 1
        st.subheader("1️⃣ Which features have the highest correlation with final exam scores (G1, G2, G3)?")
        
        g1_corr = numeric_df.corr()['G1'].sort_values(ascending=False).drop('G1')
        g2_corr = numeric_df.corr()['G2'].sort_values(ascending=False).drop('G2')
        g3_corr = numeric_df.corr()['G3'].sort_values(ascending=False).drop('G3')
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("**📝 G1 (First Period)**")
            st.write("Top 5 Correlations:")
            for feat, val in g1_corr.head(5).items():
                st.write(f"- {feat}: **{val:.3f}**")
        
        with col2:
            st.markdown("**📝 G2 (Second Period)**")
            st.write("Top 5 Correlations:")
            for feat, val in g2_corr.head(5).items():
                st.write(f"- {feat}: **{val:.3f}**")
        
        with col3:
            st.markdown("**📝 G3 (Final Grade)**")
            st.write("Top 5 Correlations:")
            for feat, val in g3_corr.head(5).items():
                st.write(f"- {feat}: **{val:.3f}**")
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>💡 Answer:</strong>
        <ul>
            <li><strong>Strongest Predictors:</strong> G1 and G2 are the strongest predictors of G3 (correlation >0.8)</li>
            <li><strong>Academic History:</strong> Previous grades show the highest correlation with final performance</li>
            <li><strong>Other Factors:</strong> Parental education (Medu, Fedu) and past failures also show moderate correlations</li>
            <li><strong>Key Insight:</strong> Early academic performance is the best predictor of final outcomes</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Question 2
        st.subheader("2️⃣ How does study time correlate with exam performance?")
        
        corr_study_g1 = filtered_df['studytime'].corr(filtered_df['G1'])
        corr_study_g2 = filtered_df['studytime'].corr(filtered_df['G2'])
        corr_study_g3 = filtered_df['studytime'].corr(filtered_df['G3'])
        corr_study_avg = filtered_df['studytime'].corr(filtered_df['Average_Grade'])
        
        # Visualization
        study_grade_data = pd.DataFrame({
            'Grade Type': ['G1', 'G2', 'G3', 'Average'],
            'Correlation': [corr_study_g1, corr_study_g2, corr_study_g3, corr_study_avg]
        })
        
        fig_q2 = px.bar(
            study_grade_data,
            x='Grade Type',
            y='Correlation',
            title='Study Time Correlation with Different Grade Types',
            color='Correlation',
            color_continuous_scale='RdYlGn',
            color_continuous_midpoint=0,
            text='Correlation'
        )
        fig_q2.update_traces(texttemplate='%{text:.3f}', textposition='outside')
        st.plotly_chart(fig_q2, use_container_width=True)
        
        # Detailed analysis by study time level
        study_analysis = filtered_df.groupby('studytime').agg({
            'G1': 'mean',
            'G2': 'mean',
            'G3': 'mean',
            'Average_Grade': 'mean',
            'studytime': 'count'
        }).round(2)
        study_analysis.columns = ['Avg_G1', 'Avg_G2', 'Avg_G3', 'Avg_Grade', 'Student_Count']
        study_analysis.index.name = 'Study_Time_Level'
        
        st.write("**Average Grades by Study Time Level:**")
        st.dataframe(study_analysis, use_container_width=True)
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>💡 Answer:</strong>
        <ul>
            <li><strong>Overall Correlation:</strong> {corr_study_avg:.3f} - {"Positive but moderate" if 0.1 < corr_study_avg < 0.3 else "Strong positive" if corr_study_avg >= 0.3 else "Weak"} relationship</li>
            <li><strong>Pattern:</strong> Study time shows {"consistent positive correlation" if corr_study_avg > 0.1 else "minimal correlation"} with all grade periods</li>
            <li><strong>Quality vs Quantity:</strong> Some students achieve high grades with less study time, suggesting study efficiency matters</li>
            <li><strong>Recommendation:</strong> Focus on effective study strategies rather than just increasing hours</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Question 3
        st.subheader("3️⃣ What insights can you draw from the boxplot?")
        
        # Create comprehensive boxplot for key metrics
        key_metrics = ['G1', 'G2', 'G3', 'studytime', 'failures', 'absences', 'Medu', 'Fedu']
        available_metrics = [m for m in key_metrics if m in numeric_df.columns]
        
        fig_q3 = go.Figure()
        
        for col in available_metrics:
            fig_q3.add_trace(go.Box(
                y=filtered_df[col],
                name=col,
                boxmean='sd'
            ))
        
        fig_q3.update_layout(
            title='Boxplot Distribution of Key Features',
            yaxis_title='Values',
            height=500,
            showlegend=True
        )
        st.plotly_chart(fig_q3, use_container_width=True)
        
        # Calculate statistics
        grade_outliers = len(filtered_df[filtered_df['G3'] < (filtered_df['G3'].quantile(0.25) - 1.5 * (filtered_df['G3'].quantile(0.75) - filtered_df['G3'].quantile(0.25)))])
        absence_outliers = len(filtered_df[filtered_df['absences'] > (filtered_df['absences'].quantile(0.75) + 1.5 * (filtered_df['absences'].quantile(0.75) - filtered_df['absences'].quantile(0.25)))])
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>💡 Answer - Key Boxplot Insights:</strong>
        <ul>
            <li><strong>Grade Distribution:</strong> G1, G2, G3 show relatively symmetric distributions around median of ~{filtered_df['G3'].median():.1f}</li>
            <li><strong>Spread:</strong> Interquartile range indicates diverse student performance levels</li>
            <li><strong>Outliers:</strong> {grade_outliers} students with exceptionally low grades; {absence_outliers} students with very high absences</li>
            <li><strong>Study Time:</strong> Most students cluster around level 2 (2-5 hours weekly)</li>
            <li><strong>Failures:</strong> Right-skewed distribution - most students have 0 failures, few with multiple</li>
            <li><strong>Absences:</strong> Heavy right skew - most attend regularly, some chronic absentees</li>
            <li><strong>Parental Education:</strong> Varies widely, showing diverse family backgrounds</li>
            <li><strong>Actionable Insight:</strong> Focus intervention on outlier students (low performers, high absences)</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Question 4
        st.subheader("4️⃣ How does gender impact the final exam score?")
        
        # Statistical comparison
        male_stats = filtered_df[filtered_df['sex'] == 'M']['G3'].describe()
        female_stats = filtered_df[filtered_df['sex'] == 'F']['G3'].describe()
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**👨 Male Students (M)**")
            st.write(f"- **Count:** {male_stats['count']:.0f}")
            st.write(f"- **Mean:** {male_stats['mean']:.2f}")
            st.write(f"- **Median:** {male_stats['50%']:.2f}")
            st.write(f"- **Std Dev:** {male_stats['std']:.2f}")
            st.write(f"- **Min:** {male_stats['min']:.0f}")
            st.write(f"- **Max:** {male_stats['max']:.0f}")
        
        with col2:
            st.markdown("**👩 Female Students (F)**")
            st.write(f"- **Count:** {female_stats['count']:.0f}")
            st.write(f"- **Mean:** {female_stats['mean']:.2f}")
            st.write(f"- **Median:** {female_stats['50%']:.2f}")
            st.write(f"- **Std Dev:** {female_stats['std']:.2f}")
            st.write(f"- **Min:** {female_stats['min']:.0f}")
            st.write(f"- **Max:** {female_stats['max']:.0f}")
        
        # Visualization
        fig_q4 = go.Figure()
        
        fig_q4.add_trace(go.Box(
            y=filtered_df[filtered_df['sex'] == 'M']['G3'],
            name='Male',
            marker_color='lightblue',
            boxmean='sd'
        ))
        
        fig_q4.add_trace(go.Box(
            y=filtered_df[filtered_df['sex'] == 'F']['G3'],
            name='Female',
            marker_color='lightpink',
            boxmean='sd'
        ))
        
        fig_q4.update_layout(
            title='Final Grade (G3) Distribution by Gender',
            yaxis_title='Final Grade (G3)',
            height=500
        )
        st.plotly_chart(fig_q4, use_container_width=True)
        
        # Additional analysis
        gender_perf_cat = pd.crosstab(filtered_df['sex'], filtered_df['Performance_Category'], normalize='index') * 100
        
        fig_gender_cat = px.bar(
            gender_perf_cat.T,
            title='Performance Category Distribution by Gender (%)',
            labels={'value': 'Percentage', 'Performance_Category': 'Performance Category'},
            barmode='group'
        )
        st.plotly_chart(fig_gender_cat, use_container_width=True)
        
        diff = female_stats['mean'] - male_stats['mean']
        
        st.markdown(f"""
        <div class='insight-box'>
        <strong>💡 Answer - Gender Impact on Performance:</strong>
        <ul>
            <li><strong>Mean Difference:</strong> {"Females" if diff > 0 else "Males"} score {abs(diff):.2f} points higher on average</li>
            <li><strong>Statistical Significance:</strong> {"Moderate" if abs(diff) > 1 else "Minimal"} gender difference in performance</li>
            <li><strong>Distribution:</strong> Both genders show similar spread and distribution patterns</li>
            <li><strong>Pass Rates:</strong> {"Females" if (filtered_df[filtered_df['sex']=='F']['G3']>=10).mean() > (filtered_df[filtered_df['sex']=='M']['G3']>=10).mean() else "Males"} have slightly higher pass rates</li>
            <li><strong>Variability:</strong> {"Males" if male_stats['std'] > female_stats['std'] else "Females"} show slightly more variation in scores</li>
            <li><strong>Conclusion:</strong> Gender has {"minimal" if abs(diff) < 1 else "moderate"} direct impact; individual factors matter more</li>
        </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Summary and Recommendations
        st.subheader("📌 Overall Summary & Recommendations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class='insight-box'>
            <strong>🎯 Key Findings:</strong>
            <ul>
                <li>Early grades (G1, G2) are strongest predictors of final performance</li>
                <li>Study time shows positive but moderate correlation with grades</li>
                <li>Past failures and absences negatively impact performance</li>
                <li>Parental education influences student outcomes</li>
                <li>Gender differences are minimal compared to individual factors</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class='insight-box'>
            <strong>💼 Recommendations:</strong>
            <ul>
                <li>Implement early intervention for students with low G1 scores</li>
                <li>Focus on study quality and efficiency training</li>
                <li>Monitor and support students with high absence rates</li>
                <li>Provide additional resources for students with past failures</li>
                <li>Consider family background in support programs</li>
            </ul>
            </div>
            """, unsafe_allow_html=True)

else:
    # Use Markdown to render the Flaticon icon and message in white
    st.markdown("""
    <div style="display: flex; align-items: center; font-size: 15px; color: #000000; background: #fcf75e; padding: 0.5rem 1.5rem; border-radius: 8px; margin-bottom: 1rem;">
        <i class="fi fi-br-octagon-exclamation" style="font-size: 1.5rem; margin-right: 1rem;"></i>
        <span>Please upload the CSV file to begin analysis</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    ### 📚 About This Dashboard
    
    This interactive dashboard provides comprehensive analysis of student performance data including:
    
    - **📊 Overview:** Key metrics, data preview, and summary statistics
    - **📈 Performance Analysis:** Interactive visualizations of grades, study patterns, and demographics
    - **🔍 Correlations:** Heatmaps, pair plots, and feature importance analysis
    - **📋 Data Exploration:** Boxplots, distributions, and categorical analysis
    - **❓ Key Questions:** Detailed answers to analytical questions
    
    **Technologies Used:** Python, Streamlit, Pandas, NumPy, Plotly, Seaborn   
    """)

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #777; padding: 2rem;'>
    <p style='font-size: 15px;'><strong>ITD105 - BIG DATA ANALYTICS</strong></p>
    <p>Student Performance Analysis Dashboard | Built with Streamlit</p>
    <p style='font-size: 0.8rem;'>Enhanced with interactive visualizations, comprehensive filters, and detailed insights</p>
    <p style='font-size: 0.8rem; margin-top: 1rem;'>&copy; 2025 Elizabeth R. Refugio. All rights reserved.</p>
</div>
""", unsafe_allow_html=True)