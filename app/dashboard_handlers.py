# masih kotor

import json
from fastapi.templating import Jinja2Templates
from pathlib import Path
import importlib, sys
import os
import pandas as pd
from jcopml.plot import plot_missing_value

sys.path.append(os.path.abspath('..'))
from helper.PlotlyFigHelpers import fig_bar, fig_line, card_template, fig_pie, fig_map, card_template_html_string, fig_map_folium

def main_explore(
        # request, file_path, save_only=False, **params
):
    # return True
    data = create_layout(
        df_csv,
        df_csv_bulan,
        tgdf,
        tgdf_perkecamatan,
        titik_tengah,
    )

    # Inisialisasi templates menggunakan Jinja2
    templates = Jinja2Templates(directory=Path("templates"))
    result = templates.TemplateResponse("dash_explore_template.html", {'request':request,"data": data})

    if (save_only):
        html_string = result.body.decode("utf-8")
        with open(file_path, "w") as file:
            # Tulis string HTML yang telah digabungkan ke dalam file HTML
            file.write(html_string)
        return True
    else:
        return result

def create_layout(
        df_csv,
        df_csv_bulan,
        tgdf,
        tgdf_perkecamatan,
        titik_tengah,
    ):
    
    # inisiasi nilai
    c_transaksi = df_csv.transaction_id.count()
    c_transaksi_daihatsu = (df_csv['immutable_merk'].str.upper() == 'DAIHATSU').sum()
    perc_transaksi_daihatsu = "{:.1f}%".format(
        (c_transaksi_daihatsu/c_transaksi) * 100
    )
    mean_transaksi = "{:.1f}".format(df_csv_bulan.transaksi.mean())
    mean_transaksi_daihatsu = "{:.1f}".format(df_csv_bulan.transaksi_daihatsu.mean())
    c_customer = df_csv.customer_name.nunique()
    
    # grafik
    f_transaksi = fig_line(df_csv, date_column='periode')
    f_type_merk = fig_pie(df_csv, "immutable_type_merk", "Tipe Merk dengan Transaksi Tertinggi")
    f_merk = fig_pie(df_csv, "immutable_merk", "Merk dengan Transaksi Tertinggi")
    f_kecamatan = fig_bar(tgdf, "KECAMATAN", "Kecamatan dengan Transaksi Tertinggi", color_by_filter=False)
    f_map = fig_map_folium(tgdf_perkecamatan, titik_tengah)
    card_1 = card_template_html_string(h4_title='Total Transaksi', p_subtitle='', id_nya='c_transaksi', icon='bx bx-line-chart', placeholder=c_transaksi, sup_subtitle='unit')
    card_2 = card_template_html_string(h4_title='Transaksi Perbulan', p_subtitle='', id_nya='mean_transaksi', icon='bx bx-line-chart', placeholder=mean_transaksi, sup_subtitle='unit')
    card_3 = card_template_html_string(h4_title='Total Trs. Daihatsu', p_subtitle='', id_nya='c_transaksi_daihatsu', icon='bx bx-line-chart', placeholder=c_transaksi_daihatsu, sup_subtitle='unit'+f'({perc_transaksi_daihatsu})')
    card_4 = card_template_html_string(h4_title='Trs. Daihatsu Perbulan', p_subtitle='', id_nya='mean_transaksi_daihatsu', icon='bx bx-line-chart', placeholder=mean_transaksi_daihatsu, sup_subtitle='unit')
    card_5 = card_template_html_string(h4_title='Total Pelanggan', p_subtitle='', id_nya='total_pelanggan', icon='bx bx-user', placeholder=c_customer, sup_subtitle='orang')

    # Data yang ingin Anda sertakan dalam template
    data = {
        'f_transaksi' : f_transaksi.to_html(full_html=False),
        'f_type_merk' : f_type_merk.to_html(full_html=False),
        'f_merk' : f_merk.to_html(full_html=False),
        'f_kecamatan' : f_kecamatan.to_html(full_html=False),
        'f_map' : f_map._repr_html_(),
        'card_1' : card_1,
        'card_2' : card_2,
        'card_3' : card_3,
        'card_4' : card_4,
        'card_5' : card_5,
    }

    return data