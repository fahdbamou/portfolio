import streamlit as st
import pandas as pd
import re

# Streamlit page configuration
st.title("KenshadClean: Your Interactive Data Cleansing Tool")

# Function to convert DataFrame to CSV for download
@st.cache_data
def convert_df_to_csv(df):
    return df.to_csv().encode('utf-8')

# Function to generate the report
def generate_report(df, steps_info):
    report = []

    report.append("# Data Cleaning Report\n")
    report.append("## Introduction\nThis report outlines the steps taken in cleaning the uploaded data.\n")
    report.append("## Data Upload\n")
    report.append(f"- Initial Rows: {steps_info['initial_row_count']}\n")
    report.append("## Data Cleaning Steps\n")
    report.append(f"### Step 1: Handling Missing Values\n- Option Selected: {steps_info['missing_values_option']}\n- Rows Dropped: {steps_info['rows_dropped']}\n- Percentage Dropped: {steps_info['percentage_dropped']:.2f}%\n")
    report.append(f"### Step 2: Removing Duplicate Rows\n- Duplicates Removed: {steps_info['duplicates_removed']}\n- Rows Dropped: {steps_info['duplicate_rows_dropped']}\n- Percentage Dropped: {steps_info['percentage_duplicate_dropped']:.2f}%\n")
    report.append(f"### Step 3: Renaming Columns\n- Columns Renamed: {steps_info['columns_renamed']}\n")
    report.append(f"### Step 4: Filtering Rows\n- Filter Condition: {steps_info['filter_condition']}\n- Rows Meeting Filter: {steps_info['filter_rows']}\n- Percentage of Total: {steps_info['percentage_filtered']:.2f}%\n")
    report.append(f"## Final Cleaned Dataset\n- Total Rows after Cleaning: {df.shape[0]}\n")
    report.append("## Conclusion\nThis report summarizes the data cleaning process undertaken.\n")

    return '\n'.join(report)

# File uploader widget
uploaded_file = st.file_uploader("Upload your CSV or Excel file.", type=["csv", "xlsx"])

# Initialize an empty DataFrame
df = pd.DataFrame()

# Dictionary to store steps information
steps_info = {
    'initial_row_count': 0,
    'missing_values_option': 'Not Applied',
    'rows_dropped': 0,
    'percentage_dropped': 0.0,
    'duplicates_removed': 'No',
    'duplicate_rows_dropped': 0,
    'percentage_duplicate_dropped': 0.0,
    'columns_renamed': 'No',
    'filter_condition': 'None',
    'filter_rows': 0,
    'percentage_filtered': 0.0
}

# Load the uploaded data
if uploaded_file is not None:
    if uploaded_file.name.endswith('.csv'):
        df = pd.read_csv(uploaded_file)
    elif uploaded_file.name.endswith('.xlsx'):
        df = pd.read_excel(uploaded_file)

    # Replace non-alphanumeric characters in column names with underscores
    df.columns = [re.sub(r'\W+', '_', column) for column in df.columns]

    st.write("Raw Data (note: your database must not exceed 10 columns)")
    st.dataframe(df)

    steps_info['initial_row_count'] = df.shape[0]
    st.write(f"Total Rows after Data Upload: {df.shape[0]}")

    if not df.empty:
        st.subheader("Step 1: Handle Missing Values")
        missing_values_option = st.radio("Select an option for handling missing values",
                                         ["Do nothing", "Drop rows", "Fill with mean (numeric columns only)", "Fill with median (numeric columns only)", "Fill with mode (categorical columns only)"])
        original_row_count = df.shape[0]

        if missing_values_option != "Do nothing":
            rows_before = df.shape[0]
            if missing_values_option == "Drop rows":
                df.dropna(inplace=True)
            elif missing_values_option == "Fill with mean":
                df.fillna(df.mean(), inplace=True)
            elif missing_values_option == "Fill with median":
                df.fillna(df.median(), inplace=True)
            elif missing_values_option == "Fill with mode":
                df.fillna(df.mode().iloc[0], inplace=True)
            rows_after = df.shape[0]
            rows_dropped = rows_before - rows_after
            percentage_dropped = (rows_dropped / original_row_count) * 100 if original_row_count > 0 else 0

            steps_info['missing_values_option'] = missing_values_option
            steps_info['rows_dropped'] = rows_dropped
            steps_info['percentage_dropped'] = percentage_dropped

            st.write("Data after handling missing values:")
            st.dataframe(df)
            st.write("Total rows after handling missing values:", df.shape[0])

            # Add this line to display the number of rows handled
            st.write(f"Number of rows handled: {rows_before - df.shape[0]}")
        st.subheader("Step 2: Remove Duplicate Rows")
        if st.checkbox("Remove duplicate rows"):
            rows_before = df.shape[0]
            df.drop_duplicates(inplace=True)
            rows_after = df.shape[0]
            duplicate_rows_dropped = rows_before - rows_after
            percentage_duplicate_dropped = (duplicate_rows_dropped / rows_before) * 100

            steps_info['duplicates_removed'] = 'Yes'
            steps_info['duplicate_rows_dropped'] = duplicate_rows_dropped
            steps_info['percentage_duplicate_dropped'] = percentage_duplicate_dropped

            st.write("Data after removing duplicates:")
            st.dataframe(df)
            st.write(f"Total rows after removing duplicates: {rows_after}")
            st.write(f"Rows deleted: {duplicate_rows_dropped}, Percentage Deleted: {percentage_duplicate_dropped:.2f}%")

        st.subheader("Step 3: Rename Columns")
        if st.checkbox("Rename columns"):
            st.write("New names should be one word or multiple words separated by underscores.")
            col1, col2 = st.columns(2)
            new_names = {}
            with col1:
                st.write("Current Column Names")
                st.write(df.columns)
            with col2:
                st.write("Enter New Column Names")
                for column in df.columns:
                    new_name = st.text_input(f"{column}", key=column)
                    if new_name:
                        new_names[column] = new_name
            if st.button("Apply New Column Names"):
                df.rename(columns=new_names, inplace=True)
                steps_info['columns_renamed'] = 'Yes'
                st.write("Data with renamed columns:")
                st.dataframe(df)

        st.subheader("Step 4: Filter Rows Based on Conditions")
        filter_condition = st.text_input("Enter the filter condition (e.g., AveragePrice > 1.79)")
        if filter_condition:
            try:
                df_filtered = df.query(filter_condition)
                filtered_rows_count = df_filtered.shape[0]
                total_count = df.shape[0]
                percentage_filtered = (filtered_rows_count / total_count) * 100 if total_count > 0 else 0
                df = df_filtered  # Update the main DataFrame to be the filtered one
                steps_info['filter_condition'] = filter_condition
                steps_info['filter_rows'] = filtered_rows_count
                steps_info['percentage_filtered'] = percentage_filtered
            except Exception as e:
                st.error(f"Error in filter condition: {e}")

        if not df.empty:
            st.subheader("Final Cleaned Data")
            st.dataframe(df)

            # Display the number of rows meeting filter conditions and their percentage
            if 'filter_condition' in steps_info and steps_info['filter_condition'] != 'None':
                st.write(f"Number of rows meeting the filter condition: {steps_info['filter_rows']}")
                st.write(f"Percentage of total rows meeting the filter condition: {steps_info['percentage_filtered']:.2f}%")

            st.markdown("""
            #### Review and Download
            - **Review**: Check the final cleaned data.
            - **Report**: Generate a report detailing the cleaning steps.
            - **Download**: Download the cleaned dataset in CSV format.
            """)


            # Generate Report
            if st.button("Generate Data Cleaning Report"):
                report = generate_report(df, steps_info)
                st.text(report)

            # Download button
            csv = convert_df_to_csv(df)
            st.download_button("Download Cleaned Data", csv, "cleaned_data.csv", "text/csv", key='download-csv')
