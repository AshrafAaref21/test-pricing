import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image

# open Etman logo file
img = Image.open("etman_logo.ico")
img = img.resize((100, 100))
# Set up the page configuration
st.set_page_config(
    page_title="Etman Group",
    page_icon=img,
    layout="wide",
)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.header('Etman Pricing\nMade by Eng\\ ***Ashraf Aaref***')

with col5:
    st.image(img)

st.divider()


product_bx = st.selectbox('Choose The Product', [
                          'Scotch', 'Alumnium Foil', 'Alumnium Tray', 'x'], index=0)
st.divider()

if product_bx == 'Scotch':

    # Reading latest Scotch Cost
    df_data = pd.read_excel(
        r'rate.xlsx',
        #   sheet_name='Final',
        index_col=0
    )


    # Reading latest Shrink Data
    df_shrink = pd.read_excel(
        r'scotch priceing 9.xlsx',
        sheet_name='تكلفة الفارغ',
        # index_col=0,
        header=2,
        usecols=[0, 5, 6],
        names=['width', 'core_cost', 'shrink_cost']
    )

    df_shrink.width = df_shrink.width.astype(float)
    df_shrink.set_index('width', inplace=True)

    # Reading the latest Production cost
    df_production = pd.read_excel(
        r'overhead.xlsx',
        sheet_name='cost_per_meter',
    )
    df_production.set_index('units', inplace=True)

    # Creating Radio button for Scotch Types
    color_option = st.radio('Choose Scotch Color', [
                            'Clear', 'Crystal', 'Super', 'Color', 'Doku', 'Laser'], index=0)

    st.divider()

    if color_option not in ['Doku', 'Laser']:
        # Create input for Scotch features
        micron = st.number_input(
            'Micron', min_value=30, max_value=60, value=45, step=1)
        width = st.selectbox('Choose The Width in CM (العرض)', df_shrink.index)
        length = st.number_input(
            'Length in Meter (الطول)', min_value=1.0, value=15.0)
        n_rollers = st.number_input(
            'Rollers Quantity (عدد البكر في الكرتونة)', min_value=1, step=1)

        # Calculate the meter Price
        rate = df_data.loc[color_option, 'rate']
        meter_price = rate * micron
        # Calculate The raw Material cost
        raw = length * meter_price

        # Calculate the Shrink Cost
        if length >= 200:
            shrink = 0
        else:
            shrink = df_shrink.loc[width, 'shrink_cost']

        # Calculate the Core Cost
        core = df_shrink.loc[width, 'core_cost']

        # Calculate the Production Cost
        if color_option in ['Clear', 'Color']:
            if width == 1.2:
                production = (length * width/100) * n_rollers * \
                    df_production.iloc[0, 0]
            elif width in [1.8, 2.3, 2.4]:
                production = (length * width/100) * n_rollers * \
                    df_production.iloc[1, 0]
            else:
                if length > 0 and length <= 15:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[2, 0]
                elif length > 15 and length <= 40:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[3, 0]
                elif length > 40 and length <= 60:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[4, 0]
                elif length > 60 and length <= 100:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[5, 0]
                elif length > 100 and length <= 150:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[6, 0]
                elif length > 150 and length <= 250:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[7, 0]
                elif length > 250:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[8, 0]
        else:
            if width == 1.2:
                production = (length * width/100) * n_rollers * \
                    df_production.iloc[0, 1]
            elif width in [1.8, 2.3, 2.4]:
                production = (length * width/100) * n_rollers * \
                    df_production.iloc[1, 1]
            else:
                if length > 0 and length <= 15:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[2, 1]
                elif length > 15 and length <= 40:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[3, 1]
                elif length > 40 and length <= 60:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[4, 1]
                elif length > 60 and length <= 100:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[5, 1]
                elif length > 100 and length <= 150:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[6, 1]
                elif length > 150 and length <= 250:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[7, 1]
                elif length > 250:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[8, 1]

        if n_rollers >= 6:
            TOTAL_COST = meter_price * \
                (length*width/100)*n_rollers + \
                1.15*production + n_rollers*(shrink + core) + 23
            Total_Price = TOTAL_COST * 1.03
        else:
            TOTAL_COST = meter_price * \
                (length*width/100)*n_rollers + \
                1.15*production + n_rollers*(shrink + core)
            Total_Price = TOTAL_COST * 1.03

        btn = st.button('Calculate', type="primary")
        if btn:
            # st.write(f"""
            #          length=>{length}\n
            #          width=>{width}\n
            #          meter_price=>{meter_price}\n
            #          n_rollers=>{n_rollers}\n
            #          shrink=>{shrink}\n
            #          core=>{core}\n
            #          production=>{production}\n""")
            st.success(int(np.ceil(Total_Price/5)*5))
            # st.success(Total_Price)
            st.snow()

    # Doku And Laser
    else:
        if color_option == 'Doku':
            width = st.selectbox(
                'Choose The Width in CM (العرض)', df_shrink.index)
        else:
            width = st.selectbox('Choose The Width in CM (العرض)', [
                                 1.2, 2.3, 4.5, 4.8])
        length = st.number_input('Length in Meter (الطول)', min_value=1)
        n_rollers = st.number_input(
            'Rollers Quantity (عدد البكر في الكرتونة)', min_value=1, step=1)

        # Calculate the meter Price
        meter_price = df_data.loc[color_option, 'rate']
        # Calculate The raw Material cost
        raw = length * meter_price

        # Calculate the Shrink Cost
        if length >= 200:
            shrink = 0
        else:
            shrink = df_shrink.loc[width, 'shrink_cost']

        # Calculate the Core Cost
        core = df_shrink.loc[width, 'core_cost']

        if color_option == 'Doku':

            if width in [1.2, 1.8, 2.3, 2.4]:
                production = (length * width/100) * n_rollers * \
                    df_production.iloc[1, 2]
            else:
                if length > 0 and length <= 15:
                    production = (length * n_rollers * width /
                                  100) * df_production.iloc[2, 2]
                  #   st.write('yaaaaa')
                elif length > 15 and length <= 40:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[3, 2]
                  #   st.write('ya:false')
                elif length > 40 and length <= 60:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[4, 2]
                  #   st.write('ya:false2')
                elif length > 60 and length <= 100:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[5, 2]
                  #   st.write('ya:false3')
                elif length > 100 and length <= 150:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[6, 2]
                  #   st.write('ya:false4')
                elif length > 150 and length <= 250:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[7, 2]
                  #   st.write('ya:false5')
                elif length > 250:
                    production = (length * width/100) * \
                        n_rollers * df_production.iloc[8, 2]
                  #   st.write('ya:false6')

        else:
            if width == 1.2:
                production = (length * n_rollers * width/100) * \
                    df_production.iloc[0, 3]
               #  st.write('ya:falsec1')
            if width == 2.3:
                production = (length * n_rollers * width/100) * \
                    df_production.iloc[0, 3]
               #  st.write('ya:falsec2')
            if width == 4.5:
                production = (length * n_rollers * width/100) * \
                    df_production.iloc[0, 3]
               #  st.write('ya:falsec3')
            if width == 4.8:
                production = (length * n_rollers * width/100) * \
                    df_production.iloc[0, 3]
               #  st.write('ya:falsec4')

        # Total Cost Formula
        if n_rollers >= 6:
            TOTAL_COST = meter_price * \
                (length*width/100)*n_rollers + \
                1.15*production + n_rollers*(shrink + core) + 23
            Total_Price = TOTAL_COST * 1.03
        else:
            TOTAL_COST = meter_price * \
                (length*width/100)*n_rollers + \
                1.15*production + n_rollers*(shrink + core)
            Total_Price = TOTAL_COST * 1.03

        # Create the cost estimate button
        btn = st.button('Calculate', type="primary")
        if btn:
            # st.write(f"""
            #          length=>{length}\n
            #          width=>{width}\n
            #          meter_price=>{meter_price}\n
            #          n_rollers=>{n_rollers}\n
            #          shrink=>{shrink}\n
            #          core=>{core}\n
            #          production=>{production}\n""")
            # # st.write(df_production.iloc[2, 2])
            # st.write(df_production.iloc[2, 2] *
            #          length * width * n_rollers / 100)
            st.success(int(np.ceil(Total_Price/5)*5))
            # st.success(Total_Price)
            st.snow()
