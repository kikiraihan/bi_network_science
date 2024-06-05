import plotly.express as px
import random

def fig_bar(tdf, filter, default_agg_col, default_agg, added_agg_data={}, batas=10, color_by_filter=True, xlabel='Transaksi'):
    ylabel = filter
    agg_data = {
        default_agg_col:default_agg, #default
    }
    agg_data.update(added_agg_data)
    result = tdf.groupby(by=filter, as_index=False).agg(agg_data).rename(columns={default_agg_col: default_agg}).sort_values(default_agg, ascending=False)[:batas][::-1] #potong batas dan reverse

    if color_by_filter:
        color = filter
    else:
        color = None

    # Membuat barplot menggunakan Plotly
    fig = px.bar(
        result, x=default_agg, y=filter, text=default_agg,
        # title=title,
        labels={filter: ylabel, default_agg: xlabel},
        hover_data=added_agg_data.keys(),  # Menambahkan informasi 'KECAMATAN' pada hover
        template='seaborn'
        ) # atau gunakan 'viridis' untuk palette

    # Menyesuaikan tampilan teks di tiap bar
    fig.update_traces(texttemplate='%{text:.2s}')

    # Menyesuaikan layout
    fig.update_layout(
        # xaxis=dict(title=xlabell), #, tickangle=-45
        # yaxis=dict(title=xlabel),
        showlegend=False,
        margin={"r":10,"t":10,"l":10,"b":10}
    )

    return fig

def fig_pie(tdf, filter, title, added_agg_data={}, batas=10):
    xlabel = filter.replace("immutable_", "")
    agg_data = {
        'transaction_id':'nunique',
    }
    agg_data.update(added_agg_data)
    result = tdf.groupby(by=filter, as_index=False).agg(agg_data).rename(columns={'transaction_id': 'count'}).sort_values('count', ascending=False)[:batas]

    # Membuat pie chart menggunakan Plotly
    fig = px.pie(
        result, values='count', names=filter, 
        # title=title,
        labels={filter: xlabel, 'count': 'Transaksi'},
        # hover_data=added_agg_data.keys(),  # Tidak diperlukan pada pie chart
        template='seaborn'
        ) # atau gunakan 'viridis' untuk palette

    # Menyesuaikan layout
    fig.update_layout(
        showlegend=True, # Pie chart biasanya menggunakan legend
        margin={"r":10,"t":10,"l":10,"b":10}
    )

    return fig


def fig_line(tgdf, default_agg_col, default_agg, date_column='tanggal', ):
    result = tgdf.groupby(by=[date_column], as_index=False).agg({
        default_agg_col:default_agg,
    }).rename(columns={'transaction_id': 'count'})

    # Membuat lineplot dengan Plotly
    fig = px.line(
        result, x=date_column, y='count', #color='tahun_bulan', 
        # title='Jumlah transaksi di MAKASSAR dalam bulan tertentu di tahun 2023',
        # labels={'tahun_bulan': 'Bulan', 'count': 'Jumlah'},
        markers=True,  # Menambahkan marker untuk tiap titik data
        template='seaborn'  # Anda dapat mengganti dengan template yang diinginkan
    )

    # Menambahkan teks untuk setiap titik data
    # for tahun in result['tahun_bulan'].unique():
    #     tahun_data = result[result['tahun_bulan'] == tahun]
    #     for x, y in zip(tahun_data[date_column], tahun_data['count']):
    #         fig.add_annotation(x=x, y=y, text=str(y), showarrow=False, yshift=10)

    # Menyesuaikan tampilan plot
    fig.update_layout(
        margin={"r":20,"t":20,"l":20,"b":20},
        legend_title_text='Tahun - Bulan',
        xaxis_title='Tanggal',
        yaxis_title='Jumlah',
        # Update layout untuk menampilkan sumbu x per bulan
        xaxis=dict(
            tickmode='auto',
            nticks=len(result['tahun_bulan']),
            tickformat='%b %Y',  # Format bulan dan tahun, contoh: Jan 2023
        )
    )

    return fig


def card_template_html_string(h4_title, p_subtitle, id_nya, icon, placeholder="", sup_subtitle=""):
    return '''
    <div class="metric-card p-4 bg-white shadow-md rounded-lg">
        <h4 class="text-lg font-bold text-gray-800">{}</h4>
        <div class="flex justify-between items-center">
            <div>
                <p class="text-sm text-gray-600 mr-2">{}</p>
                <h2 id="{}" class="text-4xl font-bold text-blue-500">{}</h2>
                <sup class="text-gray-600">{}</sup>
            </div>
            <i class="{} text-gray-600 text-4xl"></i>
        </div>
    </div>
    '''.format(h4_title, p_subtitle, id_nya, placeholder, sup_subtitle, icon)