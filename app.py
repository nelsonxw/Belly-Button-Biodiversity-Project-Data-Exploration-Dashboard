import datetime as dt
import numpy as np
import pandas as pd

from flask import (
    Flask,
    render_template,
    jsonify,
    request,
    redirect)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    # render dashboard homepage
    return render_template("index.html")

@app.route("/names")
def names():
    df = pd.read_csv("datasets\\belly_button_biodiversity_samples.csv")
    sample_data = df.set_index("otu_id").keys()
    return jsonify(sample_data.tolist())

@app.route("/otu")
def otu_descriptions():
    df = pd.read_csv("datasets\\belly_button_biodiversity_otu_id.csv")
    otu_descriptions = df["lowest_taxonomic_unit_found"]
    return jsonify(otu_descriptions.tolist())

@app.route("/metadata/<sample>")
def metadata(sample):
    sampleID = sample[3:]
    df = pd.read_csv("datasets\\Belly_Button_Biodiversity_Metadata.csv")
    meta_data = df[df["SAMPLEID"] == int(sampleID)][["SAMPLEID","ETHNICITY","GENDER","AGE","BBTYPE","LOCATION"]]
    return jsonify(meta_data.to_dict("records"))


@app.route("/wfreq/<sample>")
def washFrequency(sample):
    sampleID = sample[3:]
    df = pd.read_csv("datasets\\Belly_Button_Biodiversity_Metadata.csv")
    wash_data = df[df["SAMPLEID"] == int(sampleID)]["WFREQ"].astype(int)
    return jsonify(wash_data.tolist())

@app.route("/samples/<sample>")
def samples(sample):
    df_samples = pd.read_csv("datasets\\belly_button_biodiversity_samples.csv")
    df_otu = pd.read_csv("datasets\\belly_button_biodiversity_otu_id.csv")
    df = df_samples.merge(df_otu,how="left")
    df = df[df[sample] > 0]
    samples = df[["otu_id","lowest_taxonomic_unit_found",sample]].sort_values(sample,ascending=False)
    samples.columns = ["otu_id","otu_descriptions","sampleValue"]
    samples = [samples.to_dict("list")]
    return jsonify(samples)


if __name__ == '__main__':
    app.run(debug=True)
    # Bind to PORT if defined, otherwise default to 5000.
    # port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=5000)