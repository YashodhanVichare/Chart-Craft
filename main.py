import streamlit as st
import pandas as pd
import plotly.express as px



# ----------------------------------------------------------------------------------------------------------------------#
st.set_page_config(
    page_title="ChartCraft",
    page_icon=":chart_with_upwards_trend:",
    layout="wide",
    initial_sidebar_state="expanded"
)
# ----------------------------------------------------------------------------------------------------------------------#
st.markdown(
    """
    <style>
    .sidebar .sidebar-content {
        background-color: #08FFC8;
        padding: 10px;
    }
    .title {
        font-size: 3rem;
        font-weight: bold;
        color: #9BEC00;
        text-shadow: 0 0 5px #9BEC00;
        margin-bottom: 1rem;
    }
    .subtitle {
        font-size: 1.5rem;
        color: #BBB;
        margin-bottom: 2rem;
    }
    .section-header {
        font-size: 1.5rem;
        font-weight: bold;
        color: #15F5BA;
        text-shadow: 0 0 5px #15F5BA;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .chart-container {
        margin-top: 2rem;
        border-radius: 10px;
        box-shadow: 0 0 20px rgba(255, 255, 255, 0.1);
        padding: 20px;
        background-color: #2a2a2a;
    }
    .error-message {
        color: red;
        font-weight: bold;
        margin-top: 1rem;
    }
    .button {
        display: inline-block;
        padding: 10px 20px;
        font-size: 16px;
        color: #fff;
        background-color: #007bff;
        text-align: center;
        text-decoration: none;
        border-radius: 5px;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# ----------------------------------------------------------------------------------------------------------------------#
# -----------------------------------------Main title and subtitle------------------------------------------------------#
st.markdown('<h1 class="title">ChartCraft</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Craft charts that convince, every time.</p>', unsafe_allow_html=True)


# ---------------------------Uploading of the CSV or EXCEL FILE---------------------------------------------------------#
uploaded_file = st.file_uploader("Upload your CSV or Excel file", type=["csv", "xlsx"])
# ----------------------------------------------------------------------------------------------------------------------#
if uploaded_file is not None:
    try:
        if uploaded_file.type == "text/csv":
            df = pd.read_csv(uploaded_file, encoding='utf-8')
        else:
            df = pd.read_excel(uploaded_file)


        # -------to diplsay the dataset------------#
        if st.checkbox("Show uploaded dataset"):
            st.subheader("Uploaded Dataset")
            st.write(df)


        # ---------delete the duplicate value----------#
        cleaned_df = df.drop_duplicates()


        # -----------------------sorting of the data----------------------#
        st.sidebar.markdown('<p class="section-header">Data Sorting</p>', unsafe_allow_html=True)
        sort_column = st.sidebar.selectbox("Select column to sort by", cleaned_df.columns)
        sort_ascending = st.sidebar.checkbox("Sort ascending", True)


        if st.sidebar.button("Sort Data"):
            cleaned_df.sort_values(by=sort_column, ascending=sort_ascending, inplace=True)
            st.subheader("Sorted Data")
            st.write(cleaned_df)
            st.success("Data sorted successfully!")


        # ---------------Max,Min,Sum,Meadian,Mean Functions-----------------#
        st.sidebar.markdown('<p class="section-header">Data Aggregation</p>', unsafe_allow_html=True)
        aggregation_type = st.sidebar.selectbox(
            "Select aggregation type",
            ["Sum", "Mean", "Median", "Min", "Max"]
        )
        aggregation_column = st.sidebar.selectbox("Select column to aggregate",
                                                  cleaned_df.select_dtypes(include='number').columns)
        if st.sidebar.button("Aggregate Data"):
            if aggregation_type == "Sum":
                aggregated_df = cleaned_df.groupby(by=aggregation_column).sum().reset_index()
            elif aggregation_type == "Mean":
                aggregated_df = cleaned_df.groupby(by=aggregation_column).mean().reset_index()
            elif aggregation_type == "Median":
                aggregated_df = cleaned_df.groupby(by=aggregation_column).median().reset_index()
            elif aggregation_type == "Min":
                aggregated_df = cleaned_df.groupby(by=aggregation_column).min().reset_index()
            elif aggregation_type == "Max":
                aggregated_df = cleaned_df.groupby(by=aggregation_column).max().reset_index()
            st.subheader(f"{aggregation_type} Aggregated Data")
            st.write(aggregated_df)
        # -------------seacrh the data by specifing columns-----------------------#
        st.sidebar.markdown('<p class="section-header">Data Search</p>', unsafe_allow_html=True)
        search_columns = st.sidebar.multiselect("Select columns for search criteria", cleaned_df.columns)
        search_terms = {}
        for column in search_columns:
            search_terms[column] = st.sidebar.text_input(f"Enter value to search in '{column}'", "")
        if st.sidebar.button("Search"):
            search_df = cleaned_df.copy()
            for column, term in search_terms.items():
                if term:
                    search_df = search_df[search_df[column].astype(str).str.contains(term, case=False, na=False)]


            st.subheader("Search Results")
            st.write(search_df)


        # ----------customize the chart---------------#
        st.sidebar.markdown('<p class="section-header">Chart Customization</p>', unsafe_allow_html=True)


        # ---------------types of the chart--------------------#
        chart_type = st.sidebar.selectbox(
            "Select chart type",
            ["Line Chart", "Bar Chart", "Scatter Plot", "Pie Chart", "Box Plot", "Area Chart", "Histogram"],
            help="""
            - **Line Chart**: Shows trends over time.
            - **Bar Chart**: Compares categories with bars.
            - **Scatter Plot**: Displays relationships between variables.
            - **Pie Chart**: Illustrates parts of a whole.
            - **Box Plot**: Summarizes data distribution.
            - **Area Chart**: Shows cumulative totals.
            - **Histogram**: Displays distribution of numerical data.
            """
        )


        st.sidebar.markdown('<p class="section-header">Chart Type Suggestions</p>', unsafe_allow_html=True)
        if chart_type == "Line Chart":
            st.sidebar.info("""
                **Line Chart**: Ideal for visualizing trends over time or continuous data points.
                Consider using if you have a time series or sequential data.
            """)
        elif chart_type == "Bar Chart":
            st.sidebar.info("""
                **Bar Chart**: Useful for comparing different categories or discrete data.
                Best for showing comparisons across categories.
            """)
        elif chart_type == "Scatter Plot":
            st.sidebar.info("""
                **Scatter Plot**: Great for visualizing relationships between two variables.
                Use if you want to see how two variables correlate with each other.
            """)
        elif chart_type == "Pie Chart":
            st.sidebar.info("""
                **Pie Chart**: Effective for illustrating parts of a whole.
                Use when you want to show proportions or percentages of a total.
            """)
        elif chart_type == "Box Plot":
            st.sidebar.info("""
                **Box Plot**: Provides a summary of the data distribution.
                Use when you want to understand the spread and skewness of the data.
            """)
        elif chart_type == "Area Chart":
            st.sidebar.info("""
                **Area Chart**: Shows cumulative totals and trends over time.
                Best for illustrating changes and total values over time.
            """)
        elif chart_type == "Histogram":
            st.sidebar.info("""
                **Histogram**: Displays the distribution of numerical data.
                Use to see how data is distributed across different bins or intervals.
            """)


        # -------------------Column selection for the chart----------------#
        selected_columns = st.sidebar.multiselect("Select columns for chart", cleaned_df.columns)


        # ---------------------Input field for the number of rows to be used---------------------------#
        num_rows = st.sidebar.number_input("Enter the number of rows to use", min_value=1, max_value=len(cleaned_df),
                                           value=len(cleaned_df))
        chart_title = st.sidebar.text_input("Enter chart title", "Chart")
        x_axis_label = st.sidebar.text_input("Enter x-axis label", "X-axis") if chart_type != "Pie Chart" else ""
        y_axis_label = st.sidebar.text_input("Enter y-axis label", "Y-axis") if chart_type not in ["Pie Chart",
                                                                                                   "Box Plot"] else ""


        # ----------------Display dataset for selected rows and columns----------------------#
        if st.button("Show Dataset for Selected Rows and Columns"):
            if selected_columns:
                selected_data = cleaned_df[selected_columns].head(num_rows)
                st.subheader("Dataset for Selected Rows and Columns")
                st.write(selected_data)
            else:
                st.warning("Please select columns to display dataset.")
        # ----------------------------------------------------------------------------------------------------------------------#
        generate_chart = st.button("Generate Chart")
        # ---------------------------------------------------------------------------------------------------------------------#
        if generate_chart:
            color_sequence = px.colors.qualitative.Plotly
            try:
                # --------limit of the columns----------------#
                limited_df = cleaned_df[selected_columns].head(num_rows)


                # ----------------------Generate the selected chart----------------------#
                if chart_type == "Line Chart":
                    fig = px.line(limited_df, title=chart_title, color_discrete_sequence=color_sequence)
                    fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
                    code_snippet = f"fig = px.line(limited_df, title='{chart_title}', color_discrete_sequence=color_sequence)\nfig.update_layout(xaxis_title='{x_axis_label}', yaxis_title='{y_axis_label}')"
                elif chart_type == "Bar Chart":
                    fig = px.bar(limited_df, title=chart_title, color_discrete_sequence=color_sequence)
                    fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
                    code_snippet = f"fig = px.bar(limited_df, title='{chart_title}', color_discrete_sequence=color_sequence)\nfig.update_layout(xaxis_title='{x_axis_label}', yaxis_title='{y_axis_label}')"
                elif chart_type == "Scatter Plot":
                    fig = px.scatter(limited_df, title=chart_title, color_discrete_sequence=color_sequence)
                    fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
                    code_snippet = f"fig = px.scatter(limited_df, title='{chart_title}', color_discrete_sequence=color_sequence)\nfig.update_layout(xaxis_title='{x_axis_label}', yaxis_title='{y_axis_label}')"
                elif chart_type == "Pie Chart":
                    fig = px.pie(limited_df, names=limited_df.columns[0], values=limited_df.columns[0],
                                 title=chart_title, color_discrete_sequence=color_sequence)
                    code_snippet = f"fig = px.pie(limited_df, names=limited_df.columns[0], values=limited_df.columns[0], title='{chart_title}', color_discrete_sequence=color_sequence)"
                elif chart_type == "Box Plot":
                    fig = px.box(limited_df, title=chart_title, color_discrete_sequence=color_sequence)
                    code_snippet = f"fig = px.box(limited_df, title='{chart_title}', color_discrete_sequence=color_sequence)"
                elif chart_type == "Area Chart":
                    fig = px.area(limited_df, title=chart_title, color_discrete_sequence=color_sequence)
                    fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
                    code_snippet = f"fig = px.area(limited_df, title='{chart_title}', color_discrete_sequence=color_sequence)\nfig.update_layout(xaxis_title='{x_axis_label}', yaxis_title='{y_axis_label}')"
                elif chart_type == "Histogram":
                    fig = px.histogram(limited_df, title=chart_title, color_discrete_sequence=color_sequence)
                    fig.update_layout(xaxis_title=x_axis_label, yaxis_title=y_axis_label)
                    code_snippet = f"fig = px.histogram(limited_df, title='{chart_title}', color_discrete_sequence=color_sequence)\nfig.update_layout(xaxis_title='{x_axis_label}', yaxis_title='{y_axis_label}')"


                if len(limited_df) == 0:
                    st.error("Insufficient data to generate the chart. Please adjust your selection.")
                else:
                    st.plotly_chart(fig, use_container_width=True)
                    st.success("Chart generated successfully!")
                    st.code(code_snippet, language='python')
            except Exception as e:
                st.error(f"Error generating chart: {str(e)}")
        # --------------exporting the chart-----------------#
        st.sidebar.markdown('<p class="section-header">Export Options</p>', unsafe_allow_html=True)
        export_as = st.sidebar.selectbox("Select export format", ["PNG", "JPEG", "PDF"])
        export_path = st.sidebar.text_input("Enter export path", "chart")


        if st.sidebar.button("Export Chart"):
            try:
                if not export_path:
                    st.error("Please enter a valid export path.")
                else:
                    export_path_with_ext = f"{export_path}.{export_as.lower()}"
                    fig.write_image(export_path_with_ext)
                    st.success(f"Chart exported successfully as {export_as}!")
            except Exception as e:
                st.error(f"Error exporting chart: {str(e)}")


        st.sidebar.markdown('<p class="section-header">Help & Documentation</p>', unsafe_allow_html=True)


        if st.sidebar.button("Show Help"):
            st.info("""
                **Help & Documentation:**
                - Upload your CSV or Excel file to get started.
                - Visit [Streamlit Documentation](https://docs.streamlit.io) for more details.
            """)



    except Exception as e:
        st.error(f"Error reading the file: {str(e)}")
else:
    st.warning("Please upload a CSV or Excel file to proceed.")



