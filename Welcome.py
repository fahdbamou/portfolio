import streamlit as st

# Main header for the page
#t.header("Welcome to my portfolio")

# Creating two columns with specified width ratio
col1, col2 = st.columns([1,3])

with col1:
    # Displaying an image
    st.image('https://static.streamlit.io/examples/owl.jpg')
    # Adding name as a header
    st.header('Fahd Bamou')
    # Adding professional title as a subheader
    st.subheader(":blue[Business Intelligence Analyst]")

with col2:
    # Introduction section title
    #st.subheader("Introduction:")
    # Introduction text. Using st.write or st.markdown for better text formatting
    st.write('Hello, I am FAHD BAMOU, a certified Data Analyst and Business Intelligence professional with a unique background in civil engineering. My journey in the data field began over six years ago, driven by a passion for turning complex data into compelling visual stories. I specialize in leveraging data to drive business strategy, operational efficiency, and innovation.')

    # Introduction section title
    st.subheader("Professional Background:")
    st.write("My career commenced in 2012 as a civil engineer, where I developed a keen eye for detail and a rigorous analytical approach. This foundation paved the way for my transition into the realm of data analytics. Over the years, I have dedicated myself to mastering various aspects of data analysis and business intelligence. My expertise now lies in transforming raw data into meaningful insights that inform strategic decisions and enhance business processes.")

    # Introduction section title
    st.subheader("Certification and Technical Skills:")
    st.write("As a Google-certified Business Intelligence professional, I possess a deep understanding of data analysis tools and methodologies. My technical arsenal includes advanced proficiency in SQL, Python, and BI tools like Tableau, Power BI, and Google Analytics. These skills enable me to adeptly navigate and interpret complex data landscapes.")


    # Introduction section title
    st.subheader("Experience Highlights:")
    st.write("Throughout my six-year tenure in data analytics, I have particularly enjoyed creating dashboards and visualizations that resonate with stakeholders. Key accomplishments include")
    st.write('- Developing intuitive dashboards that simplify complex engineering data, facilitating better project management and decision-making.')
    st.write('- Implementing data warehousing solutions that have streamlined data processing and reporting workflows.')
    st.write('- Crafting predictive models that have enhanced business forecasting and operational planning.')
    st.write('- Leading initiatives to integrate data-driven insights into core business strategies, significantly improving overall performance metrics.')
    st.write('- These experiences have not only solidified my analytical prowess but also reinforced my ability to translate data into visually engaging and easily understandable formats for diverse audiences.')
    st.subheader("Professional Philosophy:")
    st.write("My approach marries my engineering discipline with my enthusiasm for data visualization. I am committed to translating complex data sets into clear, impactful visual stories, thereby bridging the gap between intricate data analysis and strategic business applications. Staying at the forefront of data trends and technologies is fundamental to my professional ethos.")
